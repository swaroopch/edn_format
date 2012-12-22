
import itertools

import datetime
import uuid
import pyrfc3339


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
    elif isinstance(obj, basestring):
        if obj.startswith(":"):
            return obj
        else:
            return '"{}"'.format(obj)
    elif isinstance(obj, tuple):
        return "({})".format(seq(obj))
    elif isinstance(obj, list):
        return "[{}]".format(seq(obj))
    elif isinstance(obj, set):
        return "#{{{}}}".format(seq(obj))
    elif isinstance(obj, dict):
        return "{{{}}}".format(seq(itertools.chain.from_iterable(obj.items())))
    elif isinstance(obj, datetime.datetime):
        return '#inst "{}"'.format(pyrfc3339.generate(obj))
    elif isinstance(obj, uuid.UUID):
        return '#uuid "{}"'.format(obj)
    else:
        raise Exception("Don't know how to handle {} : {}", type(obj), obj)