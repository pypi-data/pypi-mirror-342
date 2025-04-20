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

import collections
import re


from byoc import errors


class Definition(object):

    def __init__(self, pre_comment, post_comment, line):
        self.pre_comment = pre_comment
        self.post_comment = post_comment
        self.line = line

    def __eq__(self, other):
        return (self.pre_comment == other.pre_comment and
                self.post_comment == other.post_comment)


class OptionDefinition(Definition):

    def __init__(self, key, value, pre=None, post=None, line=None):
        super(OptionDefinition, self).__init__(pre, post, line)
        self.key = key
        self.value = value

    def __eq__(self, other):
        return (self.key == other.key and
                self.value == other.value and
                super(OptionDefinition, self).__eq__(other))

    def __repr__(self):
        pre = self.pre_comment or ''
        post = self.post_comment or ''
        return pre + self.value + post


class SectionDefinition(Definition):

    def __init__(self, name, pre=None, post=None, line=None):
        super(SectionDefinition, self).__init__(pre, post, line)
        self.name = name

    def __eq__(self, other):
        return (self.name == other.name and
                super(SectionDefinition, self).__eq__(other))

    def __repr__(self):
        s = ''
        if self.pre_comment:
            s = s + self.pre_comment
        if self.name is not None:
            s = s + '[' + self.name + ']'
        if self.post_comment:
            s = s + self.post_comment
        return s


class Section(collections.OrderedDict):
    """A section holding options with their associated value and comments.

    This allows serializing configuration files where users can add comments
    and keep them when the configuration file is updated.
    """
    def __init__(self, name, pre=None, post=None):
        super(Section, self).__init__()
        self.name = name
        # The section comments
        self.pre_comment = pre
        self.post_comment = post
        # The option comments. They are handled separatly from the values since
        # relying on the key is enough (renaming options is not a feature ;)
        self.pre = {}
        self.post = {}

    def add(self, key, value, pre=None, post=None):
        """Add a new option.

        :param key: The option name.

        :param value: The option value.

        :param pre: The preceding comment.

        :param post: The comment following the value up to the end of the line
            where it is defined.
        """
        self[key] = value
        self.pre[key] = pre
        self.post[key] = post

    def serialize(self):
        """Serialize the section with the comments.

        :return: The serialized unicode text.
        """
        def get_pre(key):
            pre = self.pre.get(key)
            if not pre:
                # This is mainly encountered when serializing a section that
                # has been created in memory (as opposed to from disk), this a
                # very common in tests but can also happen in real life
                # (existing-vms.conf for example). The parser puts the '=' sign
                # in the pre comment but there is little interest in forcing
                # that chore on callers so we just do it here and now.
                pre = '{} = '.format(key)
            return pre

        chunks = []
        chunks.append(self.pre_comment or '')
        if self.name is not None:
            chunks.extend(['[', self.name, ']'])
            chunks.append(self.post_comment or '\n')
        for key, value in self.items():
            chunks.extend([get_pre(key), value,
                           self.post.get(key) or '\n'])
        # FIXME: Provide a way to activate the breakpoint below for tests or
        # just fix it ?  -- vila 2022-05-13

        # Help debug cases leading to None ending as an option value (rather
        # than a valid utf8 string)

        # if None in chunks:
        #     print('Chunks: {}'.format(chunks))
        #     breakpoint()
        return ''.join(chunks)


