
import logging
import ply.lex

tokens = ('STRING',
          'NIL',
          'BOOLEAN',
          'NUMBER',
          'VECTOR_START',
          'VECTOR_END',
          'LIST_START',
          'LIST_END',
          'MAP_START',
          'SET_START',
          'MAP_OR_SET_END')


t_STRING = '"[^"]*"'
t_VECTOR_START = '\['
t_VECTOR_END = '\]'
t_LIST_START = '\('
t_LIST_END = '\)'
t_MAP_START = '\{'
t_SET_START = '\#\{'
t_MAP_OR_SET_END = '\}'
t_ignore = "".join([" ", "\t", ","])


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


def lex(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True, debuglog=logging.getLogger(__name__))
    l = ply.lex.lex(**kwargs)
    l.input(text)
    return l