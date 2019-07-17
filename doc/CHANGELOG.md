# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.0.0
### added
- add `Annotation` class
  + which has 'audio_file' and 'annot_file' attributes,
    along with 'seq' attribute

### changed
- rewrite everything centered around `Annotation` class
  + meaning `Sequence` and `Segment` lose their redundant 'file'
    attributes and all format modules convert to and from `Annotations`
    and so does the csv module
- single-source version
  + now found in an `__about__.py` file in `src/crowsetta` that is used
    by `setup.py`.

## 1.1.1
### changed
- `segments` property of a `Sequence` is a tuple, not a list, so that class is immutable + hashable

### fixed
- `__hash__` implementation for `Sequence` class
  + convert attributes that are `numpy.ndarray`s into tuples before hashing
- tests for `Sequence`
  + no longer assert that calling `__hash__` raises `NotImplementedError`
  + test that `segments` attribute is a `tuple` not a `list`

## 1.1.0
### added
- implement hashing and equality for `Sequence` class
  + this makes it possible to use with concurrency, e.g. with the Dask library

## 1.0.0
### added
- entry point group `crowsetta.format` to make it possible to 'install' formats
  + removes special casing for built-in formats, they just get added via entry point
  + instead of parsing a config.json file built into the package
- module for working with Praat Textgrid format
- `Meta` class which represents metadata about a format
  + such as file extension associated with it
  + and the module / functions that a `Transcriber` instance should use
    to work with this format

### changed
- Each instance of `Transcriber` has only one vocal annotation format that it handles
  + because it's annoying to type `file_format` every time you call a method like `to_seq`
  + instead you just make an instance of `Transcriber` for each format you want 
  + This also works better with `crowsetta.format` entry points and `Meta` class;
    when you instantiate a `Transcriber` for a given `voc_format`, the `__init__`
    uses the `Meta` for that format to figure out which function to use for `to_seq`, 
    `to_csv`, etc.
  + For this reason bumping to 1.0.0, new `Transcriber` not backwards compatible
    - although this will be inconvenient for millions of people

## 0.2.0a5
### added
- Sequence instances have attributes: labels, onsets_s, offsets_s, onsets_Hz, 
  offsets_Hz, and file. 
- Explanation of default `to_csv` function for user formats in `howto-user-config`.

### changed
- Sequence class totally re-written
  + no longer attrs-based
  + because of somewhat complicated logic for validating arguments that
  was necessary in init (to prevent user from creating a 'bad'
  instance.)
- Sequences are immutable. Idea is they are just connectors between 
  annotation and whatever user needs to do with it so you shouldn't 
  need to change any attribute values after loading annotation 
- Segment also immutable (by setting frozen=True in call to attr.s decorator)
- Transcriber.__init__ uses config.json instead of config.ini to read defaults
  + this makes __init__ logic more readable since we don't have to convert
  user_config dict to strings and then back again; default config just loads as 
  a dict from the .json file and we add the user_config dicts to it

## 0.2.0a4
### added
- `data` module that downloads small example datasets for each annotation format
  + includes `formats` function that is imported at package level 
  and prints formats built in to `crowsetta`
- `to_seq_func_to_csv` that takes a `yourformat2seq` function and returns a function
  that will convert the same format to csv files (just a wrapper around your function
  and `seq2csv`)
- for docs, Makefile that generates `./notebooks` folder from `./doc/notebooks`

### changed
- major revamp of docs
- `config_dict`s for `user_config` arg of Transcriber.__init__ only require
  `module` and `to_seq` keys; `to_csv` and `to_format` are optional, can be 
  specified Python `None` or a string `'None'`

### fixed
- Transcriber raises `NotImplemented` error when `to_csv` or `to_format` are 
  None for a specified format (instead of crashing mysteriously)
- `seq2csv` and `csv2seq` can deal with `None` values for one pair of onsets and offsets

## 0.2.0a3
### changed
- fix failing tests

## 0.2.0a2
### added
- `Segment` class, attrs-based
  + has `asdict` method (wrapper around `attrs` function)
  + has class variable `_FIELDS` which is used in any place 
  where we need to know how to go from `Segment` attributes to rows of
  a csv file, e.g. in src/crowsetta/csv.py and in tests

### changed
- `Sequence` class is now attrs-based, has factory functions, is itself
just a list of `Segment`s
  + now has `to_dict` method
- `Crowsetta` class is now called `Transcriber` 

## 0.2.0a1
### added
- add Crowsetta class with simple interface for converting any annotation to
- add ability to work with user-defined functions
  + user passes an `extra_config` dict when instantiating Crowsetta
- add docs

### changed
- change package name to Crowsetta
- change function names so they are all 'format2seq' or 'format2csv' or 
'toformat' for consistency

## 0.1.0
- Initial version after excising from hvc 
(https://github.com/NickleDave/hybrid-vocal-classifier/blob/master/hvc/utils/annotation.py)

### changed
- Convert tests to Python unittest format (instead of using PyTest library)

### added
+ Write README.md with usage