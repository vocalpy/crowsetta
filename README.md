# crowsetta
[![Build Status](https://travis-ci.com/NickleDave/crowsetta.svg?branch=master)](https://travis-ci.com/NickleDave/crowsetta)
[![Documentation Status](https://readthedocs.org/projects/crowsetta/badge/?version=latest)](https://crowsetta.readthedocs.io/en/latest/?badge=latest)

`crowsetta` is a tool to work with any format for annotating birdsong.
**The goal of** `crowsetta` **is to make sure that your ability to work with a dataset 
of birdsong does not depend on your ability to work with any given format for 
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