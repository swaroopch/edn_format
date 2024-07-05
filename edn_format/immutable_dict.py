# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc


class ImmutableDict(collections_abc.Mapping):
    def __init__(self, somedict):
        self.dict = dict(somedict)   # make a copy
        self.hash = None

    def __getitem__(self, key):
        return self.dict[key]

    def __repr__(self):
        return self.dict.__repr__()

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __hash__(self):
        if self.hash is None:
            self.hash = hash(frozenset(self.dict.items()))
        return self.hash

    def __eq__(self, other):
        if isinstance(other, ImmutableDict):
            return self.dict == other.dict
        else:
            return self.dict == other
