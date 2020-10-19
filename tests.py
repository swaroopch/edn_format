# -*- coding: utf-8 -*-
# TODO: Tests pass on Python 3.6, Disabled to not break tests on 2.7 :-(
# from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
from uuid import uuid4, UUID
import random
import datetime
import fractions
import unittest

import pytz

from edn_format import edn_lex, edn_parse, \
    loads, dumps, Keyword, Symbol, ImmutableDict, ImmutableList, Char, \
    TaggedElement, add_tag, remove_tag, tag, \
    EDNDecodeError


class ConsoleTest(unittest.TestCase):
    def test_dumping(self):
        is_exception = False
        try:
            loads("[1 true nil]")
        except AttributeError:
            is_exception = True
        self.assertFalse(is_exception)


class KeywordTest(unittest.TestCase):
    def test_name(self):
        for name in ("foo", "a/b", "a/b/c", "a:::::::b"):
            self.assertEqual(name, Keyword(name).name)

    def test_namespace(self):
        self.assertIsNone(Keyword("foo").namespace)
        self.assertEqual("a", Keyword("a/b").namespace)
        self.assertEqual("a", Keyword("a/b/d").namespace)

    def test_with_namespace(self):
        for (expected, keyword, namespace) in (
            ("k", "k", None),
            ("k", "n/k", None),
            ("n/k", "k", "n"),
            ("n/k", "x/k", "n"),
            ("n/a/b/c", "x/a/b/c", "n"),
        ):
            self.assertEqual(Keyword(expected),
                             Keyword(keyword).with_namespace(namespace))


