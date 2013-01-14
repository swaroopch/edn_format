
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = """\
# edn_format

Implements the EDN format reader in Python.
See https://github.com/edn-format/edn for details.

# Installation

    pip install edn_format

# Usage

    >>> import edn_format
    >>> edn_format.dumps({1, 2, 3})
    '#{1 2 3}'
    >>> edn_format.loads("[1 true nil]")
    [1, True, None]


In general, `edn_format.loads(edn_format.dumps(obj)) == obj`.
If this is false, it may be a bug.

See `tests.py` for full details.

# Caveats

Almost all features of EDN have been implemented, including custom tagged
elements. But expect bugs since this has not yet been used in production.
"""

setup(name="edn_format",
      version="0.3.1",
      author="Swaroop C H",
      author_email="swaroop@swaroopch.com",
      description="EDN format reader and writer in Python",
      long_description=README,
      url="https://github.com/swaroopch/edn_format",
      install_requires=[
          "pytz==2012h",
          "pyRFC3339==0.1",
          "ply==3.4",
      ],
      license="apache",
      py_modules=['edn_format'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
