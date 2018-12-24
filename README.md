# crowsetta
[![Build Status](https://travis-ci.com/NickleDave/crowsetta.svg?branch=master)](https://travis-ci.com/NickleDave/crowsetta)
[![Documentation Status](https://readthedocs.org/projects/crowsetta/badge/?version=latest)](https://crowsetta.readthedocs.io/en/latest/?badge=latest)

A tool to work with any format for annotating birdsong.
**The goal of** `crowsetta` **is to make sure that your ability to work with a 
birdsong dataset does not depend on your ability to work with any given format for 
annotating that dataset.**

```python
    from crowsetta import Transcriber
    scribe = Transcriber(user_config=your_config)
    scribe.to_csv(file_'your_annotation_file.mat',
                  csv_filename='your_annotation.csv')
```

## Features

- convert annotation formats to ``Sequence`` objects that can be easily used in a Python program
- convert ``Sequence`` objects to comma-separated value text files that can be read on any system
- load comma-separated values files back into Python and convert to other formats
- easily use with your own annotation format


`crowsetta` is used by the `hybrid-vocal-classifier` and `songdeck` 
libraries.

You might find it useful in any situation where you want 
to share audio files of song and some associated annotations, 
but you don't want to require the user to install a large 
application in order to work with the annotation files.

## Getting Started
You can install with pip:
`$ pip install crowsetta`

To learn how to use `crowsetta`, please see the documentation at:  
<https://crowsetta.readthedocs.io/en/latest/index.html>

## Project Information

### Support

If you are having issues, please let us know.

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues

### Contribute

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues
- Source Code: https://github.com/NickleDave/crowsetta

### CHANGELOG
You can see project history and work in progress in the [CHANGELOG](./doc/CHANGELOG.md)

### License

The project is licensed under the [BSD license](./LICENSE).

### Citation
If you use `crowsetta`, please cite the DOI:
[![DOI](https://zenodo.org/badge/159904494.svg)](https://zenodo.org/badge/latestdoi/159904494)