class EdnTest(unittest.TestCase):
    def check_lex(self, expected_output, actual_input):
        self.assertEqual(expected_output, str(list(edn_lex.lex(actual_input))))

    def test_lexer(self):
        self.check_lex("[LexToken(SYMBOL,None,1,0)]",
                       "nil")
        self.check_lex("[LexToken(SYMBOL,True,1,0)]",
                       "true")
        self.check_lex("[LexToken(INTEGER,123,1,0)]",
                       "123")
        self.check_lex("[LexToken(HEX_INTEGER,1,1,0)]",
                       "0x1")
        self.check_lex(
            "[LexToken(INTEGER,456,1,0), " +
            "LexToken(SYMBOL,None,1,4), " +
            "LexToken(SYMBOL,False,1,8)]",
            "456 nil false")
        self.check_lex("[LexToken(CHAR,'c',1,0)]",
                       r"\c")
        self.check_lex("[LexToken(KEYWORD,Keyword(abc),1,0)]",
                       r":abc")
        self.check_lex("[LexToken(KEYWORD,Keyword(+),1,0)]",
                       r":+")
        self.check_lex("[]",
                       "; a comment")
        self.check_lex("[LexToken(KEYWORD,Keyword(abc),1,0)]",
                       ":abc ; a comment")
        self.check_lex("[LexToken(TAG,'inst',1,0), " +
                       "LexToken(STRING,'1985-04-12T23:20:50.52Z',1,6)]",
                       '#inst "1985-04-12T23:20:50.52Z"')
        self.check_lex("[LexToken(SYMBOL,Symbol(abc),1,0)]",
                       "abc")
        self.check_lex("[LexToken(SYMBOL,Symbol(?abc),1,0)]",
                       "?abc")
        self.check_lex("[LexToken(SYMBOL,Symbol(/),1,0)]",
                       "/")
        self.check_lex("[LexToken(SYMBOL,Symbol(prefix/name),1,0)]",
                       "prefix/name")
        self.check_lex("[LexToken(SYMBOL,Symbol(true.),1,0)]",
                       "true.")
        self.check_lex("[LexToken(SYMBOL,Symbol(nil.),1,0)]",
                       "nil.")
        self.check_lex("[LexToken(SYMBOL,Symbol($:ABC?),1,0)]",
                       "$:ABC?")
        self.check_lex("[LexToken(MAP_START,'{',1,0), "
                       "LexToken(KEYWORD,Keyword(a),1,2), "
                       "LexToken(SYMBOL,False,1,5), "
                       "LexToken(KEYWORD,Keyword(b),1,12), "
                       "LexToken(SYMBOL,False,1,15), "
                       "LexToken(MAP_OR_SET_END,'}',1,21)]",
                       "{ :a false, :b false }")

        self.check_lex("[LexToken(RATIO,Fraction(2, 3),1,0)]",
                       "2/3")
        self.check_lex("[LexToken(MAP_NAMESPACE_TAG,'a',1,0), "
                       "LexToken(MAP_START,'{',1,3), "
                       "LexToken(MAP_OR_SET_END,'}',1,4)]",
                       "#:a{}")

    def check_parse(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_parse.parse(actual_input),
                         actual_input)

    def check_parse_all(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_parse.parse_all(actual_input),
                         actual_input)

    def check_dumps(self, expected_output, actual_input, **kw):
        self.assertEqual(expected_output, dumps(actual_input, **kw))

    def test_parser_single_expressions(self):
        for expected, edn_string in (
            (1, "1"),
            (16768115, "0xFFDC73"),
            (Symbol("xFF"), "xFF"),
            (Symbol("a*b"), 'a*b'),
            ("ab", '"ab"'),
            ('a"b', r'"a\"b"'),
            ("blah\n", '"blah\n"'),
            ([1, 2, 3], "[1 2 3]"),
            ({1, 2, 3}, "#{1 2 3}"),
            ([1, True, None], "[1 true nil]"),
            (Char("c"), r"\c"),
            (Char("\n"), r"\newline"),
            (Char(u"Σ"), u"\\Σ"),
            (Char(u"λ"), r"\u03bB"),
            (Keyword("abc"), ":abc"),
            ([Keyword("abc"), 1, True, None], "[:abc 1 true nil]"),
            ((Keyword("abc"), 1, True, None), "(:abc 1 true nil)"),
            (tuple(), "()"),
            (set(), "#{}"),
            ({}, "{}"),
            ([], "[]"),
            ({"a": [1, 2, 3]}, '{"a" [1 2 3]}'),
            (datetime.datetime(2012, 12, 22, 19, 40, 18, 0, tzinfo=pytz.utc),
                '#inst "2012-12-22T19:40:18Z"'),
            (datetime.date(2011, 10, 9),
                '#inst "2011-10-09"'),
            ("|", "\"|\""),
            ("%", "\"%\""),
            (['bl"ah'], r"""["bl\"ah"]"""),
            ("blah\n", '"blah\n"'),
            ('"', r'"\""'),
            ('\\', r'"\\"'),
            (["abc", "123"], '["abc", "123"]'),
            ({"key": "value"}, '{"key" "value"}'),
            (frozenset({ImmutableList([u"ab", u"cd"]), ImmutableList([u"ef"])}),
                '#{["ab", "cd"], ["ef"]}'),
            (fractions.Fraction(2, 3), "2/3"),
            ((2, Symbol('/'), 3), "(2 / 3)"),

            ({}, "#:foo{}"),
            ({"a": "b"}, "#:foo{\"a\" \"b\"}"),
            ({Keyword("k"): 42}, "#:foo{:_/k 42}"),
            ({Keyword("bar/k"): 42}, "#:foo{:bar/k 42}"),
            ({Keyword("foo/k"): 42}, "#:foo{:k 42}"),
            ({Keyword("foo/k"): {Keyword("k"): 1}}, "#:foo{:k {:k 1}}"),
        ):
            self.check_parse(expected, edn_string)
            self.check_parse_all([expected], edn_string)

    def test_parser_multiple_expressions(self):
        for expected, edn_string in (
            ([], ""),
            ([], "              ,,,,          ,, ,     "),
            ([1], ",,,,,,,1,,,,,,,,,"),
            ([1, 2], "1 2"),
            ([0, Symbol("x1"), 1], "0 x1 0x1"),
            ([1, 2], "1                    2"),
            ([True, 42, False, Symbol('end')], "true 42 false end"),
            ([Symbol("a*b"), 42], 'a*b 42'),
            ([Char("a"), Char("b"), Char("c")], r"\a \b \c"),
        ):
            self.check_parse_all(expected, edn_string)
            if expected:
                self.check_parse(expected[0], edn_string)

    def check_roundtrip(self, data_input, **kw):
        self.assertEqual(data_input, loads(dumps(data_input, **kw)))

    def check_eof(self, data_input, **kw):
        with self.assertRaises(EDNDecodeError) as ctx:
            loads(data_input, **kw)

        self.assertEqual('EOF Reached', str(ctx.exception))

    def check_mismatched_delimiters(self):
        for bad_string in ("[", "(", "{", "(((((())", '"', '"\\"'):
            self.check_eof(bad_string)

    def test_dump(self):
        self.check_roundtrip({1, 2, 3})
        self.check_roundtrip({1, 2, 3}, sort_sets=True)
        self.check_roundtrip(
            {Keyword("a"): 1,
             "foo": Keyword("gone"),
             Keyword("bar"): [1, 2, 3]})
        self.check_roundtrip(uuid4())
        self.check_roundtrip(datetime.date(1354, 6, 7))
        self.check_roundtrip(datetime.datetime(1900, 6, 7, 23, 59, 59,
                                               tzinfo=pytz.utc))

    def test_proper_unicode_escape(self):
        self.check_roundtrip(u"\"")
        self.check_roundtrip(u'"')
        self.check_roundtrip(u"\\\"")
        self.check_roundtrip(u'\\"')
        self.check_roundtrip(u'\b\f\n\r\t"\\')

    def test_round_trip_conversion(self):
        edn_literals = [
            ["[ :ghi ]", "[:ghi]"],
            ["[:a #_foo 42]", "[:a 42]"],
            ["123N", "123"],
            ["-123N", "-123"],
            ["+123", "123"],
            ["+123N", "123"],
            ["123.2", "123.2"],
            ["+32.23M", "32.23M"],
            ["3.23e10", "32300000000.0"],
            ["3e10", "30000000000.0"],
        ]

        for literal in edn_literals:
            step1 = literal[0]
            step2 = loads(step1)
            step3 = dumps(step2)
            self.assertEqual(literal[1], step3)

    def test_round_trip_sets(self):
        step1 = '#{:a (1 2 3) :b}'
        step2 = loads(step1)
        step3 = dumps(step2)
        step4 = loads(step3)
        self.assertIn(Keyword("a"), step4)
        self.assertIn(Keyword("b"), step4)
        self.assertIn((1, 2, 3), step4)

    def test_round_trip_inst_short(self):
        step1 = '#inst "2011"'
        step2 = loads(step1)
        step3 = dumps(step2)
        step4 = loads(step3)
        self.assertEqual('#inst "2011-01-01"', step3)
        self.assertEqual(datetime.date(2011, 1, 1), step4)

    def test_round_trip_same(self):
        EDN_LITERALS = (
            "nil",
            "true",
            "false",
            '"hello world"',
            ":keyword",
            ":+",
            ":!",
            ":-",
            ":_",
            ":$",
            ":&",
            ":=",
            ":.",
            ":abc/def",
            "symbol",
            "123",
            "-123",
            "32.23",
            "32.23M",
            "-32.23M",
            "32M",
            "-32M",
            "-3.903495E-73M",
            "3.23e-10",
            "3e+20",
            "3E+20M",
            '["abc"]',
            '[1]',
            '[1 "abc"]',
            '[1 "abc" true]',
            '[:ghi]',
            '(:ghi)',
            '[1 "abc" true :ghi]',
            '(1 "abc" true :ghi)',
            '{"a" 2}',
            '#inst "1985-04-12T23:20:50.000000Z"',
            '#inst "2011-10-09"',
            '#uuid "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"',
            '#date "19/07/1984"',
            '#{{"a" 1}}',
            '#{{"a" #{{:b 2}}}}',
            '"|"',
            "/",
            "1/3",
            '"1/3"',
            '"c"',
            r'"\n"',
            r"\c",
            r"\n",
            r"\newline",
            r"\tab",
            r"\uAA0A",
        )

        class TagDate(TaggedElement):
            def __init__(self, value):
                super(TagDate, self).__init__()
                self.name = 'date'
                self.value = datetime.datetime.strptime(
                    value,
                    "%d/%m/%Y").date()

            def __str__(self):
                return '#{} "{}"'.format(
                    self.name,
                    self.value.strftime("%d/%m/%Y"))

        add_tag('date', TagDate)

        for literal in EDN_LITERALS:
            step1 = literal
            step2 = loads(step1)
            step3 = dumps(step2)
            self.assertEqual(step1, step3)

    def check_char(self, expected, name):
        edn_data = "\\{}".format(name)
        parsed = loads(edn_data)
        self.assertIsInstance(parsed, str)
        self.assertEqual(expected, parsed, edn_data)

        self.assertIsInstance(parsed, Char)
        self.assertEqual(Char(expected), parsed, edn_data)

    def test_chars(self):
        # 33-126 = printable ASCII range, except space (code 32)
        for i in range(33, 127):
            ch = chr(i)
            self.check_char(ch, ch)

        for expected, name in (
                (" ", "space"),
                ("\n", "newline"),
                ("\r", "return"),
                ("\t", "tab"),
                (u"\uAA0A", "uAA0A"),
        ):
            self.check_char(expected, name)

    def test_exceptions(self):
        with self.assertRaises(EDNDecodeError):
            loads("{")

    def test_fractions(self):
        for edn_data in (
            '0/1',
            '1/1',
            '1/2',
            '1/3',
            '-5/3',
            '99999999999999999999999999999999999/999999999999999999999999991',
        ):
            self.assertEqual(edn_data, dumps(loads(edn_data)), edn_data)

    def test_keyword_keys(self):
        unchanged = (
            None,
            True,
            1,
            "foo",
            {},
            {True: 42},
            {25: 42},
            {3.14: "test"},
            {Keyword("foo"): "something"},
            {Symbol("foo"): "something"},
            ["foo", "bar"],
            ("foo", "bar"),
            {1: {2: 3}},
            ImmutableDict({1: 2}),
        )

        for case in unchanged:
            self.check_roundtrip(case, keyword_keys=True)

        keyworded_keys = (
            ("{:foo 42}", {"foo": 42}),
            ("{:a {:b {:c 42} :d 1}}", {"a": {"b": {"c": 42}, "d": 1}}),
            ("[{:a 42} {:b 25}]", [{"a": 42}, {"b": 25}]),
            ("({:a 42} {:b 25})", ({"a": 42}, {"b": 25})),
            ("{1 [{:a 42}]}", {1: [{"a": 42}]}),
            ("{:foo 1}", ImmutableDict({"foo": 1})),
        )

        for expected, data in keyworded_keys:
            self.assertEqual(expected, dumps(data, keyword_keys=True))

        self.assertEqual(
                {Keyword("a"): {Keyword("b"): 2}, 3: 4},
                loads(dumps({Keyword("a"): {"b": 2}, 3: 4}, keyword_keys=True)))

    def test_sort_keys(self):
        cases = (
            ('{"a" 4 "b" 5 "c" 3}', OrderedDict([("c", 3), ("b", 5), ("a", 4)])),
            ('{1 0 2 0 "a" 0}', {"a": 0, 1: 0, 2: 0}),
            ('[{"a" 1 "b" 1}]', [OrderedDict([("b", 1), ("a", 1)])]),
        )

        for expected, data in cases:
            self.check_dumps(expected, data, sort_keys=True)

        self.check_dumps('{:a 1 :b 1 :c 1 :d 1}',
                         {"a": 1, "d": 1, "b": 1, "c": 1},
                         sort_keys=True, keyword_keys=True)

    def test_sort_sets(self):
        def misordered_set_sequence():
            """"
            Return a tuple that, if put in a set then iterated over, doesn't
            yield elements in the original order
            """
            while True:
                seq = tuple(random.sample(range(10000), random.randint(2, 8)))
                s = set(seq)
                if tuple(s) != seq:
                    return seq

        for _ in range(10):
            seq = misordered_set_sequence()
            self.check_roundtrip(set(seq))
            self.check_dumps("#{{{}}}".format(" ".join(str(i) for i in sorted(seq))),
                             set(seq),
                             sort_sets=True)

    def test_indent(self):
        fixture = {"foo": "bar"}
        self.check_dumps('{"foo" "bar"}', fixture, indent=None)

        fixture = {Keyword("a"): {Keyword("b"): "foo"}}
        self.check_dumps('''\
{
:a {
:b "foo"
}
}''', fixture, indent=0)

        fixture = (1, Keyword("b"), "foo")
        self.check_dumps('''\
(
 1
 :b
 "foo"
)''', fixture, indent=1)

        fixture = [1, Keyword("b"), "foo", {Keyword("foo"): Keyword("bar")}]
        self.check_dumps('''\
[
  1
  :b
  "foo"
  {
    :foo :bar
  }
]''', fixture, indent=2)

        fixture = {1, 2, 3}
        self.check_dumps('''\
#{
    1
    2
    3
}''', fixture, indent=4, sort_sets=True)

        fixture = [{"a": 42}]
        self.check_dumps('''\
[
  {
    :a 42
  }
]''', fixture, keyword_keys=True, indent=2)

        fixture = [[1, 2, 3]]
        self.check_dumps('''\
[
  [
    1
    2
    3
  ]
]''', fixture, indent=2)

        fixture = {
            "a": "foo",
            "b": {"c": [Keyword("a"), Keyword("b"), Keyword("c")]},
            "d": {1, 2, 3},
            "e": (
                datetime.date(2011, 10, 9),
                UUID("urn:uuid:1e4856a2-085e-45df-93e1-41a0c7aeab2e"),
                datetime.datetime(2012, 12, 22, 19, 40, 18, 0, tzinfo=pytz.utc)
            )
        }
        self.check_dumps('''\
{
  :a "foo"
  :b {
    :c [
      :a
      :b
      :c
    ]
  }
  :d #{
    1
    2
    3
  }
  :e (
    #inst "2011-10-09"
    #uuid "1e4856a2-085e-45df-93e1-41a0c7aeab2e"
    #inst "2012-12-22T19:40:18.000000Z"
  )
}''', fixture, keyword_keys=True, sort_keys=True, sort_sets=True, indent=2)

    def test_discard(self):
        for expected, edn_data in (
            ('[x]', '[x #_ z]'),
            ('[z]', '[#_ x z]'),
            ('[x z]', '[x #_ y z]'),
            ('{1 4}', '{1 #_ 2 #_ 3 4}'),
            ('[1 2]', '[1 #_ [ #_ [ #_ [ #_ [ #_ 42 ] ] ] ] 2 ]'),
            ('[1 2 11]', '[1 2 #_ #_ #_ #_ 4 5 6 #_ 7 #_ #_ 8 9 10 11]'),
            ('()', '(#_(((((((1))))))))'),
            ('[6]', '[#_ #_ #_ #_ #_ 1 2 3 4 5 6]'),
            ('[4]', '[#_ #_ 1 #_ 2 3 4]'),
            ('{:a 1}', '{:a #_:b 1}'),
            ('[42]', '[42 #_ {:a [1 2 3 4] true false 1 #inst "2017"}]'),
            ('#{1}', '#{1 #_foo}'),
            ('"#_ foo"', '"#_ foo"'),
            (r'[\# _]', r'[\#_]'),
            ('[_]', r'[#_\#_]'),
            ('[1]', '[1 #_\n\n42]'),
            ('{}', '{#_ 1}'),
        ):
            self.assertEqual(expected, dumps(loads(edn_data)), edn_data)

    def test_discard_syntax_errors(self):
        for edn_data in ('#_', '#_ #_ 1', '#inst #_ 2017', '[#_]'):
            with self.assertRaises(EDNDecodeError):
                loads(edn_data)

    def test_discard_all(self):
        for edn_data in (
            '42', '-1', 'nil', 'true', 'false', '"foo"', '\\space', '\\a',
            ':foo', ':foo/bar', '[]', '{}', '#{}', '()', '(a)', '(a b)',
            '[a [[[b] c]] 2]', '#inst "2017"',
        ):
            self.assertEqual([1], loads('[1 #_ {}]'.format(edn_data)), edn_data)
            self.assertEqual([1], loads('[#_ {} 1]'.format(edn_data)), edn_data)

            self.assertEqual(None, loads('#_ {}'.format(edn_data)))

            for coll in ('[%s]', '(%s)', '{%s}', '#{%s}'):
                expected = coll % ""
                edn_data = coll % '#_ {}'.format(edn_data)
                self.assertEqual(expected, dumps(loads(edn_data)), edn_data)

    def test_chained_discards(self):
        for expected, edn_data in (
            ('[]', '[#_ 1 #_ 2 #_ 3]'),
            ('[]', '[#_ #_ 1 2 #_ 3]'),
            ('[]', '[#_ #_ #_ 1 2 3]'),
        ):
            self.assertEqual(expected, dumps(loads(edn_data)), edn_data)

    def test_custom_tags(self):
        @tag("dog")
        def parse_dog(name):
            return {
                "kind": "dog",
                "name": name,
                "message": "woof-woof",
            }

        @tag("cat")
        class Cat(TaggedElement):
            def __init__(self, name):
                self.name = name

        dog = loads("#dog \"Max\"")
        self.assertEqual(
                {"kind": "dog", "name": "Max", "message": "woof-woof"}, dog)

        cat = loads("#cat \"Alex\"")
        self.assertIsInstance(cat, Cat)
        self.assertEqual("Alex", cat.name)

        remove_tag("cat")
        self.assertRaises(NotImplementedError, lambda: loads("#cat \"Alex\""))

        add_tag("cat", Cat)
        cat = loads("#cat \"Alex\"")
        self.assertIsInstance(cat, Cat)
        self.assertEqual("Alex", cat.name)


