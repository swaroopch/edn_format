# Contributing to edn\_format #

## Setup ##

1. Make sure you have a working Python installation (2 or 3). You may want to
   use a [Virtualenv][] or a similar tool to create an isolated environment.
2. Install `edn_format`’s dependencies: `pip install -r requirements.txt`
3. Install `flake8`: `pip install flake8`

[Virtualenv]: https://virtualenv.pypa.io/en/stable/#virtualenv

## Tests ##

Run unit tests with:

    python tests.py

Run a linter over the code with:

    flake8 --max-line-length=100 --exclude=parsetab.py tests.py
