# `edn_format` Changelog

## v0.6.5 (2019/11/03)

* Parse integers in hexadecimal notation
* Disallow `0`-prefixed integers other than zero itself

## v0.6.4 (2019/09/14)

* Add an `edn_parse.tag` decorator

## v0.6.3 (2019/04/16)

* Add support for Unicode char literals

## v0.6.2 (2019/01/04)

* Parse `nil` and booleans as symbols

## v0.6.1 (2018/09/21)

* Use mutable data structures to improve parsing time
* Run Travis tests on Python 3.7

## v0.6.0 (2018/09/08)

* Fix vector parser to use `ImmutableList`
* Fix parsing of exact-precision floats with a negative exposant
* Support all ASCII characters
* Add a `sort_sets` optional argument to `dumps`
* Raise custom exceptions on syntax errors
* Support fractions
* Support `#_`

## v0.5.13 (2017/10/08)

* Convert requirements from exact to minimum

## v0.5.12 (2017/02/14)

* Unbreak tests on Python 2.x
* PEP8 style fixes

## v0.5.11 (2017/02/14)

* Add a `sort_keys` optional keyword argument to `dumps`
* Correctly parse floats with an exponent

## v0.5.10 (2017/02/13)

* Support string-\>keyword keys in `dumps`
* Add Travis config
* Bump dependencies

## v0.5.9 (2015/07/09)

* Add support to dump `#inst` with microseconds

## v0.5.8 (2015/06/19)

* Fix Python 2/3 support

## v0.5.7 (2015/06/08)

* Fix Python 3 `unichr`/`chr` incompatibility
* Changed Python version detection from exactly equal to 3 to greater than or
  equal to 3

## v0.5.6 (2015/05/31)

* Make UTF-8 the default expectation of text type

## v0.5.5 (2015/05/25)

* Fixed string parsing and escaping
* Unicode now consistently used internally
* New method `dumpu` added that returns unicode
* `dumps` method now takes optional encoding arguments: `output_encoding`
  (specifies encoding of output string) and `string_encoding` (specifies
  encoding of non-unicode strings in object to be serialized), both default to
  `'utf-8'`
* `loads` now takes optional argument `input_encoding`, defaults to `'utf-8'`
* New method `loadu` added that assumes unicode input
* Bump dependencies

## v0.5.4 (2015/02/26)

* Fix parsing of booleans before comma

## v0.5.3 (2014/05/03)

## v0.5 (2014/01/25)

* Fix `BaseEdnType.__hash__`
* Fix equality
* Handle escape sequences in strings
* Allow backslashed double-quotes in strings
* Add `<`, `>`, `@`

## v0.4 (2014/01/24)

* Parse empty collections
* Raise an exception on syntax error
* Improves patterns for `SYMBOL`, `TAG`, and `KEYWORD` to more closely match
  the [EDN specifications][spec]
* Improve Python 3 support

[spec]: https://github.com/edn-format/edn

## v0.3.6 (2014/01/15)

First published release.
