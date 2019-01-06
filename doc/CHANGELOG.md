# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### added
- Sequence instances have attributes: labels, onsets_s, offsets_s, onsets_Hz, 
  offsets_Hz, and file. 

### changed
- Sequence class totally re-written
  + no longer attrs-based
  + because of somewhat complicated logic for validating arguments that
  (I decided) was necessary in init (to prevent user from creating a 'bad'
  instance. A Nanny State init function.)
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