
import pytz
import pyrfc3339
from datetime import datetime
import uuid
import logging


def loads(text):
    obj = text # TODO Parse EDN format
    return obj


def dumps(obj):
    text = obj # TODO Convert to EDN format
    return text