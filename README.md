# edn_format #

Implements the [EDN format](https://github.com/edn-format/edn) in Python.

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

## Caveats ##

Almost all features of EDN have been implemented, including custom
tagged elements.

But expect bugs since this has not yet been used in production.

## Contributors ##

Special thanks to the following contributors for making this library
usable:

- [@marianoguerra](https://github.com/marianoguerra)
- [@bitemyapp](https://github.com/bitemyapp)
- [@jashugan](https://github.com/jashugan)
- [@exilef](https://github.com/exilef)

## Contributor Notes ##

To release a new version:

1. Bump up the version number in `setup.py`, e.g. `0.5.4`
2. Create a git tag: `git tag -a v0.5.4 -m 'Version 0.5.4'`
3. Push git tag: `git push origin master --tags`
4. Make sure you have a [~/.pypirc file](http://docs.python.org/2/distutils/packageindex.html#pypirc) with your PyPI credentials.
5. Run `python setup.py sdist upload`
