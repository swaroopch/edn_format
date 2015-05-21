from __future__ import print_function
import sys
import ply.lex
import logging
import re
import decimal
from .immutable_dict import ImmutableDict


if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str

# proper unicode escaping
# see http://stackoverflow.com/a/24519338
import re
import codecs

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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return u'{}({})'.format(self.__class__.__name__, self._name)

    def __hash__(self):
        return ImmutableDict(self.__dict__).__hash__()


class Keyword(BaseEdnType):
    def __init__(self, name):
        self._name = unicode(name)
        self._type = Keyword

    @property
    def name(self):
        return self._name

    def __str__(self):
        return u':{}'.format(self._name)


class Symbol(BaseEdnType):
    def __init__(self, name):
        self._name = unicode(name)
        self._type = Symbol

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
PARTS["non_nums"] = ur"\w.*+!\-_?$%&=:#<>@"
PARTS["all"] = PARTS["non_nums"] + ur"\d"
PARTS["first"] = ur"\w*!_?$%&=<>@"
PARTS["special"] = ur"\-+."
PARTS["start"] = \
    (u"("
     u"[{first}]"
     u"|"
     u"[{special}]"
     u"[{non_nums}]"
     u"|"
     u"[{special}]"
     u")").format(**PARTS)
SYMBOL = (u"("
          u"{start}"
          u"[{all}]*"
          ur"\/"
          u"[{all}]+"
          u"|"
          ur"\/"
          u"|"
          u"{start}"
          u"[{all}]*"
          u")").format(**PARTS)
KEYWORD = (u":"
           u"("
           u"[{all}]+"
           ur"\/"
           u"[{all}]+"
           u"|"
           u"[{all}]+"
           u")").format(**PARTS)
TAG = (ur"\#"
       ur"\w"
       u"("
       u"[{all}]*"
       ur"\/"
       u"[{all}]+"
       u"|"
       u"[{all}]*"
       u")").format(**PARTS)

t_VECTOR_START = ur'\['
t_VECTOR_END = ur'\]'
t_LIST_START = ur'\('
t_LIST_END = ur'\)'
t_MAP_START = ur'\{'
t_SET_START = ur'\#\{'
t_MAP_OR_SET_END = ur'\}'
t_ignore = u''.join([u" ", u"\t", u"\n", u","])


def t_WHITESPACE(t):
    ur"(\\newline)|(\\return)|(\\space)|(\\tab)"
    if t.value == ur"\newline":
        t.value = u"\n"
    elif t.value == ur"\return":
        t.value = u"\r"
    elif t.value == ur"\space":
        t.value = u" "
    elif t.value == ur"\tab":
        t.value = u"\t"
    return t


def t_CHAR(t):
    ur"(\\\w)"
    t.value = t.value[1]
    return t

def t_STRING(t):
    ur'"([^"\\]*(\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]
    t.value = decode_escapes(t.value)
    return t

def t_NIL(t):
    """nil"""
    t.value = None
    return t


def t_BOOLEAN(t):
    ur"""(true|false)(?=([,\s\])}]|$))"""
    if t.value == u"false":
        t.value = False
    elif t.value == u"true":
        t.value = True
    return t


def t_FLOAT(t):
    ur"""[+-]?\d+\.\d+[M]?([eE][+-]?\d+)?"""
    e_value = 0
    if u'e' in t.value or u'E' in t.value:
        matches = re.search(u"[eE]([+-]?\d+)$", t.value)
        if matches is None:
            raise SyntaxError(u"Invalid float : {}".format(t.value))
        e_value = int(matches.group()[1:])
    if t.value.endswith(u"M"):
        t.value = decimal.Decimal(t.value[:-1]) * pow(1, e_value)
    else:
        t.value = float(t.value) * pow(1, e_value)
    return t


def t_INTEGER(t):
    ur"""[+-]?\d+N?"""
    if t.value.endswith(u"N"):
        t.value = t.value[:-1]
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    ur'[;][^\n]*'
    pass  # ignore


def t_DISCARD(t):
    ur'\#_\S+\b'
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
    raise SyntaxError(
        u"Illegal character '{c}' with lexpos {p} in the area of ...{a}...".format(
            c=t.value[0], p=t.lexpos, a=t.value[0:100]))


def lex(text=None):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True, debuglog=logging.getLogger(__name__))
    l = ply.lex.lex(reflags=re.UNICODE, **kwargs)
    if text is not None:
        l.input(text)
    return l
