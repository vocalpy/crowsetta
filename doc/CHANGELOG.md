# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### added
- `Segment` class, attrs-based

### changed
- `Sequence` class is now attrs-based, has factory functions, is itself
just a list of `Segment`s

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