class EdnInstanceTest(unittest.TestCase):
    def test_hashing(self):
        pop_count = len(set(map(hash,
                                ["db/id",
                                 Keyword("db/id"),
                                 Symbol("db/id")])))
        self.assertEqual(pop_count, 3)

    def test_equality(self):
        self.assertTrue("db/id" != Keyword("db/id"))
        self.assertTrue("db/id" != Symbol("db/id"))
        self.assertTrue(Symbol("db/id") != Keyword("db/id"))
        self.assertTrue("db/id" == "db/id")
        self.assertTrue(Keyword("db/id") == Keyword("db/id"))
        self.assertTrue(Symbol("db/id") == Symbol("db/id"))


class ImmutableListTest(unittest.TestCase):
    def test_list(self):
        x = ImmutableList([1, 2, 3])
        self.assertTrue(x == [1, 2, 3])

        self.assertTrue(x.index(1) == 0)
        self.assertTrue(x.count(3) == 1)
        self.assertTrue(x.insert(0, 0) == [0, 1, 2, 3])

        y = ImmutableList([3, 1, 4])
        self.assertTrue(y.sort() == [1, 3, 4])


class CharTest(unittest.TestCase):
    def test_new_ok(self):
        for c in " abc123\x12$*\n\r!\"{":
            self.assertEqual(c, Char(c), c)

    def test_new_fail(self):
        self.assertRaises(AssertionError, lambda: Char("some string"))


if __name__ == "__main__":
    unittest.main()
