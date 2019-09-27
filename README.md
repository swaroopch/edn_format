# edn_format #

Implements the [EDN format](https://github.com/edn-format/edn) in Python.

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
>>> edn_format.loads_all("1 2 3 4")
[1, 2, 3, 4]
```


In general, `edn_format.loads(edn_format.dumps(obj)) == obj`. If this is
false, it may be a bug.

See `tests.py` for full details.

## Caveats ##

All features of EDN have been implemented, including custom tagged elements.

However, I personally don't use this in production, even though many users do, esp. the active contributors below.

## Contributors ##

Special thanks to the following contributors for making this library
usable:

- [@bfontaine](https://github.com/bfontaine)
- [@marianoguerra](https://github.com/marianoguerra)
- [@bitemyapp](https://github.com/bitemyapp)
- [@jashugan](https://github.com/jashugan)
- [@exilef](https://github.com/exilef)

## Local Dev ##

```bash
# 1. One-time: Install Vagrant
#
# macOS
# Install Homebrew from https://brew.sh
# brew cask install virtualbox vagrant
#
# All OSes
# Install from https://www.vagrantup.com/downloads.html

# 2. One-time: Install Vagrant plugin
vagrant plugin install vagrant-vbguest

# 3. This is all you need
vagrant up

# 4. To access the dev environment via ssh
vagrant ssh
cd /vagrant
# To run tests
python tests.py
# To check Python warnings
python -Wall -c 'import edn_format'
# Code style
flake8 --max-line-length=100 --exclude=parsetab.py .
```

## Contributor Notes ##

To release a new version:

1. Ensure you have [setup GPG](https://help.github.com/en/articles/generating-a-new-gpg-key) and [`twine`](https://pypi.org/project/twine/)
2. Bump up the version number in `setup.py`, e.g. `0.6.3`
3. Create a git tag: `git tag -s v0.6.3 -m 'Version 0.6.3'` (use [signed tags](https://help.github.com/en/articles/signing-tags))
4. Verify git tag: `git tag -v v0.6.3`
5. Push git tag: `git push origin master --tags`
6. Clean your `dist/` directory if it already exists
7. Package the release: `python setup.py sdist bdist_wheel`
8. Check the package: `twine check dist/*`
9. Upload the package: `twine upload dist/*`
