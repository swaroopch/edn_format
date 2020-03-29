# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# proper unicode escaping
# see http://stackoverflow.com/a/24519338
import codecs
import decimal
import fractions
import logging
import re
import sys


import ply.lex

from .exceptions import EDNDecodeError
from .immutable_dict import ImmutableDict


if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str
    def _bytes(s): return bytes(s, 'utf-8')
else:
    _bytes = bytes


ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


class BaseEdnType(object):
    def __init__(self, name):
        self._name = unicode(name)
        self._type = BaseEdnType

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._name)

    def __hash__(self):
        return ImmutableDict(self.__dict__).__hash__()


class Keyword(BaseEdnType):
    def __init__(self, name):
        super(Keyword, self).__init__(name)
        self._type = Keyword

    def __str__(self):
        return ':{}'.format(self.name)

    @property
    def namespace(self):
        """
        Return the keyword's namespace. This may be ``None``.
        """
        if "/" in self.name:
            return self.name.split("/", 1)[0]

    def with_namespace(self, ns):
        """
        Return a new keyword with the given namespace. Use ``None`` or an empty
        string to remove it:

            >>> Keyword("foo/a").with_namespace("bar")
            Keyword("bar/a")

            >>> Keyword("a").with_namespace("bar")
            Keyword("bar/a")

            >>> Keyword("a/b").with_namespace(None)
            Keyword("b")
        """
        name = self.name
        if "/" in name:
            name = name.split("/", 1)[1]

        if not ns:
            return self.__class__(name)

        return self.__class__("%s/%s" % (ns, name))


class Symbol(BaseEdnType):
    def __init__(self, name):
        super(Symbol, self).__init__(name)
        self._type = Symbol

    def __str__(self):
        return self._name


# http://www.dabeaz.com/ply/ply.html
tokens = ('WHITESPACE',
          'CHAR',
          'STRING',
          'INTEGER',
          'HEX_INTEGER',
          'FLOAT',
          'RATIO',
          'SYMBOL',
          'KEYWORD',
          'VECTOR_START',
          'VECTOR_END',
          'LIST_START',
          'LIST_END',
          'MAP_START',
          'SET_START',
          'MAP_OR_SET_END',
          'TAG',
          'DISCARD_TAG',
          'MAP_NAMESPACE_TAG')

PARTS = {}
PARTS["non_nums"] = r"\w.*+!\-_?$%&=:#<>@"
PARTS["all"] = PARTS["non_nums"] + r"\d"
PARTS["first"] = r"\w*!_?$%&=<>@"
PARTS["special"] = r"\-+."
PARTS["start"] = \
    ("("
     "[{first}]"
     "|"
     "[{special}]"
     "[{non_nums}]"
     "|"
     "[{special}]"
     ")").format(**PARTS)
SYMBOL = ("("
          "{start}"
          "[{all}]*"
          r"\/"
          "[{all}]+"
          "|"
          r"\/"
          "|"
          "{start}"
          "[{all}]*"
          ")").format(**PARTS)
KEYWORD = (":"
           "("
           "[{all}]+"
           r"\/"
           "[{all}]+"
           "|"
           "[{all}]+"
           ")").format(**PARTS)
TAG = (r"\#"
       r"[a-zA-Z]"  # https://github.com/edn-format/edn/issues/30#issuecomment-8540641
       "("
       "[{all}]*"
       r"\/"
       "[{all}]+"
       "|"
       "[{all}]*"
       ")").format(**PARTS)

DISCARD_TAG = r"\#\_"
# https://clojure.org/reference/reader#_maps
MAP_NAMESPACE_TAG = "#:[{all}]+".format(**PARTS)

t_VECTOR_START = r'\['
t_VECTOR_END = r'\]'
t_LIST_START = r'\('
t_LIST_END = r'\)'
t_MAP_START = r'\{'
t_SET_START = r'\#\{'
t_MAP_OR_SET_END = r'\}'
t_ignore = ''.join([" ", "\t", "\n", ","])


def t_WHITESPACE(t):
    r"(\\newline)|(\\return)|(\\space)|(\\tab)"
    if t.value == r"\newline":
        t.value = "\n"
    elif t.value == r"\return":
        t.value = "\r"
    elif t.value == r"\space":
        t.value = " "
    elif t.value == r"\tab":
        t.value = "\t"
    return t


def t_CHAR(t):
    # uXXXX hex code or from "!" to "~" = all printable ASCII chars except the space
    # or unicode word chars
    r"(\\u[0-9A-Fa-f]{4}|\\[!-~\w])"
    t.value = (t.value[1] if len(t.value) == 2 else _bytes(t.value).decode('raw_unicode_escape'))
    return t


def t_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]
    t.value = decode_escapes(t.value)
    return t


def t_FLOAT(t):
    r"""[+-]?\d+(?:(?:\.\d+([eE][+-]?\d+)?|[eE][+-]?\d+)M?|M)"""
    e_value = 0
    if 'e' in t.value or 'E' in t.value:
        matches = re.search(r'[eE]([+-]?\d+)M?$', t.value)
        if matches is None:
            raise EDNDecodeError('Invalid float : {}'.format(t.value))
        e_value = int(matches.group(1))
    if t.value.endswith('M'):
        ctx = decimal.getcontext()
        t.value = decimal.Decimal(t.value[:-1]) * ctx.power(1, e_value)
    else:
        t.value = float(t.value) * pow(1, e_value)
    return t


def t_RATIO(t):
    r"""-?\d+/\d+"""
    numerator, denominator = t.value.split("/", 1)
    t.value = fractions.Fraction(int(numerator), int(denominator))
    return t


def t_INTEGER(t):
    # "No integer other than 0 may begin with 0."
    # https://github.com/edn-format/edn#integers
    r"""[+-]?(?:0(?!x)|[1-9]\d*)N?"""
    if t.value.endswith('N'):
        t.value = t.value[:-1]
    t.value = int(t.value)
    return t


def t_HEX_INTEGER(t):
    r"""[+-]?0x[A-F0-9]+"""
    t.value = int(t.value, 16)
    return t


def t_COMMENT(t):
    r'[;][^\n]*'
    pass  # ignore


@ply.lex.TOKEN(DISCARD_TAG)
def t_DISCARD_TAG(t):
    t.value = t.value[1:]
    return t


@ply.lex.TOKEN(TAG)
def t_TAG(t):
    t.value = t.value[1:]
    return t


@ply.lex.TOKEN(MAP_NAMESPACE_TAG)
def t_MAP_NAMESPACE_TAG(t):
    t.value = t.value[2:]
    return t


@ply.lex.TOKEN(KEYWORD)
def t_KEYWORD(t):
    t.value = Keyword(t.value[1:])
    return t


@ply.lex.TOKEN(SYMBOL)
def t_SYMBOL(t):
    if t.value == "nil":
        t.value = None
    elif t.value == "true":
        t.value = True
    elif t.value == "false":
        t.value = False
    else:
        t.value = Symbol(t.value)
    return t


def t_error(t):
    raise EDNDecodeError(
        "Illegal character '{c}' with lexpos {p} in the area of ...{a}...".format(
            c=t.value[0], p=t.lexpos, a=t.value[0:100]))


def lex(text=None):
    kwargs = {}
    if __debug__:
        kwargs["debug"] = True
        kwargs["debuglog"] = logging.getLogger(__name__)
    lex = ply.lex.lex(reflags=re.UNICODE, **kwargs)
    if text is not None:
        lex.input(text)
    return lex
