# -*- coding: utf-8 -*-
from .edn_lex import Keyword, Symbol
from .edn_parse import parse as loads
from .edn_parse import uparse as loadu
from .edn_parse import add_tag, remove_tag, TaggedElement
from .edn_dump import dump as dumps
from .edn_dump import udump as dumpu
from .immutable_dict import ImmutableDict

__all__ = ('loads',
           'loadu',
           'dumps',
           'dumpu',
           'ImmutableDict',
           'Keyword',
           'Symbol',
           'add_tag',
           'remove_tag',
           'TaggedElement')
