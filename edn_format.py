
import edn_parse
import edn_dump


def loads(text):
    return edn_parse.parse(text)


def dumps(obj):
    return edn_dump.dump(obj)