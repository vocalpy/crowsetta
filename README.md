# crowsetta
[![Build Status](https://travis-ci.com/NickleDave/crowsetta.svg?branch=master)](https://travis-ci.com/NickleDave/crowsetta)
[![Documentation Status](https://readthedocs.org/projects/crowsetta/badge/?version=latest)](https://crowsetta.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/159904494.svg)](https://zenodo.org/badge/latestdoi/159904494)
[![PyPI version](https://badge.fury.io/py/crowsetta.svg)](https://badge.fury.io/py/crowsetta)

`crowsetta` is a tool to work with any format for annotating vocalizations: speech, birdsong, 
mouse ultrasonic calls (insert your favorite animal vocalization here).
**The goal of** `crowsetta` **is to make sure that your ability to work with a dataset 
of vocalizations does not depend on your ability to work with any given format for 
annotating that dataset.** What `crowsetta` gives you is **not** yet another format for 
annotation (I promise!); instead you get some nice data types that make it easy to 
work with any format: namely, `Sequence`s made up of `Segment`s.

```Python
    >>> from crowsetta import Segment, Sequence
    >>> a_segment = Segment.from_keyword(
    ...     label='a',
    ...     onset_Hz=16000,
    ...     offset_Hz=32000,
    ...     file='bird21.wav'
    ...     )
    >>> list_of_segments = [a_segment] * 3
    >>> seq = Sequence(segments=list_of_segments)
    >>> print(seq)
    Sequence(segments=[Segment(label='a', onset_s=None, offset_s=None, onset_Hz=16000, 
    offset_Hz=32000, file='bird21.wav'), Segment(label='a', onset_s=None, offset_s=None, 
    onset_Hz=16000, offset_Hz=32000, file='bird21.wav'), Segment(label='a', onset_s=None, 
    offset_s=None, onset_Hz=16000, offset_Hz=32000, file='bird21.wav')])
```

You can load annotation from your format of choice into `Sequence`s of `Segment`s 
(most conveniently with the `Transcriber`, as explained below) and then use the 
`Sequence`s however you need to in your program.

For example, if you want to loop through the `Segment`s of each `Sequence`s to 
pull syllables out of a spectrogram, you can do something like this, very Pythonically:

```Python
   >>> syllables_from_sequences = []
   >>> for a_seq in seq:
   ...     seq_dict = seq.to_dict()  # convert to dict with 
   ...     spect = some_spectrogram_making_function(seq['file'])
   ...     syllables = []
   ...     for seg in seq.segments:
   ...         syllable = spect[:, seg.onset:seg.offset]  ## spectrogram is a 2d numpy array
   ...         syllables.append(syllable)
   ...     syllables_from_sequences.append(syllables)
```

As mentioned above, `crowsetta` provides you with a `Transcriber` that comes equipped
with convenience functions to do the work of converting for you. 

```Python
    from crowsetta import Transcriber
    scribe = Transcriber()
    seq = scribe.to_seq(file=notmat_files, format='notmat')
```

You can even easily adapt the `Transcriber` to use your own in-house format, like so:

```Python
    from crowsetta import Transcriber
    scribe = Transciber(user_config=your_config)
    scribe.to_csv(file_'your_annotation_file.mat',
                  csv_filename='your_annotation.csv')
```

## Features

- convert annotation formats to `Sequence` objects that can be easily used in a Python program
- convert `Sequence` objects to comma-separated value text files that can be read on any system
- load comma-separated values files back into Python and convert to other formats
- easily use with your own annotation format

You might find it useful in any situation where you want 
to share audio files of song and some associated annotations, 
but you don't want to require the user to install a large 
application in order to work with the annotation files.

## Getting Started
You can install with pip:
`$ pip install crowsetta`

To learn how to use `crowsetta`, please see the documentation at:  
<https://crowsetta.readthedocs.io/en/latest/index.html>

### Development Installation

Currently `crowsetta` is developed with `conda`.
To set up a development environment:
```
$ conda create crowsetta-dev
$ conda create -n crowsetta-dev python=3.6 numpy scipy attrs
$ conda activate crowsetta-dev
$ $ pip install evfuncs koumura
$ git clone https://github.com/NickleDave/crowsetta.git
$ cd crowsetta
$ pip install -e .
```


## Project Information

### Background

`crowsetta` was developed for two libraries:
- `hybrid-vocal-classifier` <https://github.com/NickleDave/hybrid-vocal-classifier>
- `vak` <https://github.com/NickleDave/vak>

Testing relies on the `Vocalization Annotation Formats Dataset` which you may find useful if you need
small samples of different audio files and associated annotation formats
- on Figshare: <https://figshare.com/articles/Vocalization_Annotation_Formats_Dataset/8046920>
- built from this GitHub repository: <https://github.com/NickleDave/vocal-annotation-formats>

### Support

If you are having issues, please let us know.

- Issue Tracker: <https://github.com/NickleDave/crowsetta/issues>

### Contribute

- Issue Tracker: <https://github.com/NickleDave/crowsetta/issues>
- Source Code: <https://github.com/NickleDave/crowsetta>

### CHANGELOG
You can see project history and work in progress in the [CHANGELOG](./doc/CHANGELOG.md)

### License

The project is licensed under the [BSD license](./LICENSE).

### Citation
If you use `crowsetta`, please cite the DOI:
[![DOI](https://zenodo.org/badge/159904494.svg)](https://zenodo.org/badge/latestdoi/159904494)