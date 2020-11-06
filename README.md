# edn_format #

Implements the [EDN format](https://github.com/edn-format/edn) in Python.

All features of EDN are implemented, including custom tagged elements.

![Build Status](https://github.com/swaroopch/edn_format/workflows/Build/badge.svg)
![PyPI version](https://img.shields.io/pypi/v/edn_format.svg)](https://pypi.org/project/edn_format/)

## Installation ##

    pip install edn_format

## Usage ##

```pycon
>>> import edn_format
>>> edn_format.dumps({1, 2, 3})
'#{1 2 3}'
>>> edn_format.loads("[1 true nil]")
[1, True, None]
>>> edn_format.loads_all("1 2 3 4")
[1, 2, 3, 4]
```


In general, `edn_format.loads(edn_format.dumps(obj)) == obj`. If this is
false, it may be a bug.

See `tests.py` for full details.

## Contributors ##

Special thanks to the following contributors for making this library
usable:

- [@bfontaine](https://github.com/bfontaine)
- [@marianoguerra](https://github.com/marianoguerra)
- [@bitemyapp](https://github.com/bitemyapp)
- [@jashugan](https://github.com/jashugan)
- [@exilef](https://github.com/exilef)

## FAQ ##

### Why immutable list & dict? ###

IIRC, it was related to https://github.com/edn-format/edn#rationale :

> edn will yield distinct object identities when read, unless a reader implementation goes out of its way to make such a promise. Thus **the resulting values should be considered immutable**, and a reader implementation should yield values that ensure this, to the extent possible.
