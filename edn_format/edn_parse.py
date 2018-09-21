# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import sys
import uuid
from collections import deque

import ply.yacc
import pyrfc3339

from .edn_lex import tokens, lex
from .exceptions import EDNDecodeError
from .immutable_dict import ImmutableDict
from .immutable_list import ImmutableList


if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str

# Dummy statement to indicate that 'tokens' is used.
if tokens:
    pass

start = 'expression'

_serializers = dict({})


class TaggedElement(object):
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
            | RATIO
            | WHITESPACE"""
    p[0] = p[1]


def p_vector(p):
    """vector : VECTOR_START expressions VECTOR_END"""
    p[0] = ImmutableList(p[2])


def p_list(p):
    """list : LIST_START expressions LIST_END"""
    p[0] = tuple(p[2])


def p_set(p):
    """set : SET_START expressions MAP_OR_SET_END"""
    p[0] = frozenset(p[2])


def p_map(p):
    """map : MAP_START expressions MAP_OR_SET_END"""
    terms = p[2]
    if len(terms) % 2 != 0:
        raise EDNDecodeError('Even number of terms required for map')
    # partition terms in pairs
    p[0] = ImmutableDict((terms[i], terms[i+1]) for i in range(0, len(terms), 2))


def p_discarded_expressions(p):
    """discarded_expressions : DISCARD_TAG expression discarded_expressions
                             |"""
    p[0] = deque([])


def p_expressions_expression_expressions(p):
    """expressions : expression expressions"""
    p[2].appendleft(p[1])
    p[0] = p[2]


def p_expressions_empty(p):
    """expressions : discarded_expressions"""
    p[0] = deque([])


def p_expression(p):
    """expression : vector
                  | list
                  | set
                  | map
                  | term"""
    p[0] = p[1]


def p_expression_discard_expression_expression(p):
    """expression : DISCARD_TAG expression expression"""
    p[0] = p[3]


def p_expression_tagged_element(p):
    """expression : TAG expression"""
    tag = p[1]
    element = p[2]

    if tag == 'inst':
        if len(element) == 10 and element.count('-') == 2:
            output = datetime.datetime.strptime(element, '%Y-%m-%d').date()
        elif len(element) == 7 and element.count('-') == 1:
            output = datetime.datetime.strptime(element, '%Y-%m').date()
        elif len(element) == 4 and element.count('-') == 0:
            output = datetime.datetime.strptime(element, '%Y').date()
        else:
            output = pyrfc3339.parse(element)
    elif tag == 'uuid':
        output = uuid.UUID(element)
    elif tag in _serializers:
        output = _serializers[tag](element)
    else:
        raise NotImplementedError(
            u"Don't know how to handle tag ImmutableDict({})".format(tag))

    p[0] = output


def eof():
    raise EDNDecodeError('EOF Reached')


def p_error(p):
    if p is None:
        eof()
    else:
        raise EDNDecodeError(p)


def parse(text, input_encoding='utf-8'):
    if not isinstance(text, unicode):
        text = text.decode(input_encoding)

    kwargs = ImmutableDict({})
    if __debug__:
        kwargs = dict({'debug': True})
    p = ply.yacc.yacc(**kwargs)
    return p.parse(text, lexer=lex())
