from __future__ import print_function
import sys
import ply.lex
import logging
import re
import decimal


if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str


class BaseEdnType(object):
    def __init__(self, name):
        self._name = unicode(name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return repr(self) == repr(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._name)

    def __hash__(self):
        return hash(repr(self))


class Keyword(BaseEdnType):
    def __str__(self):
        return ":{}".format(self._name)


class Symbol(BaseEdnType):
    def __str__(self):
        return self._name


# http://www.dabeaz.com/ply/ply.html
tokens = ('WHITESPACE',
          'CHAR',
          'STRING',
          'NIL',
          'BOOLEAN',
          'INTEGER',
          'FLOAT',
          'SYMBOL',
          'KEYWORD',
          'VECTOR_START',
          'VECTOR_END',
          'LIST_START',
          'LIST_END',
          'MAP_START',
          'SET_START',
          'MAP_OR_SET_END',
          'TAG')

PARTS = {}
PARTS["non_nums"] = r"\w.*+!\-_?$%&=:#<>@"
PARTS["all"] = PARTS["non_nums"] + r"\d"
PARTS["first"] = r"\w*!_?$%&=<>@"
PARTS["special"] = r"\-+."
PARTS["start"] = \
    (r"("
     r"[{first}]"
     r"|"
     r"[{special}]"
     r"[{non_nums}]"
     r"|"
     r"[{special}]"
     r")").format(**PARTS)
SYMBOL = (r"("
          r"{start}"
          r"[{all}]*"
          r"\/"
          r"[{all}]+"
          r"|"
          r"\/"
          r"|"
          r"{start}"
          r"[{all}]*"
          r")").format(**PARTS)
KEYWORD = (r":"
           r"("
           r"[{all}]+"
           r"\/"
           r"[{all}]+"
           r"|"
           r"[{all}]+"
           r")").format(**PARTS)
TAG = (r"\#"
       r"\w"
       r"("
       r"[{all}]*"
       r"\/"
       r"[{all}]+"
       r"|"
       r"[{all}]*"
       r")").format(**PARTS)

t_VECTOR_START = r'\['
t_VECTOR_END = r'\]'
t_LIST_START = r'\('
t_LIST_END = r'\)'
t_MAP_START = r'\{'
t_SET_START = r'\#\{'
t_MAP_OR_SET_END = r'\}'
t_ignore = r"".join([" ", "\t", "\n", ","])


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
    r"(\\\w)"
    t.value = t.value[1]
    return t


def t_STRING(t):
    r'"(.|\"|\t|\n|\r|\newline|\return|\space|\tab)*"'
    t.value = t.value[1:-1]
    t.value = t.value.replace(r"\newline", "\n") \
                     .replace(r"\return", "\r") \
                     .replace(r"\space", " ") \
                     .replace(r"\tab", "\t")
    return t


def t_NIL(t):
    """nil"""
    t.value = None
    return t


def t_BOOLEAN(t):
    r"""(true|false)(?=([\s\])}]|$))"""
    if t.value == "false":
        t.value = False
    elif t.value == "true":
        t.value = True
    return t


def t_FLOAT(t):
    r"""[+-]?\d+\.\d+[M]?([eE][+-]?\d+)?"""
    e_value = 0
    if 'e' in t.value or 'E' in t.value:
        matches = re.search("[eE]([+-]?\d+)$", t.value)
        if matches is None:
            raise SyntaxError("Invalid float : {}".format(t.value))
        e_value = int(matches.group()[1:])
    if t.value.endswith("M"):
        t.value = decimal.Decimal(t.value[:-1]) * pow(1, e_value)
    else:
        t.value = float(t.value) * pow(1, e_value)
    return t


def t_INTEGER(t):
    r"""[+-]?\d+N?"""
    if t.value.endswith("N"):
        t.value = t.value[:-1]
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    r'[;][^\n]*'
    pass  # ignore


def t_DISCARD(t):
    r'\#_\S+\b'
    pass  # ignore


@ply.lex.TOKEN(TAG)
def t_TAG(t):
    t.value = t.value[1:]
    return t


@ply.lex.TOKEN(KEYWORD)
def t_KEYWORD(t):
    t.value = Keyword(t.value[1:])
    return t


@ply.lex.TOKEN(SYMBOL)
def t_SYMBOL(t):
    t.value = Symbol(t.value)
    return t


def t_error(t):
    raise SyntaxError("Illegal character '%s'" % t.value[0])


def lex(text=None):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True, debuglog=logging.getLogger(__name__))
    l = ply.lex.lex(reflags=re.UNICODE, **kwargs)
    if text is not None:
        l.input(text)
    return l
