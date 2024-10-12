# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 5.1.0
### Added
- Make `crowsetta.SimpleSeq.from_file` work with an "empty" csv file,
  one that has no annotated segments
  (e.g. because no audio was above threshold for segmenting)
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#264](https://github.com/NickleDave/crowsetta/issues/264).
- Add `default_label` argument to `crowsetta.SimpleSeq.from_file` 
  that will add labels to segments in a csv file if there are none
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#271](https://github.com/NickleDave/crowsetta/issues/271).
- Add example csv file from 
  [Jourjine et al. 2023 dataset](https://datadryad.org/stash/dataset/doi:10.5061/dryad.g79cnp5ts)
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#274](https://github.com/NickleDave/crowsetta/issues/274).
- Add how-to showing how to work with unannotated segmentation 
  in a csv file, using the csv from the Jourjine et al. 2023 dataset
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#275](https://github.com/NickleDave/crowsetta/issues/275).

### Changed
- Rename `crowsetta.data` to `crowsetta.examples`, 
  simplify how `crowsetta.example` works 
  (to be more like `vocalpy.example`)
  and give all the example annotation files 
  more specific names so that we can have 
  multiple examples per annotation format
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#278](https://github.com/NickleDave/crowsetta/issues/278).
- Import format classes at package level, so we can just type e.g. 
  `crowsetta.SimpleSeq` instead of `crowsetta.formats.seq.SimpleSeq` 
  ("flat is better than nested") 
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#273](https://github.com/NickleDave/crowsetta/issues/273).

### Fixed
- Make `crowsetta.SimpleSeq.from_file` use `columns_map` arg 
  to rename only columns whose names are keys in the supplied dict, 
  and ignore other columns in the csv file
  [#280](https://github.com/NickleDave/crowsetta/pull/280).
  Fixes [#272](https://github.com/NickleDave/crowsetta/issues/272).


## 5.0.3
### Fixed
- Replace deprecated `pandera.SchemaModel` with `DataFrameModel`,
  fixes `AttributeError` on import after new install
  [#266](https://github.com/NickleDave/crowsetta/pull/266).
  Fixes [#265](https://github.com/NickleDave/crowsetta/issues/265).
- Change range of Python version supported from 3.9-3.11 to 3.10-3.12
  [#268](https://github.com/NickleDave/crowsetta/pull/268).
  Fixes [#267](https://github.com/NickleDave/crowsetta/issues/267).

## 5.0.2 -- 2024-01-01
### Fixed
- Vendor code from evfuncs and birdsong-recognition-dataset packages,
  to reduce the number of dependencies and make sure the code is maintained
  [#263](https://github.com/NickleDave/crowsetta/pull/263).
  Fixes [#262](https://github.com/NickleDave/crowsetta/issues/262).

## 5.0.1 -- 2023-05-27
### Fixed
- Fix bug in "generic-seq" format; use validated dataframe 
  returned by pandera schema, so that "label" column is 
  coerced to strings
  [#258](https://github.com/NickleDave/crowsetta/pull/258).
  Fixes [#257](https://github.com/NickleDave/crowsetta/issues/257).

## 5.0.0 -- 2023-03-29
### Added
- Add information on contributing and setting up a development environment
  [#212](https://github.com/NickleDave/crowsetta/pull/212).
  Fixes [#30](https://github.com/NickleDave/crowsetta/issues/30).
- Add method to convert generic sequence format to a pandas DataFrame
  [#216](https://github.com/NickleDave/crowsetta/pull/216).
- Add additional vignettes to docs:
  on removing "silent" labels from TextGrid annotations,
  on converting to the simple sequence and generic sequence formats
  [#216](https://github.com/NickleDave/crowsetta/pull/216).
  Fixes [#152](https://github.com/NickleDave/crowsetta/issues/152)
  and [#197](https://github.com/NickleDave/crowsetta/issues/197).
- Add format class for Audacity extended label track format
  [#226](https://github.com/NickleDave/crowsetta/pull/226).
  Fixes [#222](https://github.com/NickleDave/crowsetta/issues/222)
  and [#213](https://github.com/NickleDave/crowsetta/issues/213).
- Add the ability for a crowsetta.Annotation to have multiple sequences
  [#243](https://github.com/NickleDave/crowsetta/pull/243).
  Fixes [#42](https://github.com/NickleDave/crowsetta/issues/42).
- Rewrite TextGrid class to better handle file formats:
  parse both "short" and default format in either UTF-8 or UTF-16
  encoding; remove empty intervals from interval tiers by default;
  can convert multiple interval tiers to a single crowsetta.Annotation 
  with multiple crowsetta.Sequences
  [#243](https://github.com/NickleDave/crowsetta/pull/243).
  Fixes [#241](https://github.com/NickleDave/crowsetta/issues/241)

### Removed
- Remove `Segment.from_row` method, no longer used
  [#232](https://github.com/NickleDave/crowsetta/pull/232).
  Fixes [#231](https://github.com/NickleDave/crowsetta/issues/231)

### Fixed
- Revise landing page of docs, and some vignettes. 
  Make other changes to clean up the docs build process 
  [#216](https://github.com/NickleDave/crowsetta/pull/216).
- Coerce path-like attributes of `GenericSeq` dataframe schema to be strings.
  This helps ensure these columns are always native Pandas types
  [#237](https://github.com/NickleDave/crowsetta/pull/237).
- Fix how the `crowsetta.Segment` class converts 
  onset sample and offset sample to int; correctly handle 
  multiple numpy integer subtypes
  [#238](https://github.com/NickleDave/crowsetta/pull/238).

## 4.0.0.post2 -- 2022-06-25
### Changed
- [c6ba100](https://github.com/vocalpy/crowsetta/commit/c6ba100d7335a880f2e1dbf66f5673ef562f3cc5)
  Fix description and uri in pyproject.toml and crowsetta/__about__.py
- [f70828f](https://github.com/vocalpy/crowsetta/commit/f70828fc09102215ae9d8076f66a79d515db3388)
  Make README images link to raw GitHub files so they render on PyPI

## 4.0.0.post1 -- 2022-06-25
### Changed
- clean up README and make other doc fixes
  [#201](https://github.com/NickleDave/crowsetta/pull/201).
  Fixes [#199](https://github.com/NickleDave/crowsetta/issues/199).

## 4.0.0 -- 2022-06-25
### Added
- add Raven format
  [#164](https://github.com/NickleDave/crowsetta/pull/164).
  Fixes [#84](https://github.com/NickleDave/crowsetta/issues/84).
- add example data
  [#180](https://github.com/NickleDave/crowsetta/pull/180).
  Fixes [#90](https://github.com/NickleDave/crowsetta/issues/90).
- add examples to docstrings, using example data
  [#180](https://github.com/NickleDave/crowsetta/pull/180).
  Fixes [#158](https://github.com/NickleDave/crowsetta/issues/158).
- import `register_format` at top level of package, 
  to be able to just write `@crowsetta.register_format`
  [#181](https://github.com/NickleDave/crowsetta/pull/181).
  Fixes [#177](https://github.com/NickleDave/crowsetta/issues/177).
- add `'aud-txt'` format, for Audacity standard LabelTracks exported to .txt files
  [#183](https://github.com/NickleDave/crowsetta/pull/183).
  Fixes [#96](https://github.com/NickleDave/crowsetta/issues/96).
- add ability to extract example data to local file system;
  avoids need to use context manager returned by `importlib.resources` 
  to access the example data files.
  [#185](https://github.com/NickleDave/crowsetta/pull/185).
  Fixes [#184](https://github.com/NickleDave/crowsetta/issues/184).
- add logo
  [#198](https://github.com/NickleDave/crowsetta/pull/198).
  Fixes [#17](https://github.com/NickleDave/crowsetta/issues/17).

### Changed
- change `Annotation` class to represent both sequence-like 
  annotation formats and bounding box-like annotation formats
  [#164](https://github.com/NickleDave/crowsetta/pull/164).
  Resolves [#149](https://github.com/NickleDave/crowsetta/issues/149)
  and [#150](https://github.com/NickleDave/crowsetta/issues/150).
- re-design API, and rewrite annotation formats as classes
  [#161](https://github.com/NickleDave/crowsetta/pull/161).
  + Re-writing as classes fixes [#99](https://github.com/NickleDave/crowsetta/issues/99).
  + API re-design fixes [#120](https://github.com/NickleDave/crowsetta/issues/120).
  + Adds an `interface` sub-package that specifies an interface for two 
    types of annotations: *sequence-like* and *bounding-box like*.
    Fixes [#105](https://github.com/NickleDave/crowsetta/issues/105)
  + All existing annotation formats were sequence-like, and they now
    adhere to that interface; the classes are registered as sub-classes.
    + Some classes were additionally re-factored; e.g.
      + `'generic-seq'` now uses `pandas` (fixes [#63](https://github.com/NickleDave/crowsetta/issues/63))
      + `'simple-seq'` can parse multiple formats (fixes [#134](https://github.com/vocalpy/crowsetta/issues/134))
  + Formats themselves are now in a `formats` sub-package, 
    fixes [#109](https://github.com/NickleDave/crowsetta/issues/109)
  + Add better functions to list the formats in this sub-package
    (fixes [#92](https://github.com/NickleDave/crowsetta/issues/92)); 
    can call `crowsetta.formats.as_list` to get a list of shorthand string names,
    and `crowsetta.formats.by_name` with the shorthand string name to get back
    to the corresponding class.
  + `Transcriber.from_file` now returns an instance of an annotation format classes.
    Methods like `to_annot` can be called on this instance.
    This refactor greatly simplifies the `Transcriber` class while maintaining mostly 
    the same API (now need to chain calls like `Transcriber.from_file().to_annot()`, 
    or capture the returned annotation instance in a variable and use it instead).
    Fixes [#144](https://github.com/NickleDave/crowsetta/issues/144).
- convert docs to markdown and use `myst-parser`
  [#153](https://github.com/NickleDave/crowsetta/pull/153).
  Fixes [#151](https://github.com/NickleDave/crowsetta/issues/151).
- require Python >= 3.8 
  to adhere to [NEP-29]()
  [#168](https://github.com/NickleDave/crowsetta/pull/168).
  Fixes [#166](https://github.com/NickleDave/crowsetta/issues/166).
- rename `Annotation.audio_path` attribute to `notated_path`
  to be more general, e.g., because annotations can also annotate 
  a spectrogram
  [#169](https://github.com/NickleDave/crowsetta/pull/169).
  Fixes [#148](https://github.com/NickleDave/crowsetta/issues/148).
- rename `onset_ind` and `offset_ind` to `onset_sample` and 
  `offset_sample` for clarity
  [#174](https://github.com/NickleDave/crowsetta/pull/174).
  Fixes [#156](https://github.com/NickleDave/crowsetta/issues/156).
- rename first parameter of `from_file` method for all format classes 
  to `annot_path` for consistency.
  [#182](https://github.com/NickleDave/crowsetta/pull/182).
  Fixes [#178](https://github.com/NickleDave/crowsetta/issues/178).
- Revise documentation
  [#191](https://github.com/NickleDave/crowsetta/pull/191).
  Fixes [#152](https://github.com/NickleDave/crowsetta/issues/152) as well as 
  [#21](https://github.com/NickleDave/crowsetta/issues/21),
  [#35](https://github.com/NickleDave/crowsetta/issues/35),
  [#138](https://github.com/NickleDave/crowsetta/issues/138),
  and [#157](https://github.com/NickleDave/crowsetta/issues/157).
- have `formats.as_list` return list `sorted` (i.e., alphabetically)
  [#194](https://github.com/NickleDave/crowsetta/pull/194).
  Fixes [#187](https://github.com/NickleDave/crowsetta/issues/187).

## Fixed
- fix `crowsetta.formats.register_format` function added in 
  [#161](https://github.com/NickleDave/crowsetta/pull/161)
  and rewrite example custom annotation formats 
  to use it
  [#176](https://github.com/NickleDave/crowsetta/pull/176).
  Fixes [#119](https://github.com/NickleDave/crowsetta/issues/119).

## Removed
- remove `Stack` class -- was not being used
  [#172](https://github.com/NickleDave/crowsetta/pull/172).
  Fixes [#170](https://github.com/NickleDave/crowsetta/issues/170).
- remove deprecated `'csv'` format that was replaced by `'generic-seq'`
  [#173](https://github.com/NickleDave/crowsetta/pull/173).
  Fixes [#171](https://github.com/NickleDave/crowsetta/issues/171).
- remove `Meta` class -- no longer used
  [#193](https://github.com/NickleDave/crowsetta/pull/193).
  Fixes [#190](https://github.com/NickleDave/crowsetta/issues/190).

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