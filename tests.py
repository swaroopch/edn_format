# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
from uuid import uuid4
import datetime
import unittest

import pytz

from edn_format import edn_lex, edn_parse, \
    loads, dumps, Keyword, Symbol, TaggedElement, ImmutableDict, add_tag


class ConsoleTest(unittest.TestCase):
    def test_dumping(self):
        is_exception = False
        try:
            loads("[1 true nil]")
        except AttributeError:
            is_exception = True
        self.assertFalse(is_exception)


class EdnTest(unittest.TestCase):
    def check_lex(self, expected_output, actual_input):
        self.assertEqual(expected_output, str(list(edn_lex.lex(actual_input))))

    def test_lexer(self):
        self.check_lex("[LexToken(NIL,None,1,0)]",
                       "nil")
        self.check_lex("[LexToken(BOOLEAN,True,1,0)]",
                       "true")
        self.check_lex("[LexToken(INTEGER,123,1,0)]",
                       "123")
        self.check_lex(
            "[LexToken(INTEGER,456,1,0), " +
            "LexToken(NIL,None,1,4), " +
            "LexToken(BOOLEAN,False,1,8)]",
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
        self.check_lex("[LexToken(SYMBOL,Symbol($:ABC?),1,0)]",
                       "$:ABC?")
        self.check_lex("[LexToken(MAP_START,'{',1,0), "
                       "LexToken(KEYWORD,Keyword(a),1,2), "
                       "LexToken(BOOLEAN,False,1,5), "
                       "LexToken(KEYWORD,Keyword(b),1,12), "
                       "LexToken(BOOLEAN,False,1,15), "
                       "LexToken(MAP_OR_SET_END,'}',1,21)]",
                       "{ :a false, :b false }")

    def check_parse(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_parse.parse(actual_input))

    def check_dumps(self, expected_output, actual_input, **kw):
        self.assertEqual(expected_output, dumps(actual_input, **kw))

    def test_parser(self):
        self.check_parse(1,
                         "1")
        self.check_parse(Symbol("a*b"),
                         'a*b')
        self.check_parse("ab",
                         '"ab"')
        self.check_parse('a"b',
                         r'"a\"b"')
        self.check_parse("blah\n",
                         '"blah\n"')
        self.check_parse([1, 2, 3],
                         "[1 2 3]")
        self.check_parse({1, 2, 3},
                         "#{1 2 3}")
        self.check_parse([1, True, None],
                         "[1 true nil]")
        self.check_parse("c",
                         r"\c")
        self.check_parse("\n",
                         r"\newline")
        self.check_parse(Keyword("abc"),
                         ":abc")
        self.check_parse([Keyword("abc"), 1, True, None],
                         "[:abc 1 true nil]")
        self.check_parse((Keyword("abc"), 1, True, None),
                         "(:abc 1 true nil)")
        self.check_parse(tuple(), "()")
        self.check_parse(set(), "#{}")
        self.check_parse({}, "{}")
        self.check_parse([], "[]")
        self.check_parse({"a": [1, 2, 3]},
                         '{"a" [1 2 3]}')
        self.check_parse(datetime.datetime(2012, 12, 22, 19, 40, 18, 0,
                                           tzinfo=pytz.utc),
                         '#inst "2012-12-22T19:40:18Z"')
        self.check_parse(datetime.date(2011, 10, 9),
                         '#inst "2011-10-09"')
        self.check_parse("|", "\"|\"")
        self.check_parse("%", "\"%\"")
        self.check_parse(['bl"ah'], r"""["bl\"ah"]""")
        self.check_parse("blah\n", '"blah\n"')
        self.check_parse('"', r'"\""')
        self.check_parse('\\', r'"\\"')
        self.check_parse(["abc", "123"], '["abc", "123"]')
        self.check_parse({"key": "value"}, '{"key" "value"}')

    def check_roundtrip(self, data_input, **kw):
        self.assertEqual(data_input, loads(dumps(data_input, **kw)))

    def test_dump(self):
        self.check_roundtrip({1, 2, 3})
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
        EDN_LITERALS = [
            [r"\c", '"c"'],
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

        for literal in EDN_LITERALS:
            step1 = literal[0]
            step2 = loads(step1)
            step3 = dumps(step2)
            if isinstance(literal[1], list):
                self.assertIn(step3, literal[1])
            else:
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
            '"|"'
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


if __name__ == "__main__":
    unittest.main()
