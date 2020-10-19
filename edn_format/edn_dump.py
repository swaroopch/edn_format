# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import decimal
import fractions
import re
import sys
import uuid

import pyrfc3339

from .immutable_dict import ImmutableDict
from .immutable_list import ImmutableList
from .char import Char
from .edn_lex import Keyword, Symbol
from .edn_parse import TaggedElement


# alias Python 2 types to their corresponding types in Python 3 if necessary
if sys.version_info[0] >= 3:
    __PY3 = True
    long = int
    basestring = str
    unicode = str
    unichr = chr
else:
    __PY3 = False


DEFAULT_INPUT_ENCODING = 'utf-8'
DEFAULT_OUTPUT_ENCODING = 'utf-8'

# proper unicode escaping
# see http://stackoverflow.com/a/24519338
ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]', re.UNICODE)
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
SPECIAL_CHARS = {
    "\n": r"\newline",
    "\r": r"\return",
    " ": r"\space",
    "\t": r"\tab",
}

for __i in range(0x20):
    ESCAPE_DCT.setdefault(unichr(__i), '\\u{0:04x}'.format(__i))
del __i


def unicode_escape(string):
    """Return a edn representation of a Python string"""
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, string) + '"'


def dump_char(c):
    """Return an EDN representation of a Char."""
    # 33-126 = printable ASCII range, except space (code 32)
    if ord(c) in range(33, 127):
        return "\\{}".format(c)

    if c in SPECIAL_CHARS:
        return SPECIAL_CHARS[c]

    # [2:] to strip the '0x' prefix
    return "\\u{}".format(hex(ord(c))[2:].upper().rjust(4, "0"))


def indent_lines(lines, open_sym, close_sym, indent, indent_step):
    """
    Indents a data structure.

    ``lines`` is an array of strings composed of each element of the data
    structure. ``open_sym`` and ``close_sym`` are strings representing the
    opening and closing symbol of the data structure (i.e.: for a dict it
    would be '{' and '}', respectively). ``indent`` is an integer representing
    the number of spaces used to indent. ``indent_step`` is an integer
    representing the current level of indentation.
    """
    indent_prev = indent_step
    indent_step = indent_prev + indent
    # open symbol should not be indented
    result = [open_sym]

    indent_spaces = indent_step * ' '
    result += [indent_spaces + line for line in lines]

    # close symbol should be indented using the previous indentation level
    result += [indent_prev * ' ' + close_sym]

    return '\n'.join(result)


def seq(obj, **kwargs):
    return [udump(i, **kwargs) for i in obj]


def udump(obj,
          string_encoding=DEFAULT_INPUT_ENCODING,
          keyword_keys=False,
          sort_keys=False,
          sort_sets=False,
          indent=None,
          indent_step=0):
    """
    Dumps a formatted representation of a Python object.

    ``string_encoding`` (defaults to 'utf-8') is the encoding to be used if the
    object are bytes instead of strings. ``keyword_keys`` when True (defaults
    to False) converts the keys from a dict from string to keywords.
    ``sort_keys`` when True (defaults to False) sort dict keys alphabetically.
    ``sort_sets`` when True (defaults to False) sort sets alphabetically.
    ``indent`` when set to a positive integer (defaults to None) represents
    the number of spaces used to indent the object. ``indent_step`` (defaults
    to 0) represents the current indentation level when ``indent`` is different
    from None.
    """
    kwargs = {
        "string_encoding": string_encoding,
        "keyword_keys": keyword_keys,
        "sort_keys": sort_keys,
        "sort_sets": sort_sets,
        "indent": indent,
        "indent_step": indent_step + (indent or 0),
    }

    if obj is None:
        return 'nil'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (int, long, float)):
        return unicode(obj)
    elif isinstance(obj, decimal.Decimal):
        return '{}M'.format(obj)
    elif isinstance(obj, (Keyword, Symbol)):
        return unicode(obj)
    elif isinstance(obj, Char):
        return dump_char(obj)
    # CAVEAT LECTOR! In Python 3 'basestring' is alised to 'str' above.
    # Furthermore, in Python 2 bytes is an instance of 'str'/'basestring' while
    # in Python 3 it is not.
    elif isinstance(obj, bytes):
        return unicode_escape(obj.decode(string_encoding))
    elif isinstance(obj, basestring):
        return unicode_escape(obj)
    elif isinstance(obj, tuple):
        lines = seq(obj, **kwargs)
        if indent is None:
            return '({})'.format(' '.join(lines))
        else:
            return indent_lines(lines, '(', ')', indent, indent_step)
    elif isinstance(obj, (list, ImmutableList)):
        lines = seq(obj, **kwargs)
        if indent is None:
            return '[{}]'.format(' '.join(lines))
        else:
            return indent_lines(lines, '[', ']', indent, indent_step)
    elif isinstance(obj, (set, frozenset)):
        if sort_sets:
            obj = sorted(obj)

        lines = seq(obj, **kwargs)
        if indent is None:
            return '#{{{}}}'.format(' '.join(lines))
        else:
            return indent_lines(lines, '#{', '}', indent, indent_step)
    elif isinstance(obj, (dict, ImmutableDict)):
        pairs = obj.items()

        if sort_keys:
            pairs = sorted(pairs, key=lambda p: str(p[0]))

        if keyword_keys:
            pairs = ((Keyword(k) if isinstance(k, (bytes, basestring)) else k, v) for k, v in pairs)

        lines = [' '.join(seq(p, **kwargs)) for p in pairs]
        if indent is None:
            return '{{{}}}'.format(' '.join(lines))
        else:
            return indent_lines(lines, '{', '}', indent, indent_step)
    elif isinstance(obj, fractions.Fraction):
        return '{}/{}'.format(obj.numerator, obj.denominator)
    elif isinstance(obj, datetime.datetime):
        return '#inst "{}"'.format(pyrfc3339.generate(obj, microseconds=True))
    elif isinstance(obj, datetime.date):
        return '#inst "{}"'.format(obj.isoformat())
    elif isinstance(obj, uuid.UUID):
        return '#uuid "{}"'.format(obj)
    elif isinstance(obj, TaggedElement):
        return unicode(obj)
    raise NotImplementedError(
        u"encountered object of type '{}' for which no known encoding is available: {}".format(
            type(obj), repr(obj)))


def dump(obj,
         string_encoding=DEFAULT_INPUT_ENCODING,
         output_encoding=DEFAULT_OUTPUT_ENCODING,
         keyword_keys=False,
         sort_keys=False,
         sort_sets=False,
         indent=None):
    outcome = udump(obj,
                    string_encoding=string_encoding,
                    keyword_keys=keyword_keys,
                    sort_keys=sort_keys,
                    sort_sets=sort_sets,
                    indent=indent)
    if __PY3:
        return outcome
    return outcome.encode(output_encoding)
