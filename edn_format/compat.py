# -*- coding: utf-8 -*-
import sys

_PY3 = sys.version_info[0] == 3

# alias Python 2 types to their corresponding types in Python 3 if necessary
if _PY3:
    long = int
    basestring = str
    unicode = str
    unichr = chr
    def _bytes(s): return bytes(s, 'utf-8')
else:
    long = long
    basestring = basestring
    unicode = unicode
    unichr = unichr
    _bytes = bytes
