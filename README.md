# edn_format #

Implements the [EDN format](https://github.com/edn-format/edn) in Python.

All features of EDN are implemented, including custom tagged elements.

[![Build Status](https://travis-ci.org/swaroopch/edn_format.svg?branch=master)](https://travis-ci.org/swaroopch/edn_format)
[![PyPI version](https://img.shields.io/pypi/v/edn_format.svg)](https://pypi.org/project/edn_format/)

## Installation ##

    pip install edn_format

## Usage ##

```pycon
>>> import edn_format
>>> edn_format.dumps({1, 2, 3})
'#{1 2 3}'
>>> edn_format.loads("[1 true nil]")
[1, True, None]
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
