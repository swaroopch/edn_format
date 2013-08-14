from __future__ import print_function

import sys
import uuid
import pyrfc3339

import ply.yacc
from .edn_lex import tokens, lex

if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str

if tokens: pass # Dummy statement to indicate that 'tokens' is used.

start = 'expression'

_serializers = {}


class TaggedElement(object):
    def __init__(self, name, value):
        raise NotImplementedError("To be implemented by derived classes")

    def __str__(self):
        raise NotImplementedError("To be implemented by derived classes")


def add_tag(tag_name, tag_class):
    assert isinstance(tag_name, basestring)
    _serializers[tag_name] = tag_class


def remove_tag(tag_name):
    assert isinstance(tag_name, basestring)
    del _serializers[tag_name]


def p_term_leaf(p):
    """term : CHAR
            | STRING
            | INTEGER
            | FLOAT
            | BOOLEAN
            | NIL
            | KEYWORD
            | SYMBOL
            | WHITESPACE"""
    p[0] = p[1]

def p_empty_vector(p):
    """vector : VECTOR_START VECTOR_END"""
    p[0] = []

def p_vector(p):
    """vector : VECTOR_START expressions VECTOR_END"""
    p[0] = p[2]

def p_empty_list(p):
    """list : LIST_START LIST_END"""
    p[0] = tuple()

def p_list(p):
    """list : LIST_START expressions LIST_END"""
    p[0] = tuple(p[2])

def p_empty_set(p):
    """set : SET_START MAP_OR_SET_END"""
    p[0] = set()

def p_set(p):
    """set : SET_START expressions MAP_OR_SET_END"""
    p[0] = set(p[2])

def p_empty_map(p):
    """map : MAP_START MAP_OR_SET_END"""
    p[0] = {}

def p_map(p):
    """map : MAP_START expressions MAP_OR_SET_END"""
    terms = p[2]
    if len(terms) % 2 != 0:
        raise SyntaxError("Even number of terms required for map")
    p[0] = dict([terms[i:i+2] for i in range(0, len(terms), 2)]) # partition terms in pairs


def p_expressions_expressions_expression(p):
    """expressions : expressions expression"""
    p[0] = p[1] + [p[2]]


def p_expressions_expression(p):
    """expressions : expression"""
    p[0] = [p[1]]


def p_expression(p):
    """expression : vector
                  | list
                  | set
                  | map
                  | term"""
    p[0] = p[1]


def p_expression_tagged_element(p):
    """expression : TAG expression"""
    tag = p[1]
    element = p[2]

    if tag == 'inst':
        output = pyrfc3339.parse(element)
    elif tag == 'uuid':
        output = uuid.UUID(element)
    elif tag in _serializers:
        output = _serializers[tag](element)
    else:
        raise NotImplementedError("Don't know how to handle tag {}".format(tag))

    p[0] = output


def p_error(p):
    if p is None:
        print("Syntax Error! Reached EOF!")
    else:
        print("Syntax error! {}".format(p))


def parse(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True)
    p = ply.yacc.yacc(**kwargs)

    return p.parse(text, lexer=lex())