class Parser(object):
    """Parse a config file.

    A config file is made of lines (or is empty).

    A line is either empty, a comment, a section definition or an option
    definition.

    A comment starts with '#' and ends at the end of the line.

    A section definition is a string enclosed in square brackets at the
    beginning of a line.

    An option definition is the option name, followed by the equal sign,
    followed by the value. Spaces are allowed between them but are not part of
    the value nor the name.

    All comments and end of lines are collected and serializing the config
    again respect the order in the file and the formatting (only the options
    values are updated). Any other change (renaming options or sections,
    re-ordering options) are better achieved with a text editor.

    """

    blank_line_re = re.compile(r'[ \t\r\f\v]*\n')
    comment_re = re.compile(r'([ \t\r\f\v]*#.*\n)')
    section_header_re = re.compile(r'\[([^]]*)\]')

    def __init__(self):
        self.path = None
        self.line = None

    def parse_config(self, path, text):
        """Parse a text containing sections, options and comments.

        :param path: The path where the text is coming from (used for error
            reporting).

        :param text: The unicode string to parse.

        :return: A list of section and option definitions.
        """
        self.path = path
        section_line = self.line = 1
        tokens = []
        rest = text
        eol_at_eof = False
        if not text.endswith('\n'):
            # We'll get rid of it for serialization but this makes parsing way
            # simpler
            rest += '\n'
            eol_at_eof = True
        while rest:
            rest, pre = self.collect_pre_comments(rest)
            if not rest:
                break
            section = self.section_header_re.match(rest)
            if section:
                section_line = self.line
                name = section.group(1)
                if name == '':
                    raise errors.SectionEmptyName(self.path, self.line)
                rest = rest[section.end():]
                rest, post = self.collect_post_comments(rest)
                tokens.append(SectionDefinition(name, pre, post,
                                                line=section_line))
                continue
            rest, option = self.parse_option(rest, pre)
            if option:
                if not tokens:
                    # Implicit None section.
                    tokens.append(SectionDefinition(None))
                tokens.append(option)
                continue

            raise errors.InvalidSyntax(self.path, self.line)
        if not tokens and pre:
            if eol_at_eof:
                self.line -= 1
                pre = pre[:-1]
            if pre:
                # Attach the comment to the empty section
                tokens.append(SectionDefinition(None, pre, None,
                                                line=section_line))
        elif eol_at_eof:
            self.line -= 1
            token = tokens[-1]
            token.post_comment = token.post_comment[:-1]

        return tokens

    def collect_pre_comments(self, rest):
        """Collect comments before a section or an option."""
        pre = []  # Pre-comments: empty or blank or '#'-prefixed lines
        while rest:
            # Comments are collected until sections or options gather them.
            pre_com = self.blank_line_re.match(rest)
            if pre_com is None:
                pre_com = self.comment_re.match(rest)
            if pre_com is None:
                break
            else:
                # We've got a (possibly empty) comment including \n
                pre.append(pre_com.group())
                rest = rest[pre_com.end():]
                self.line += 1
        return rest, ''.join(pre)

    def collect_post_comments(self, rest):
        """Collect comments after a section or an option."""
        post = self.blank_line_re.match(rest)
        if post is None:
            post = self.comment_re.match(rest)
        if post:
            rest = rest[post.end():]
            post = post.group()
            self.line += 1
        if post is None:
            post = ''
        return rest, post

    option_re = re.compile(r'([ \t\r\f\v]*)'  # Ignore leading space
                           '([a-zA-Z_][a-zA-Z0-9_.]*)'  # option name
                           r'(\s*=[ \t\r\f\v]*)'  # equal sign
                           '([^#\n\t\r\f\v]*)')  # value (spaces allowed)

    def parse_option(self, rest, pre):
        # To keep the regexp ~simple, we allow spaces and remove the trailing
        # ones after the fact.
        option = self.option_re.match(rest)
        if not option:
            return rest, None
        line = self.line
        comment, name, equal, value = option.groups()
        # Renaming option is not allowed so, for serialization, we
        # include the name and the equal in the comment.
        pre = ''.join([pre, comment, name, equal])
        end = option.end()
        # Remove the trailing spaces
        while value.endswith(' '):
            value = value[:-1]
            end -= 1
        rest = rest[end:]
        rest, post = self.collect_post_comments(rest)
        option = OptionDefinition(name, value, pre, post, line=line)
        return rest, option

    def make_sections(self, tokens):
        """Yields the sections built from the received tokens.

        :param tokens: An iterable of tokens as returned by 'parse_config'.

        :yield: A Section object as soon as one is complete.
        """
        sections = {}
        options = {}
        cur = None
        for token in tokens:
            if isinstance(token, SectionDefinition):
                if cur is not None:
                    yield cur
                cur = Section(token.name,
                              token.pre_comment, token.post_comment)
                options = {}
                existing = sections.get(token.name)
                if existing is not None:
                    raise errors.DuplicateSection(
                        self.path, token.line,
                        name=token.name, previous=existing)
                sections[token.name] = token.line
            else:
                existing = options.get(token.key)
                if existing is not None:
                    raise errors.DuplicateOption(
                        self.path, token.line,
                        name=token.key, previous=existing)
                options[token.key] = token.line
                cur.add(token.key, token.value,
                        token.pre_comment, token.post_comment)
        if cur is not None:
            yield cur
