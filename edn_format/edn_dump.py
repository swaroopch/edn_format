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
        return u"{}M".format(obj)
    elif isinstance(obj, (Keyword, Symbol)):
        return unicode(obj)
    elif isinstance(obj, basestring):
        return u'"{}"'.format(obj)
    elif isinstance(obj, tuple):
        return u"({})".format(seq(obj))
    elif isinstance(obj, list):
        return u"[{}]".format(seq(obj))
    elif isinstance(obj, set) or isinstance(obj, frozenset):
        return u"#{{{}}}".format(seq(obj))
    elif isinstance(obj, dict) or isinstance(obj, ImmutableDict):
        return u"{{{}}}".format(seq(itertools.chain.from_iterable(obj.items())))
    elif isinstance(obj, datetime.datetime):
        return u'#inst "{}"'.format(pyrfc3339.generate(obj))
    elif isinstance(obj, datetime.date):
        return u'#inst "{}"'.format(obj.isoformat())
    elif isinstance(obj, uuid.UUID):
        return u'#uuid "{}"'.format(obj)
    elif isinstance(obj, TaggedElement):
        return unicode(obj)
    else:
        raise NotImplementedError(
            "Don't know how to handle {} : {}", type(obj), obj)
