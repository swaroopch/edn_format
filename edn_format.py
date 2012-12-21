
import pytz
import pyrfc3339
from datetime import datetime
import uuid
import logging
import ply.lex as lex
import edn_lex


def lexer(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True, debuglog=logging.getLogger(__name__))
    l = lex.lex(module=edn_lex, **kwargs)
    l.input(text)
    return l


def loads(text):
    obj = text # TODO Parse EDN format
    return obj


def dumps(obj):
    text = obj # TODO Convert to EDN format
    return text