# This file is part of Build Your Own Config
#
# Copyright 2018 Vincent Ladeuil
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

import os
import unittest
import warnings


from byoc import (
    errors,
    stores,
    tests,
)
from byot import (
    assertions,
    fixtures,
)


class TestSection(unittest.TestCase):

    def test_get_a_value(self):
        a_dict = dict(foo='bar')
        section = stores.Section('myID', a_dict)
        self.assertEqual('bar', section.get('foo'))

    def test_get_unknown_option(self):
        a_dict = dict()
        section = stores.Section(None, a_dict)
        self.assertEqual('out of thin air',
                         section.get('foo', 'out of thin air'))

    def test_options_is_shared(self):
        a_dict = dict()
        section = stores.Section(None, a_dict)
        self.assertIs(a_dict, section.options)


class TestMutableSection(unittest.TestCase):

    def get_section(self, opts):
        return stores.MutableSection('myID', opts)

    def test_set(self):
        a_dict = dict(foo='bar')
        section = self.get_section(a_dict)
        section.set('foo', 'new_value')
        self.assertEqual('new_value', section.get('foo'))
        # The change appears in the shared section
        self.assertEqual('new_value', a_dict.get('foo'))
        # We keep track of the change
        self.assertTrue('foo' in section.orig)
        self.assertEqual('bar', section.orig.get('foo'))

    def test_set_preserve_original_once(self):
        a_dict = dict(foo='bar')
        section = self.get_section(a_dict)
        section.set('foo', 'first_value')
        section.set('foo', 'second_value')
        # We keep track of the original value
        self.assertTrue('foo' in section.orig)
        self.assertEqual('bar', section.orig.get('foo'))

    def test_remove(self):
        a_dict = dict(foo='bar')
        section = self.get_section(a_dict)
        section.remove('foo')
        # We get None for unknown options via the default value
        self.assertEqual(None, section.get('foo'))
        # Or we just get the default value
        self.assertEqual('unknown', section.get('foo', 'unknown'))
        self.assertFalse('foo' in section.options)
        # We keep track of the deletion
        self.assertTrue('foo' in section.orig)
        self.assertEqual('bar', section.orig.get('foo'))

    def test_remove_new_option(self):
        a_dict = dict()
        section = self.get_section(a_dict)
        section.set('foo', 'bar')
        section.remove('foo')
        self.assertFalse('foo' in section.options)
        # The option didn't exist initially so we need to keep track of it with
        # a special value
        self.assertTrue('foo' in section.orig)
        self.assertEqual(stores._NewlyCreatedOption, section.orig['foo'])


class TestFileStore(unittest.TestCase):

    def get_store(self):
        return stores.FileStore('foo.conf')

    def test_id(self):
        store = self.get_store()
        self.assertIsNot(None, store.id)

    def test_loading_unknown_file_fails(self):
        store = self.get_store()
        with self.assertRaises(errors.NoSuchFile):
            store.load()

    def test_invalid_content(self):
        store = self.get_store()
        self.assertFalse(store.is_loaded())
        with self.assertRaises(errors.InvalidSyntax) as cm:
            store._load_from_string('this is invalid !')
        self.assertEqual('foo.conf(1): Not a section nor an option.',
                         repr(cm.exception))
        # And the load failed
        self.assertFalse(store.is_loaded())


class TestFileStoreReload(unittest.TestCase):

    def get_store(self):
        return stores.FileStore('foo.conf')

    def test_load_twice(self):
        store = self.get_store()
        store._load_from_string('[foo]\na = 1\n')
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        store.unload()
        store._load_from_string('[bar]\na = 1\n')
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)


class TestReadOnlyFileStore(unittest.TestCase):

    def get_store(self):
        return stores.FileStore('foo.conf')

    def test_building_delays_load(self):
        store = self.get_store()
        self.assertEqual(False, store.is_loaded())
        store._load_from_string('')
        self.assertEqual(True, store.is_loaded())

    def test_get_no_sections_for_empty(self):
        store = self.get_store()
        store._load_from_string('')
        self.assertEqual([], list(store.get_sections()))

    def test_get_default_section(self):
        store = self.get_store()
        store._load_from_string('foo=bar')
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        tests.assertSectionContent(self, (None, {'foo': 'bar'}), sections[0])

    def test_get_named_section(self):
        store = self.get_store()
        store._load_from_string('[baz]\nfoo=bar')
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        tests.assertSectionContent(self, ('baz', {'foo': 'bar'}), sections[0])

    def test_load_from_string_fails_for_non_empty_store(self):
        store = self.get_store()
        store._load_from_string('foo=bar')
        self.assertRaises(AssertionError, store._load_from_string, 'bar=baz')


