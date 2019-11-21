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

start = 'expressions'

_serializers = {}


class TaggedElement(object):
    def __str__(self):
        raise NotImplementedError("To be implemented by derived classes")


def add_tag(tag_name, tag_fn_or_class):
    """
    Add a custom tag handler.
    """
    assert isinstance(tag_name, basestring)
    _serializers[tag_name] = tag_fn_or_class


def remove_tag(tag_name):
    """
    Remove a custom tag handler.
    """
    assert isinstance(tag_name, basestring)
    del _serializers[tag_name]


def tag(tag_name):
    """
    Decorator for a function or a class to use as a tagged element.

    Example:

        @tag("dog")
        def parse_dog(name):
            return {
                "kind": "dog",
                "name": name,
                "message": "woof-woof",
            }

        parse("#dog \"Max\"")
        # => {"kind": "dog", "name": "Max", "message": "woof-woof"}
    """

    def _tag_decorator(fn_or_cls):
        _serializers[tag_name] = fn_or_cls
        return fn_or_cls
    return _tag_decorator


def p_term_leaf(p):
    """term : CHAR
            | STRING
            | HEX_INTEGER
            | INTEGER
            | FLOAT
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
    p[0] = deque()


def p_expressions_expression_expressions(p):
    """expressions : expression expressions"""
    p[2].appendleft(p[1])
    p[0] = p[2]


def p_expressions_empty(p):
    """expressions : discarded_expressions"""
    p[0] = deque()


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
        length = len(element)
        hyphens_count = element.count('-')

        if length == 10 and hyphens_count == 2:
            output = datetime.datetime.strptime(element, '%Y-%m-%d').date()
        elif length == 7 and hyphens_count == 1:
            output = datetime.datetime.strptime(element, '%Y-%m').date()
        elif length == 4 and hyphens_count == 0:
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


def parse_all(text, input_encoding='utf-8', debug=False,
              write_ply_tables=True):
    """
    Parse all objects from the text and return a (possibly empty) list.

    ``debug`` and ``write_ply_tables`` arguments are passed to the Yacc parser.
    If ``debug`` is True, the parser writes a ``parser.out`` debugging file.
    If ``write_ply_tables`` is True, the parser writes grammar tables in a
    ``parsetab.py`` module on disk and reuse it in subsequent calls. If it
    can't write this cache file, it'll print a warning, and be a bit less
    efficient as it'll have to re-generate the tables every time. If you can't
    let it write its cache, you can disable this warning by passing
    `write_ply_tables=False`.
    """
    if not isinstance(text, unicode):
        text = text.decode(input_encoding)

    # See http://www.dabeaz.com/ply/ply.html#ply_nn36
    p = ply.yacc.yacc(debug=debug, write_tables=write_ply_tables)
    expressions = p.parse(text, lexer=lex())
    return list(expressions)


def parse(text, **kwargs):
    """
    Parse one object from the text. Return None if the text is empty.

    See parse_all for the accepted arguments.
    """
    expressions = parse_all(text, **kwargs)
    return expressions[0] if expressions else None
