# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import itertools
import decimal
import datetime
import uuid
import pyrfc3339
import re
from .immutable_dict import ImmutableDict

from .edn_lex import Keyword, Symbol
from .edn_parse import TaggedElement

if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str

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

for i in range(0x20):
    ESCAPE_DCT.setdefault(unichr(i), '\\u{0:04x}'.format(i))


def unicode_escape(string):
    """Return a edn representation of a Python string"""
    def replace(match):
        return ESCAPE_DCT[match.group(0)]

    return '"' + ESCAPE.sub(replace, string) + '"'


def udump(obj, string_encoding = 'utf-8'):
    def seq(obj):
        return ' '.join([udump(i, string_encoding = string_encoding) for i in obj])

    if obj is None:
        return 'nil'
    elif isinstance(obj, bool):
        if obj:
            return 'true'
        else:
            return 'false'
    elif isinstance(obj, (int, long, float)):
        return unicode(obj)
    elif isinstance(obj, decimal.Decimal):
        return '{}M'.format(obj)
    elif isinstance(obj, (Keyword, Symbol)):
        return unicode(obj)
    elif isinstance(obj, basestring):
        if isinstance(obj, unicode):
            uobj = obj
        else:
            uobj = obj.decode(string_encoding)
        return unicode_escape(uobj)
    elif isinstance(obj, tuple):
        return '({})'.format(seq(obj))
    elif isinstance(obj, list):
        return '[{}]'.format(seq(obj))
    elif isinstance(obj, set) or isinstance(obj, frozenset):
        return '#{{{}}}'.format(seq(obj))
    elif isinstance(obj, dict) or isinstance(obj, ImmutableDict):
        return '{{{}}}'.format(seq(itertools.chain.from_iterable(obj.items())))
    elif isinstance(obj, datetime.datetime):
        return '#inst "{}"'.format(pyrfc3339.generate(obj))
    elif isinstance(obj, datetime.date):
        return '#inst "{}"'.format(obj.isoformat())
    elif isinstance(obj, uuid.UUID):
        return '#uuid "{}"'.format(obj)
    elif isinstance(obj, TaggedElement):
        return unicode(obj)
    else:
        raise NotImplementedError(
            u"Don't know how to handle {} : {}", type(obj), obj)


def dump(obj, string_encoding = 'utf-8', output_encoding = 'utf-8'):
    return udump(obj, string_encoding = string_encoding).encode(output_encoding)
