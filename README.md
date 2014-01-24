# edn_format #

Implements the [EDN format](https://github.com/edn-format/edn) reader in
Python.

## Installation ##

    pip install edn_format

## Usage ##

    >>> import edn_format
    >>> edn_format.dumps({1, 2, 3})
    '#{1 2 3}'
    >>> edn_format.loads("[1 true nil]")
    [1, True, None]


In general, `edn_format.loads(edn_format.dumps(obj)) == obj`. If this is
false, it may be a bug.

See `tests.py` for full details.

## Caveats ##

Almost all features of EDN have been implemented, including custom
tagged elements.

But expect bugs since this has not yet been used in production.
