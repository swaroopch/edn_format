# -*- coding: utf-8 -*-

class Char(str):
    """
    This class represents a one-character string.
    """
    def __new__(cls, content):
        assert len(content) == 1, "Char can only contain one character."
        return super(Char, cls).__new__(cls, content)
