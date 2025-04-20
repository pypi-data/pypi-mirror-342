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

import sys
import unittest

from byot import assertions

from byoc import (
    errors,
    parsers,
)

if sys.version_info >= (3,):
    unicode = str


# Some aliases to make tests shorter
SD = parsers.SectionDefinition
OD = parsers.OptionDefinition


def assertTokens(test, expected, to_parse):
    actual = test.parser.parse_config('<string>', to_parse)
    test.assertEqual(
        expected, actual,
        '\n[{}]\n differs from\n[{}]'.format([e.__dict__ for e in expected],
                                             [a.__dict__ for a in actual]))


class TestParseConfigEdgeCases(unittest.TestCase):

    def setUp(self):
        super(TestParseConfigEdgeCases, self).setUp()
        self.parser = parsers.Parser()

    def test_empty(self):
        assertTokens(self, [], '')

    def test_almost_empty(self):
        blank_noise = ' \n   \n\n   \n   '
        assertTokens(self, [SD(None, blank_noise, None)], blank_noise)

    def test_leading_comment(self):
        assertTokens(self, [SD(None, '# leading comment\n', None)],
                     '''\
# leading comment
''')

    def test_section_and_end_comment(self):
        assertTokens(self, [SD('section', '', '  ')],
                     '''[section]  ''')

    def test_option_and_end_comment(self):
        assertTokens(self, [SD(None), OD('a', 'b', 'a= ', '  ')],
                     '''a= b  ''')
        assertTokens(self, [SD(None), OD('a', 'b', 'a= ', ' # Good ')],
                     '''a= b # Good ''')

    def test_invalid(self):
        with self.assertRaises(errors.InvalidSyntax):
            self.parser.parse_config('<string>', 'whatever')


class TestOptions(unittest.TestCase):

    def setUp(self):
        super(TestOptions, self).setUp()
        self.parser = parsers.Parser()

    def test_simple_value(self):
        assertTokens(self, [SD(None), OD('a', 'b', 'a=', '')], 'a=b')
        self.assertEqual(1, self.parser.line)

    def test_simple_value_stripping_spaces(self):
        assertTokens(self, [SD(None), OD('a', 'b', ' a = ', ' ')], ' a = b ')
        self.assertEqual(1, self.parser.line)

    def test_empty_value(self):
        assertTokens(self, [SD(None), OD('a', '', 'a=', '')], 'a=')
        self.assertEqual(1, self.parser.line)

    def test_newline_is_empty_value(self):
        assertTokens(self, [SD(None), OD('a', '', 'a=', '\n')], 'a=\n')
        self.assertEqual(2, self.parser.line)

    def test_empty_value_with_spaces(self):
        assertTokens(self, [SD(None), OD('a', '', 'a=  \t\t\r\r\f\f\v\v', '')],
                     'a=  \t\t\r\r\f\f\v\v')
        self.assertEqual(1, self.parser.line)

    def test_newline_and_spaces_is_empty_value(self):
        assertTokens(self, [SD(None),
                            OD('a', '', 'a=  \t\t\r\r\f\f\v\v', '\n')],
                     'a=  \t\t\r\r\f\f\v\v\n')
        self.assertEqual(2, self.parser.line)

    def test_empty_value_with_following_options(self):
        assertTokens(self, [SD(None), OD('a', '', 'a=', post='\n'),
                            OD('b', 'b', 'b=', post='')],
                     'a=\nb=b')
        self.assertEqual(2, self.parser.line)

    def test_pre_comment(self):
        assertTokens(self, [SD(None), OD('a', 'b', '# Define a\na=', '')],
                     '# Define a\na=b')
        self.assertEqual(2, self.parser.line)

    def test_post_comment(self):
        # The comment collects even the preceding spaces as they are not part
        # of the value
        assertTokens(self, [SD(None), OD('a', 'b', 'a=', ' # b is good\n')],
                     'a=b # b is good\n')
        self.assertEqual(2, self.parser.line)

    def test_outer_spaces(self):
        assertTokens(self, [SD(None), OD('a', 'b', 'a\t=\t  ', '  \t ')],
                     'a\t=\t  b  \t ')
        self.assertEqual(1, self.parser.line)

    def test_embedded_spaces(self):
        assertTokens(self, [SD(None), OD('a', 'b  x', 'a= ', '')],
                     'a= b  x')
        self.assertEqual(1, self.parser.line)

    def test_several_options(self):
        assertTokens(self, [SD(None),
                            OD('a', 'b', 'a=', '\n'),
                            OD('c', 'd', '# c now\nc=', ' # c is better\n')],
                     'a=b\n# c now\nc=d # c is better\n')
        self.assertEqual(4, self.parser.line)


