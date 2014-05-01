import sys
import itertools
import decimal
import datetime
import uuid
import pyrfc3339
from .immutable_dict import ImmutableDict

from .edn_lex import Keyword, Symbol
from .edn_parse import TaggedElement


if sys.version_info[0] == 3:
    long = int
    basestring = str
    unicode = str


def dump(obj):
    def seq(obj):
        return " ".join([dump(i) for i in obj])

    if obj is None:
        return "nil"
    elif isinstance(obj, bool):
        if obj:
            return "true"
        else:
            return "false"
    elif isinstance(obj, (int, long, float)):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return "{}M".format(obj)
    elif isinstance(obj, (Keyword, Symbol)):
        return str(obj)
    elif isinstance(obj, basestring):
        return '"{}"'.format(obj)
    elif isinstance(obj, tuple):
        return "({})".format(seq(obj))
    elif isinstance(obj, list):
        return "[{}]".format(seq(obj))
    elif isinstance(obj, set) or isinstance(obj, frozenset):
        return "#{{{}}}".format(seq(obj))
    elif isinstance(obj, dict) or isinstance(obj, ImmutableDict):
        return "{{{}}}".format(seq(itertools.chain.from_iterable(obj.items())))
    elif isinstance(obj, datetime.datetime):
        return '#inst "{}"'.format(pyrfc3339.generate(obj))
    elif isinstance(obj, datetime.date):
        return '#inst "{}"'.format(obj.isoformat())
    elif isinstance(obj, uuid.UUID):
        return '#uuid "{}"'.format(obj)
    elif isinstance(obj, TaggedElement):
        return str(obj)
    else:
        raise NotImplementedError(
            "Don't know how to handle {} : {}", type(obj), obj)
