# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.4.0 -- 2022-03-26
### Added
- add a `__repr__` to the `Transcriber` class
  [#145](https://github.com/NickleDave/crowsetta/pull/143).
  Fixes [#142](https://github.com/NickleDave/crowsetta/issues/141).

### Changed
- change format names 'simple-csv' and 'csv' to 'simple-seq' and 'generic-seq'.
  With goal of eventually having 'simple-seq' work on other file formats, e.g. .txt,
  and for 'csv' to be the "generic" sequence format that allow for converting between others.
  [#140](https://github.com/NickleDave/crowsetta/pull/140).
  Fixes [#133](https://github.com/NickleDave/crowsetta/issues/133).
- deprecate the name 'csv' for the 'generic-seq' format;
  a FutureWarning is raised when creating a `Transcriber` 
  with `format='csv'`.
  [#143](https://github.com/NickleDave/crowsetta/pull/143).
  Fixes [#141](https://github.com/NickleDave/crowsetta/issues/141).

- switch to using `nox` for development, instead of `make`
  [#137](https://github.com/NickleDave/crowsetta/pull/137).
  Fixes [#132](https://github.com/NickleDave/crowsetta/issues/132.

## 3.3.0 -- 2022-01-02
### Added
- add 'simple-csv' format 
  [#130](https://github.com/NickleDave/crowsetta/pull/130).
  Fixes [#97](https://github.com/NickleDave/crowsetta/issues/197).

### Changed
- change dependency / format name `koumura` to `birdsong-recognition-dataset` 
  because package was renamed
  [#126](https://github.com/NickleDave/crowsetta/pull/126).
  Fixes [#124](https://github.com/NickleDave/crowsetta/issues/124).
- switch to using `flit` to build / publish. Remove `poetry`.
  [#127](https://github.com/NickleDave/crowsetta/pull/127).
  Fixes [#125](https://github.com/NickleDave/crowsetta/issues/125).
- move `textgrid` package into sub-package `_vendor`, since `flit` only works 
  with a single top-level package.
  [#127](https://github.com/NickleDave/crowsetta/pull/127).
  This is the approach `pip` takes, as discussed on https://github.com/pypa/flit/issues/497.
- rename attributes / variables `onsets_Hz` and `offsets_Hz` 
  to `onset_inds` and `offset_inds`
  [#128](https://github.com/NickleDave/crowsetta/pull/128).
  Fixes [#87](https://github.com/NickleDave/crowsetta/pull/87).
- rename function `crowsetta.validation._parse_file` to `validate_ext`
  [#129](https://github.com/NickleDave/crowsetta/pull/129).
  Fixes [#123](https://github.com/NickleDave/crowsetta/pull/123).

## 3.2.0 -- 2021-12-19
### Added
- add a [CITATION.cff](https://citation-file-format.github.io/) file
  [#103](https://github.com/NickleDave/vak/pull/103).
- add `'yarden'` format, that parses the `.mat` files saved by 
  [`SongAnnotationGUI`](https://github.com/yardencsGitHub/BirdSongBout/blob/master/helpers/GUI/README.md), 
  and is used with the canary song dataset that accompanies the 
  [`tweetynet` paper](https://github.com/yardencsGitHub/tweetynet).
  [#122](https://github.com/NickleDave/crowsetta/pull/122).
  Fixes [#121](https://github.com/NickleDave/crowsetta/issues/121).

### Changed
- rewrite tests to use `pytest` [#106](https://github.com/NickleDave/crowsetta/pull/106)
  Fixes [#89](https://github.com/NickleDave/crowsetta/issues/89).
- change compatible Python versions to >3.6 and <3.10
  [#111](https://github.com/NickleDave/crowsetta/pull/111).
- switch from using [Make](https://www.gnu.org/software/make/)
  to using [nox](https://nox.thea.codes/en/stable/) 
  for development tasks
  [#137](https://github.com/NickleDave/crowsetta/pull/137).
  As [suggsted by Scikit-HEP](https://scikit-hep.org/developer/tasks).
  Fixes [#132](https://github.com/NickleDave/crowsetta/issues/132).

### Fixed
- Fix .TextGrid and .phn docstrings that referred to ".not.mat files"
  [#118](https://github.com/NickleDave/crowsetta/pull/118).

### Removed
- remove `data` module [#110](https://github.com/NickleDave/crowsetta/pull/110) 
  that downloaded data from other sources.
  Fixes [#93](https://github.com/NickleDave/crowsetta/issues/93).

## 3.1.1.post1 -- 2021-03-04
### fixed
- add missing `packages` to pyproject.toml so that `textgrid` is included 
  in build
  [857ba09](https://github.com/NickleDave/crowsetta/commit/857ba097eedf45a38c33244fd7353bc7fdb48315)
- add metadata to pyproject.toml so that README is used as "long description" 
  and appears on PyPI
  [e8b8209](https://github.com/NickleDave/crowsetta/commit/e8b8209fff5a3aa530b7ef93b015c6b35c5615a5)

## 3.1.1 -- 2021-03-04
### changed
- switch to using `poetry` for development
  [#79](https://github.com/NickleDave/crowsetta/pull/79)
- raise minimum version of `evfuncs` to 0.3.1
  [#79](https://github.com/NickleDave/crowsetta/pull/79)
- raise minimum version of `koumura` to 0.2.0
  [#79](https://github.com/NickleDave/crowsetta/pull/79)
- change to using GitHub Actions for continuous integration
  [#83](https://github.com/NickleDave/crowsetta/pull/83)

### fixed
- fix dependencies and Python so they are not pinned to major version
  [#83](https://github.com/NickleDave/crowsetta/pull/83)

## 3.1.0
### changed
- switch to using `soundfile` library to parse .wav files
  [#75](https://github.com/NickleDave/crowsetta/pull/75)
  see discussion on issue [#67](https://github.com/NickleDave/crowsetta/issues/67).

### fixed
- fix `phn2annot` function so it works with `.PHN` and `.WAV` files found in 
  some versions of TIMIT dataset
  [#75](https://github.com/NickleDave/crowsetta/pull/75)
  + needed to make extension checking case-insensitive, 
    see issue [#68](https://github.com/NickleDave/crowsetta/issues/68)
  + and also switch to `soundfile` library to be able to parse the specific NIST format of .WAV files
 
## 3.0.1
### fixed
- add missing comma in `ENTRY_POINTS` in `setup.py` 
  so that built-in formats are properly installed
  [599149f](https://github.com/NickleDave/crowsetta/commit/599149f2bb52fb4cd01deca4d4b151fff085171c)

## 3.0.0
### added
- make `csv` a format
  [#60](https://github.com/NickleDave/crowsetta/pull/60); 
  See discussion on 
  [#55](https://github.com/NickleDave/crowsetta/issues/55).

### changed
- change name of `Transcriber` parameter `annot_format` to just `format`
  [#64](https://github.com/NickleDave/crowsetta/pull/64)
- change name of `Annotation` attributes `annot_file` and `audio_file` to 
  `annot_path` and `audio_path`, for clarity and to match what's used in 
  the `vak` library
  [#65](https://github.com/NickleDave/crowsetta/pull/65)

## 2.3.0
### added
- add `phn` module that parses `.phn` files from TIMIT dataset
  [#59](https://github.com/NickleDave/crowsetta/pull/59)

## 2.2.0
### changed
- change types of `Annotation` attributes `annot_file` and `audio_path` from `str` (string) 
  to `pathlib.Path`, to fix errors raised when passing in `Path` objects (because the 
  attribute validator requires a string), and because it's preferable to work with `Path` 
  objects over strings [#52](https://github.com/NickleDave/crowsetta/pull/52)
- change default value for `koumura2annot` parameter `wavpath` so that the function 
  will work regardless of current working directory for user, instead of requiring 
  them to be in the parent directory of the `.wav` files that `wavpath` refers to
  [#53](https://github.com/NickleDave/crowsetta/pull/53)

### fixed
- fixed error that `koumura2annot` function threw when `annot_file` was a `pathlib.Path` 
  and not a string [#53](https://github.com/NickleDave/crowsetta/pull/53) 

## 2.1.0
### changed
- modify functions for `.not.mat` annotation files (created by evsonganaly GUI) 
  so they do not require other files such as `.rec` files (created by evTAF data 
  acquisition program)
  - `notmat.notmat2annot` no longer looks for `.rec` files, which it used to get 
    the sampling rate and convert onsets and offsets from seconds to Hz
- the `make_notmat` for creating `.not.mat` files from `Annotation`s also 
  now expects onsets and offsets in seconds, not Hz.
  + the idea being that one can go from `.not.mat` to `Annotation` and back 
    without doing any extra conversion. If user needs conversion to Hz for 
    some other reason they can do this using the `Annotation` 

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
- Sequence instances have attributes: labels, onsets_s, offsets_s, onset_inds, 
  offset_inds, and file. 
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