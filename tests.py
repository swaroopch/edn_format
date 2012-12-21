

import unittest
import edn_lex
import edn_parse
#import edn_format


class EdnRoundTripTest(unittest.TestCase):
    def setUp(self):
        self.edn_literals = ("nil",
                             "true",
                             "false",
                             r"\c",
                             '"hello world"',
                             ":keyword",
                             "symbol",
                             "123",
                             "123N",
                             "32.23",
                             "32.23M",
                             '(1 "abc" true :ghi)',
                             '[1 "abc" true :ghi]',
                             '{:a 1 "foo" :bar, [1 2 3]}',
                             '#{:a :b [1 2 3]',
                             '#myapp/Person {:first "Fred" :last "Mertz',
                             '#inst "1985-04-12T23:20:50.52Z"',
                             '#uuid "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"')


    def _compare_lexer_output(self, expected_output, actual_input):
        self.assertEqual(expected_output, str(list(edn_lex.lex(actual_input))))


    def test_lexer(self):
        self._compare_lexer_output("[LexToken(NIL,None,1,0)]",
                                   "nil")
        self._compare_lexer_output("[LexToken(BOOLEAN,True,1,0)]",
                                   "true")
        self._compare_lexer_output("[LexToken(NUMBER,123,1,0)]",
                                   "123")
        self._compare_lexer_output("[LexToken(NUMBER,456,1,0), LexToken(NIL,None,1,4), LexToken(BOOLEAN,False,1,8)]",
                                   "456 nil false")


    def _compare_parser_output(self, expected_output, actual_input):
        self.assertEqual(expected_output, str(edn_parse.parse(actual_input)))


    def test_parser(self):
        self._compare_parser_output("1",
                                    "1")
        self._compare_parser_output("[1, 2, 3]",
                                    "[1 2 3]")
        self._compare_parser_output("set([1, 2, 3])",
                                    "#{1 2 3}")
        self._compare_parser_output("[1, True, None]",
                                    "[1 true nil]")


#    def test_round_trips(self):
#        for literal in self.edn_literals:
#            self.assertEqual(literal, edn.dumps(edn.loads(literal)))