# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import collections


class ImmutableList(collections.MutableSequence, collections.Hashable):
    def __init__(self, wrapped_list, copy=True):
        self._list = list(wrapped_list) if copy else wrapped_list
        self._hash = None

    def __repr__(self):
        return self._list.__repr__()

    def __eq__(self, other):
        if isinstance(other, ImmutableList):
            return self._list == other._list
        else:
            return self._list == other

    def _call_wrapped_list_method(self, method, *args):
        new_list = list(self._list)
        getattr(new_list, method)(*args)
        return ImmutableList(new_list, copy=False)

    # collection.MutableSequence methods
    # https://docs.python.org/2/library/collections.html#collections-abstract-base-classes

    def __getitem__(self, index):
        return self._list[index]

    def __delitem__(self, *args):
        return self._call_wrapped_list_method("__delitem__", *args)

    def __setitem__(self, *args):
        return self._call_wrapped_list_method("__setitem__", *args)

    def __len__(self):
        return len(self._list)

    # collection.Hashable methods
    # https://docs.python.org/2/library/collections.html#collections-abstract-base-classes

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(self._list))
        return self._hash

    # Other list methods https://docs.python.org/2/tutorial/datastructures.html#more-on-lists

    def insert(self, *args):
        return self._call_wrapped_list_method("insert", *args)

    def sort(self, *args):
        return self._call_wrapped_list_method("sort", *args)
