
def dump(obj):
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
    elif isinstance(obj, list):
        return "[{}]".format(" ".join([dump(i) for i in obj]))
    elif isinstance(obj, set):
        return "#{{{}}}".format(" ".join([dump(i) for i in obj]))
    else:
        raise Exception("Don't know how to handle {} : {}", type(obj), obj)