class TestFileStoreContent(unittest.TestCase):
    """Simulate loading a config store with content of various encodings.

    All files produced have an utf8 content.

    Users may modify them manually and end up with a file that can't be
    loaded. We need to issue proper error messages in this case.
    """

    invalid_utf8_char = b'\xff'

    def setUp(self):
        super(TestFileStoreContent, self).setUp()
        fixtures.set_uniq_cwd(self)

    def test_load_utf8(self):
        """Ensure we can load an utf8-encoded file."""
        # Store the raw content in the config file
        with open('foo.conf', 'wb') as f:
            f.write('user=b\N{Euro Sign}ar'.encode('utf8'))
        store = stores.FileStore('foo.conf')
        store.load()
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        s, section = sections[0]
        self.assertIs(store, s)
        self.assertEqual('b\N{Euro Sign}ar', section.get('user'))

    def test_load_non_ascii(self):
        """Ensure we display a proper error on non-ascii, non utf-8 content."""
        with open('foo.conf', 'wb') as f:
            f.write(b'user=foo\n#' + self.invalid_utf8_char + b'\n')
        store = stores.FileStore('foo.conf')
        with self.assertRaises(errors.InvalidContent):
            store.load()

    def test_load_erroneous_content(self):
        """Ensure we display a proper error on content that can't be parsed."""
        with open('foo.conf', 'w') as f:
            f.write('[open_section\n')
        store = stores.FileStore('foo.conf')
        with self.assertRaises(errors.InvalidSyntax):
            store.load()

    def test_load_permission_denied(self):
        """Ensure we get warned when trying to load an inaccessible file."""
        with open('foo.conf', 'w') as f:
            f.write('')
        os.chmod('foo.conf', 0o000)
        self.addCleanup(os.chmod, 'foo.conf', 0o644)
        store = stores.FileStore('foo.conf')
        with warnings.catch_warnings(record=True) as wcm:
            with self.assertRaises(errors.PermissionDenied):
                store.load()
        self.assertEqual('Permission denied while trying to load'
                         ' configuration store foo.conf.',
                         str(wcm[0].message))


