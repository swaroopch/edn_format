
import edn_parse

def loads(text):
    return edn_parse.parse(text)


def dumps(obj):
    text = obj # TODO Convert to EDN format
    return text