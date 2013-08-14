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
        if isinstance(other, basestring):
            return repr(self) == other
        if not isinstance(other, self.__class__):
            return False
        return repr(self) == repr(other)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._name)

    def __hash__(self):
        return hash(self._name)


class Keyword(BaseEdnType):
    def __str__(self):
        return ":{}".format(self._name)


class Symbol(BaseEdnType):
    def __str__(self):
        return self._name


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


SYMBOL_FIRST_CHAR = r'\w+!\-_$&=\.'
SYMBOL = r"[{0}][{0}\d/]*".format(SYMBOL_FIRST_CHAR)
t_VECTOR_START = '\['
t_VECTOR_END = '\]'
t_LIST_START = '\('
t_LIST_END = '\)'
t_MAP_START = '\{'
t_SET_START = '\#\{'
t_MAP_OR_SET_END = '\}'
t_ignore = "".join([" ", "\t", "\n", ","])


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
    '"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_NIL(t):
    """nil"""
    t.value = None
    return t


def t_BOOLEAN(t):
    r"""(true)|(false)"""
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
    pass # ignore


def t_DISCARD(t):
    r'\#_\S+\b'
    pass # ignore


@ply.lex.TOKEN(r'\#{}'.format(SYMBOL))
def t_TAG(t):
    t.value = t.value[1:]
    return t


@ply.lex.TOKEN(":{}".format(SYMBOL))
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
