
import re
import logging
import ply.lex


tokens = ('WHITESPACE',
          'CHAR',
          'STRING',
          'NIL',
          'BOOLEAN',
          'NUMBER',
#          'SYMBOL',
          'KEYWORD',
          'VECTOR_START',
          'VECTOR_END',
          'LIST_START',
          'LIST_END',
          'MAP_START',
          'SET_START',
          'MAP_OR_SET_END')


SYMBOL_FIRST_CHAR = r'\w+!\-_$&=\.'
SYMBOL = r"[{0}][{0}\d/]*".format(SYMBOL_FIRST_CHAR)
t_KEYWORD = ":{}".format(SYMBOL)
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


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def lex(text=None):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True, debuglog=logging.getLogger(__name__))
    l = ply.lex.lex(reflags=re.UNICODE, **kwargs)
    if text is not None:
        l.input(text)
    return l