class TestMutableStore(unittest.TestCase):

    def setUp(self):
        super(TestMutableStore, self).setUp()
        fixtures.set_uniq_cwd(self)

    def get_store(self, path=None):
        if path is None:
            path = 'foo.conf'
        return stores.FileStore(path)

    def has_store(self, store):
        return os.access(store.path, os.F_OK)

    def assertStoreContent(self, expected, store):
        with open(store.path) as f:
            content = f.read()
        self.assertEqual(expected, content)

    def test_save_empty_creates_no_file(self):
        store = self.get_store()
        store.save()
        self.assertFalse(self.has_store(store))

    def test_save_empty_in_subdir_creates_no_file_nor_dir(self):
        store = self.get_store('dir/foo.conf')
        store.save()
        self.assertFalse(os.path.exists('dir'))
        self.assertFalse(self.has_store(store))

    def test_mutable_section_shared(self):
        store = self.get_store()
        store._load_from_string('foo=bar\n')
        section1 = store.get_mutable_section(None)
        section2 = store.get_mutable_section(None)
        # If we get different sections, different callers won't share the
        # modification
        self.assertIs(section1, section2)

    def test_save_emptied_succeeds(self):
        store = self.get_store()
        store._load_from_string('foo=bar\n')
        section = store.get_mutable_section(None)
        section.remove('foo')
        store.save()
        self.assertTrue(self.has_store(store))
        modified_store = self.get_store()
        sections = list(modified_store.get_sections())
        assertions.assertLength(self, 0, sections)
        self.assertStoreContent('', store)

    def test_save_with_content_succeeds(self):
        store = self.get_store()
        store._load_from_string('foo=bar\n')
        self.assertFalse(self.has_store(store))
        store.save(force=True)
        self.assertTrue(self.has_store(store))
        modified_store = self.get_store()
        sections = list(modified_store.get_sections())
        assertions.assertLength(self, 1, sections)
        tests.assertSectionContent(self, (None, {'foo': 'bar'}), sections[0])
        self.assertStoreContent('foo=bar\n', store)

    def test_save_in_subdir_with_content_succeeds(self):
        store = self.get_store('dir/subdir/foo.conf')
        store._load_from_string('foo=bar\n')
        self.assertFalse(self.has_store(store))
        store.save(force=True)
        self.assertTrue(self.has_store(store))

    def test_set_option_in_default_section(self):
        store = self.get_store()
        section = store.get_mutable_section(None)
        section.set('foo', 'bar')
        store.save()
        modified_store = self.get_store()
        sections = list(modified_store.get_sections())
        assertions.assertLength(self, 1, sections)
        tests.assertSectionContent(self, (None, {'foo': 'bar'}), sections[0])
        self.assertStoreContent('foo = bar\n', store)

    def test_set_option_in_named_section(self):
        store = self.get_store()
        store._load_from_string('')
        section = store.get_mutable_section('baz')
        section.set('foo', 'bar')
        store.save()
        modified_store = self.get_store()
        sections = list(modified_store.get_sections())
        assertions.assertLength(self, 1, sections)
        self.assertStoreContent('[baz]\nfoo = bar\n', store)

    def test_no_name_stays_first(self):
        store = self.get_store()
        store._load_from_string('[baz]\nfoo = bar\n')
        store.save(force=True)
        section = store.get_mutable_section(None)
        section.set('foo', 'foo')
        store.save()
        modified_store = self.get_store()
        sections = list(modified_store.get_sections())
        assertions.assertLength(self, 2, sections)
        self.assertStoreContent('foo = foo\n[baz]\nfoo = bar\n', store)


class TestRoundTripping(unittest.TestCase):

    def setUp(self):
        super(TestRoundTripping, self).setUp()
        fixtures.set_uniq_cwd(self)
        self.store = stores.FileStore('foo.conf')

    def assertRoundTrip(self, content):
        self.store._load_from_string(content)
        self.store.save(force=True)
        with open(self.store.path) as f:
            new_content = f.read()
        assertions.assertMultiLineAlmostEqual(self, content, new_content)

    def test_raw(self):
        self.assertRoundTrip('''\
a = b
[s1]
c = d
[s2]
e = x
f =
''')

    def test_with_comments(self):
        self.assertRoundTrip('''\
# Initial comment
a = b # And a comment
f =
# section comment
[src] # another section comment
c = d
''')

    def test_orphan_leading_comment(self):
        self.assertRoundTrip('''# leading comment
''')

    def test_orphan_leading_comment_with_empty_line(self):
        self.assertRoundTrip('''
# leading comment
''')


class TestCmdlineStore(unittest.TestCase):

    # DEPRECATED in 3.0.2 -- vila 2024-10-27
    def test_from_cmdline(self):
        store = stores.CommandLineStore()
        store.from_cmdline(['foo=bar', 'baz=qux'])
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        opts = sections[0][1]
        self.assertEqual('bar', opts.get('foo'))
        self.assertEqual('qux', opts.get('baz'))

    def test_valid_overrides(self):
        store = stores.CommandLineStore()
        store.update({'foo': 'bar', 'baz': 'qux'})
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        opts = sections[0][1]
        self.assertEqual('bar', opts.get('foo'))
        self.assertEqual('qux', opts.get('baz'))

    def test_last_override_prevails(self):
        store = stores.CommandLineStore()
        store.update({'foo': 'bar', 'baz': 'qux'})
        store.update({'foo': 'quux'})
        sections = list(store.get_sections())
        assertions.assertLength(self, 1, sections)
        opts = sections[0][1]
        self.assertEqual('quux', opts.get('foo'))
        self.assertEqual('qux', opts.get('baz'))
