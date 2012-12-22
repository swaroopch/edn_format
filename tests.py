
# TODO Handle floats with e, M, minus, plus
# TODO Handle custom tagged element serializer / deserializer
# TODO Handle symbols


import datetime
import pytz

import unittest
import edn_lex
import edn_parse
import edn_format


class ConsoleTest(unittest.TestCase):
    def test_dumping(self):
        is_exception = False
        try:
            edn_format.loads("[1 true nil]")
        except AttributeError as x:
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
        self.check_lex("[LexToken(NUMBER,123,1,0)]",
                       "123")
        self.check_lex("[LexToken(NUMBER,456,1,0), LexToken(NIL,None,1,4), LexToken(BOOLEAN,False,1,8)]",
                       "456 nil false")
        self.check_lex("[LexToken(CHAR,'c',1,0)]",
                       r"\c")
        self.check_lex("[LexToken(KEYWORD,':abc',1,0)]",
                       r":abc")
        self.check_lex("[LexToken(KEYWORD,':+',1,0)]",
                       r":+")
        self.check_lex("[]",
                       "; a comment")
        self.check_lex("[LexToken(KEYWORD,':abc',1,0)]",
                       ":abc ; a comment")
        self.check_lex("[LexToken(TAG,'inst',1,0), LexToken(STRING,'1985-04-12T23:20:50.52Z',1,6)]",
                       '#inst "1985-04-12T23:20:50.52Z"')


    def check_parse(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_parse.parse(actual_input))


    def test_parser(self):
        self.check_parse(1,
                         "1")
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
        self.check_parse(":abc",
                         ":abc")
        self.check_parse([":abc", 1, True, None],
                         "[:abc 1 true nil]")
        self.check_parse((":abc", 1, True, None),
            "(:abc 1 true nil)")
        self.check_parse({":a" : 1, ":b" : 2},
                         "{:a 1 :b 2}")
        self.check_parse({"a" : [1, 2, 3]},
                         '{"a" [1 2 3]}')
        self.check_parse({":a" : 1,
                          "foo" : ":gone",
                          ":bar" : [1, 2, 3]},
                         '{:bar [1 2 3] "foo" :gone :a 1}')
        self.check_parse(datetime.datetime(2012, 12, 22, 19, 40, 18, 0, tzinfo=pytz.utc),
                        '#inst "2012-12-22T19:40:18Z"')


    def check_dump(self, expected_output, actual_input):
        self.assertEqual(expected_output, edn_format.dumps(actual_input))


    def test_dump(self):
        self.check_dump("#{1 2 3}",
                        {1, 2, 3})
        self.check_dump('{:bar [1 2 3] "foo" :gone :a 1}',
                        {":a" : 1,
                         "foo" : ":gone",
                         ":bar" : [1, 2, 3]})


    def test_round_trip_conversion(self):
        EDN_LITERALS = [
            [r"\c", '"c"'],
            ["[ :ghi ]", "[:ghi]"],
            ["[:a #_foo 42]", "[:a 42]"],
            ["123N", "123"],
            ["-123N", "-123"],
            ["+123", "123"],
            ["+123N", "123"],
        ]

        for literal in EDN_LITERALS:
            step1 = literal[0]
            step2 = edn_format.loads(step1)
            step3 = edn_format.dumps(step2)
#            print step1, "->", step2, "->", step3
            self.assertEqual(literal[1], step3)


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
            #"symbol",
            "123",
            "-123",
            #"32.23",
            #"32.23M",
            '["abc"]',
            '[1]',
            '[1 "abc"]',
            '[1 "abc" true]',
            '[:ghi]',
            '(:ghi)',
            '[1 "abc" true :ghi]',
            '(1 "abc" true :ghi)',
            '#{:a :b (1 2 3)}',
            #'#myapp/Person {:first "Fred" :last "Mertz',
            '#inst "1985-04-12T23:20:50Z"',
            '#uuid "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"'
        )

        for literal in EDN_LITERALS:
            step1 = literal
            step2 = edn_format.loads(step1)
            step3 = edn_format.dumps(step2)
#            print step1, "->", step2, "->", step3
            self.assertEqual(step1, step3)