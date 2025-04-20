# This file is part of Build Your Own Config
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2013-2016 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""Configuration stores contains key/value definitions.

They may define a single level of sections, each of which containing key/value
definitions.
"""
import collections
import errno
import io
import os
import warnings

from byoc import (
    errors,
    parsers,
)


class Section(object):
    """A section defines a dict of option name => value.

    This is merely a read-only dict which can add some knowledge about the
    options. It is *not* a python dict object though and doesn't try to mimic
    its API.
    """

    def __init__(self, section_id, options):
        self.id = section_id
        # We re-use the dict-like object received
        self.options = options

    def get(self, name, default=None):
        return self.options.get(name, default)

    def iter_option_names(self):
        for k in self.options.keys():
            yield k

    def __repr__(self):
        # Mostly for debugging purposes
        return "<stores.%s id=%s>" % (self.__class__.__name__, self.id)


_NewlyCreatedOption = object()
"""Was the option created during the MutableSection lifetime"""
_DeletedOption = object()
"""Was the option deleted during the MutableSection lifetime"""


class MutableSection(Section):
    """A section allowing changes and keeping track of the original values."""

    def __init__(self, section_id, options):
        super(MutableSection, self).__init__(section_id, options)
        self.reset_changes()

    def reset_changes(self):
        self.orig = {}

    def set(self, name, value):
        if name not in self.options:
            # This is a new option
            self.orig[name] = _NewlyCreatedOption
        elif name not in self.orig:
            self.orig[name] = self.get(name, None)
        self.options[name] = value

    def remove(self, name):
        if name not in self.orig and name in self.options:
            # Preserve value
            self.orig[name] = self.get(name, None)
        # And get rid of it
        del self.options[name]

    def apply_changes(self, dirty):
        """Apply option value changes.

        :param dirty: mutable section containing the changes made since the
            previous loading.

        This applies the recorded `dirty` changes in self.options, `self.orig`
        is then reset so the section is "clean".
        """
        for k, expected in dirty.orig.items():
            new_value = dirty.get(k, _DeletedOption)
            if new_value is _DeletedOption:
                # The option from orig does not exist anymore
                if k in self.options:
                    self.remove(k)
            else:
                self.set(k, new_value)
        # No need to keep track of the original values anymore
        self.reset_changes()


class Store(object):
    """Abstract interface for option stores."""

    def __init__(self, id=None):
        self.id = id
        self.unload()

    def external_url(self):
        return '{}://'.format(self.id)

    def quote(self, value):
        # We don't support quoting for now
        return value

    def unquote(self, value):
        # We don't support quoting for now
        return value

    def is_loaded(self):
        return self._loaded

    def unload(self):
        self._loaded = False
        self.sections = collections.OrderedDict()
        # Which sections need to be saved (by section id). We use a dict here
        # so the dirty sections can be shared by multiple callers.
        self.dirty_sections = {}

    def _load_from_string(self, text):
        """Create a config store from a string.

        :param text: A unicode string representing the file content.
        """
        if self.is_loaded():
            raise AssertionError('Already loaded')

        # Reset the sections before loading or we may keep sections that are
        # not defined in the new content.
        self.unload()
        parser = parsers.Parser()
        # FIXME: Using self.id rather than self.path below may be risky ? May
        # be external_url() would be better ?  -- vila 2024-10-10
        tokens = parser.parse_config(self.external_url(), text)
        for section in parser.make_sections(tokens):
            self.sections[section.name] = section
        self._loaded = True


class CommandLineStore(Store):
    """A store to carry command line overrides for the config options."""

    readonly_section_class = Section

    def __init__(self):
        super(CommandLineStore, self).__init__()
        # Use an ordered dict to preserve command line order. There is no known
        # use for that so far, except for tests that needs a stable order.
        self.options = collections.OrderedDict()
        self.id = 'cmdline'

    def _reset(self):
        # The dict should be cleared but not replaced so it can be shared.
        self.options.clear()

    def update(self, overrides):
        # Update the options dict in place
        self.options.update(overrides)

    # DEPRECATED in 3.0.2 -- vila 2024-10-10
    def from_cmdline(self, overrides):
        # Reset before accepting new definitions
        self._reset()
        # For compatibility before removal
        as_dict = dict()
        for over in overrides:
            try:
                name, value = over.split('=', 1)
            except ValueError:
                raise errors.InvalidOverrideError(over)
            as_dict[name] = value

        self.update(as_dict)

    def get_sections(self):
        yield self, self.readonly_section_class(None, self.options)

    def save(self, force=False):
        # Nope, we don't do persistence
        pass


class FileStore(Store):
    """A configuration store using a local file storage.

    The file content must be utf8 encoded.

    :cvar readonly_section_class: The class used to create read-only sections.

    :cvar mutable_section_class: The calss used to create mutable sections.
    """

    readonly_section_class = Section
    mutable_section_class = MutableSection

    def __init__(self, path):
        """A Store using a file on disk.

        :param path: The config file path.
        """
        # Daughter classes can use a more specific id
        super(FileStore, self).__init__(id=path)
        self.path = path

    def _load_content(self):
        """Load the config file bytes.

        :return: Unicode string.
        """
        try:
            with io.open(self.path, encoding='utf8') as f:
                return f.read()
        except UnicodeDecodeError:
            raise errors.InvalidContent(self.path)
        except IOError as e:
            if e.errno == errno.EACCES:
                warnings.warn('Permission denied while trying to load'
                              ' configuration store {}.'
                              .format(self.external_url()))
                raise errors.PermissionDenied(self.path)
            elif e.errno in (errno.ENOENT, errno.ENOTDIR):
                raise errors.NoSuchFile(self.path)
            else:
                raise

    def ensure_dir(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            # python2 doesn't provide the exist_ok=True to makedirs
            if e.errno != errno.EEXIST:
                raise

    def _save_content(self, content):
        """Save the config file bytes.

        :param content: Config file unicode string to write
        """
        dir_path = os.path.dirname(self.path)
        if dir_path:
            self.ensure_dir(dir_path)
        with io.open(self.path, 'w', encoding='utf8') as f:
            f.write(content)

    def load(self):
        """Load the store from the associated file.

        This happens as soon as callers access any section.
        """
        if self.is_loaded():
            return
        content = self._load_content()
        self._load_from_string(content)

    def _needs_saving(self):
        for s in self.dirty_sections.values():
            if s.orig:
                # At least one dirty section contains a modification
                return True
        return False

    def apply_changes(self, dirty_sections):
        """Apply changes from dirty sections while checking for coherency.

        The Store content is discarded and reloaded (lazily, later) from
        persistent storage to acquire up-to-date values.

        Dirty sections are MutableSection which kept track of the value they
        are expected to update.

        """
        # We need an up-to-date version from the persistent storage, unload the
        # store. The reload will occur when needed (triggered by the first
        # get_mutable_section() call below.
        self.unload()
        # Apply the changes from the preserved dirty sections
        for section_id, dirty in dirty_sections.items():
            clean = self.get_mutable_section(section_id)
            clean.apply_changes(dirty)
        # Everything is clean now
        self.dirty_sections = {}

    def save(self, force=False):
        """Save the FileStore content on disk.

        :param force: Force the serialization of the existing sections. Default
            is False. When True, this creates the file on disk from the
            existing sections, ignoring the dirty sections. This is mainly
            intended for tests. The known use case is saving the changes
            introduced by a _load_from_string() (this creates the options in a
            way that escapes the usual capture).

        The FileStore serialization is:
        - no name section if it exists,
        - then other sections.

        The order of the sections is either the file content order if it exists
        or the access order from the callers. Sections are filled with the
        *actual* content of the section, ignoring self.dirty_sections if they
        exist.

        """
        # Unless told otherwise (force=True), return early if nothing needs
        # saving.
        if not force:
            if not self._needs_saving():
                return
            # Keep a copy of the current version to work with (dirty_sections
            # are literrally consumed here).
            dirty_sections = dict(self.dirty_sections.items())
            self.apply_changes(dirty_sections)

        # Serialize all sections.
        no_name_section = self.sections.get(None)
        chunks = []
        if no_name_section is not None:
            chunks = [no_name_section.serialize()]
        for section_name in self.sections.keys():
            if section_name is None:
                # Already serialized
                continue
            section = self.sections[section_name]
            chunks.append(section.serialize())
        # saving content (creating the file if needed)
        self._save_content(''.join(chunks))
    # DEPRECATED in 3.0.1 -- vila 2024-10-10
    save_changes = save

    def get_sections(self):
        """Get the sections in the file order.

        :returns: An iterable of (store, section).
        """
        # We need a loaded store
        try:
            self.load()
        except (errors.NoSuchFile, errors.PermissionDenied):
            # If the file can't be read, there is no sections
            return
        for section_name in self.sections.keys():
            yield (self,
                   self.readonly_section_class(section_name,
                                               self.sections[section_name]))

    def get_mutable_section(self, section_id=None):
        # We need a loaded store
        try:
            self.load()
        except errors.NoSuchFile:
            # The file doesn't exist, let's pretend it was empty: no values
            # there
            self._load_from_string('')
        if section_id in self.dirty_sections:
            # We already created a mutable section for this id
            return self.dirty_sections[section_id]
        section = self.sections.get(section_id, None)
        if section is None:
            # Create a new section
            section = parsers.Section(section_id)
            self.sections[section_id] = section
        mutable_section = self.mutable_section_class(section_id, section)
        # All mutable sections can become dirty
        self.dirty_sections[section_id] = mutable_section
        return mutable_section

    def external_url(self):
        return self.path
