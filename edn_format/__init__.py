
from edn_format import edn_dump, edn_parse
from edn_format.edn_lex import Keyword, Symbol


def loads(text):
    return edn_parse.parse(text)


def dumps(obj):
    return edn_dump.dump(obj)


__all__ = ['loads', 'dumps', 'Keyword', 'Symbol']