class TestParseSections(unittest.TestCase):

    def setUp(self):
        super(TestParseSections, self).setUp()
        self.parser = parsers.Parser()

    def test_empty_section(self):
        assertTokens(self, [SD('s', '', '')], '[s]')
        self.assertEqual(1, self.parser.line)

    def test_empty_section_name(self):
        with self.assertRaises(errors.SectionEmptyName):
            self.parser.parse_config('<string>', '[]')

    def test_pre_comment(self):
        assertTokens(self, [SD('s', '  # Empty section\n', '')],
                     '  # Empty section\n[s]')
        self.assertEqual(2, self.parser.line)

    def test_post_comment(self):
        assertTokens(self, [SD('s', '', ' # It is empty\n')],
                     '[s] # It is empty\n')
        self.assertEqual(2, self.parser.line)


class TestSerializeSection(unittest.TestCase):

    def test_serialize_empty(self):
        sect = parsers.Section(None)
        self.assertEqual('', sect.serialize())

    def test_single_option(self):
        sect = parsers.Section(None)
        sect.add('foo', 'bar', '# This is foo\nfoo = ', ' # Set to bar\n')
        self.assertEqual('''# This is foo
foo = bar # Set to bar
''',
                         sect.serialize())

    def test_single_option_in_named_section(self):
        sect = parsers.Section('sect', '# This is sect\n # A simple section\n',
                               ' # Just saying\n')
        sect.add('foo', 'bar', '# This is foo\nfoo = ', ' # Set to bar\n')
        self.assertEqual('''# This is sect
 # A simple section
[sect] # Just saying
# This is foo
foo = bar # Set to bar
''',
                         sect.serialize())

    def test_several_options(self):
        sect = parsers.Section(None)
        sect.add('foo', 'bar', '# This is foo\nfoo = ', ' # Set to bar\n')
        sect.add('baz', 'qux', '# This is baz\nbaz = ', ' # Set to qux\n')
        self.assertEqual('''# This is foo
foo = bar # Set to bar
# This is baz
baz = qux # Set to qux
''',
                         sect.serialize())


class TestModifiedSectionSerialization(unittest.TestCase):

    def setUp(self):
        super(TestModifiedSectionSerialization, self).setUp()
        sect = parsers.Section(None)
        sect.add('b', '1', '# Define b\nb = ', ' # set to 1\n')
        sect.add('a', '2', '# Define a\na = ', ' # set to 2\n')
        sect.add('z', '3', '# Define z\nz = ', ' # set to 3\n')
        self.section = sect

    def test_added_option(self):
        self.section.add('foo', 'bar')
        self.assertEqual('''# Define b
b = 1 # set to 1
# Define a
a = 2 # set to 2
# Define z
z = 3 # set to 3
foo = bar
''',
                         self.section.serialize())

    def test_modified_option(self):
        self.section['a'] = '42'
        self.assertEqual('''# Define b
b = 1 # set to 1
# Define a
a = 42 # set to 2
# Define z
z = 3 # set to 3
''',
                         self.section.serialize())

    def test_deleted_option(self):
        del self.section['a']
        self.assertEqual('''# Define b
b = 1 # set to 1
# Define z
z = 3 # set to 3
''',
                         self.section.serialize())


class TestMakeSections(unittest.TestCase):

    def setUp(self):
        super(TestMakeSections, self).setUp()
        self.parser = parsers.Parser()

    def test_empty(self):
        self.assertEqual([], list(self.parser.make_sections([])))

    def test_single_section(self):
        defs = [SD(None), OD('a', 'b', None, ' # b is good\n')]
        sections = list(self.parser.make_sections(defs))
        assertions.assertLength(self, 1, sections)
        section = sections[0]
        self.assertEqual('b', section['a'])

    def test_several_sections(self):
        defs = [SD('s1'), OD('a', 'b', None, ' # b is good\n'),
                SD('s2'), OD('c', 'd'), OD('foo', 'bar')]
        sections = list(self.parser.make_sections(defs))
        assertions.assertLength(self, 2, sections)
        s1, s2 = sections
        self.assertEqual('b', s1['a'])
        self.assertEqual('d', s2['c'])
        self.assertEqual('bar', s2['foo'])

    def test_duplicate_section(self):
        defs = [SD('s1', line=1), SD('s1', line=2)]
        with self.assertRaises(errors.DuplicateSection) as cm:
            list(self.parser.make_sections(defs))
        self.assertEqual(2, cm.exception.line)
        self.assertEqual(1, cm.exception.previous)
        self.assertEqual('None(2): Section s1 already defined at line 1.',
                         unicode(cm.exception))

    def test_duplicate_option(self):
        defs = [SD(None), OD('a', 'b', line=1), OD('a', 'c', line=2)]
        with self.assertRaises(errors.DuplicateOption) as cm:
            list(self.parser.make_sections(defs))
        self.assertEqual(2, cm.exception.line)
        self.assertEqual(1, cm.exception.previous)
        self.assertEqual('None(2): Option a already defined at line 1.',
                         unicode(cm.exception))
