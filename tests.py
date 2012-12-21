

import unittest
import edn_format as edn


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


    def test_lexer(self):
        print list(edn.lexer("nil"))
        print list(edn.lexer("true"))
        print list(edn.lexer("123"))
        print list(edn.lexer("456 nil false"))


#    def test_round_trips(self):
#        for literal in self.edn_literals:
#            self.assertEqual(literal, edn.dumps(edn.loads(literal)))