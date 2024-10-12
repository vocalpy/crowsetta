---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

::::{grid}
:reverse:
:gutter: 2 1 1 1
:margin: 4 4 1 1

:::{grid-item}
:columns: 8
:class: sd-fs-3

A Python tool to work with any format for annotating 
animal sounds and bioacoustics data.
:::

:::{grid-item}
:columns: 4

```{image} ./_static/crowsetta-secondary-logo.png
:width: 150px
```
:::

::::

crowsetta provides a Pythonic way to work with annotation formats 
for animal sounds and bioacoustics data. 
Files in these formats are created by
applications that enable users to annotate audio and/or spectrograms. 
Such annotations typically include the times when sound events start and stop, 
and labels that assign each sound to some set of classes 
chosen by the annotator.
crowsetta has built-in support for many widely used {ref}`formats <formats-index>` 
such as {ref}`Audacity label tracks <aud-seq>`, 
{ref}`Praat .TextGrid files <textgrid>`, 
and {ref}`Raven .txt files <raven>`.
The images below show examples of the two families of annotation formats 
built into crowsetta, sequence-like formats and bounding box-like formats.

:::{figure} _static/example-textgrid-for-index.png
---
width: 90%
figclass: margin-caption
alt: example spectrogram showing Bengalese finch song with Praat TextGrid annotations indicated as segments underneath
name: example-textgrid-for-index
---
**Spectrogram of the song of a Bengalese finch 
with syllables annotated as segments underneath. 
Annotations parsed by crowsetta 
from a file in the {ref}`Praat TextGrid <textgrid>` format.
Example song from 
[Bengalese finch song dataset](https://osf.io/r6paq/), 
Tachibana and Morita 2021, adapted under 
CC-By-4.0 License.**
:::

:::{figure} _static/example-raven-for-index.png
---
width: 90%
figclass: margin-caption
alt: example spectrogram from field recording with Raven annotations of birdsong indicated as rectangular bounding boxes
name: example spectrogram with Raven annotations
---
**Spectrogram of a field recording 
with annotations of songs of different bird species 
indicated as bounding boxes.
Annotations parsed by crowsetta 
from a file in the {ref}`Raven Selection Table <raven>` format.
Example song from 
["An annotated set of audio recordings of Eastern North American birds containing frequency, time, and species information"](https://esajournals.onlinelibrary.wiley.com/doi/full/10.1002/ecy.3329), 
Chronister et al., 2021, adapted under 
CC0 1.0 License.**
:::

# About

<h3>What can you do with crowsetta?</h3>

- Analyze your annotations with Python scripts
- Develop Python libraries that can work with a wide array of annotation formats
- Convert your annotations to a file format that's easy for you to share and for anyone to load, 
  like a single csv file
- Convert your annotations into a format that's needed to train machine learning models

<h3>Who would want to use crowsetta?</h3>
Anyone that works with animal sounds 
or other bioacoustics data that is annotated in some way.
Maybe you are a neuroscientist trying to figure out how songbirds learn their song,
or why mice emit ultrasonic calls. Or maybe you're an ecologist studying dialects of finches
distributed across Asia, or maybe you are a linguist studying accents in the
Caribbean, or a speech pathologist looking for phonetic changes that indicate early onset
Alzheimer's disease. crowsetta makes it easier for you to work with 
your annotations in Python, regardless of the format.  

It was originally developed for use with the libraries 
[vak](https://vak.readthedocs.io/en/latest/)
and
[hybrid-vocal-classifier](https://hybrid-vocal-classifier.readthedocs.io/en/latest/).

[hybrid-vocal-classifier]: https://hybrid-vocal-classifier.readthedocs.io/en/latest/
[pandas]: https://pandas.pydata.org/
[vak]: https://github.com/vocalpy/vak

# Installation 

```{eval-rst}

.. tabs::

   .. code-tab:: shell with ``pip``

         pip install crowsetta

   .. code-tab:: shell with ``conda``

         conda install crowsetta -c conda-forge

```

# Features

With crowsetta, you can:
* work with your annotations in Python,
  taking advantage of built-in support 
  for many widely used {ref}`formats <formats-index>`
  such as {ref}`Audacity label tracks <aud-seq>`, 
  {ref}`Praat .TextGrid files <textgrid>`,
  and {ref}`Raven .txt files <raven>`.
* work with any format by remembering just one class:  
  `annot = crowsetta.Transcriber(format='format').from_file('annotations.ext')`
  - no need to remember different functions for different formats
  - great for interactive analysis and scripts
* when needed, use classes that represent the formats 
  to develop software libraries that access annotations through 
  class attributes and methods 
* convert annotations to widely-used, easy to access file formats
  (like csv files and json files) that anyone can work with
* work with custom annotation formats that are not built in 
  by writing simple classes, leveraging abstractions in crowsetta 
  that can represent a wide array of annotation formats

<h3>Built-in support for many widely-used formats</h3>

crowsetta has built-in support for many widely used {ref}`formats <formats-index>` 
such as {ref}`Audacity label tracks <aud-seq>`, 
{ref}`Praat .TextGrid files <textgrid>`, 
and {ref}`Raven .txt files <raven>`.

Here is an example of loading an example {ref}`Praat .TextGrid <textgrid>` file:

```{code-cell} ipython3
import crowsetta
path = crowsetta.example('AVO-maea-basic', return_path=True)
a_textgrid = crowsetta.formats.seq.TextGrid.from_file(path)
print(
    f"`a_textgrid` is a {type(a_textgrid)}"
)
print(
    "The first five intervals from the interval tier in `a_textgrid`:\n"
    f"{a_textgrid.tiers[1].intervals[:5]}"
)
```

Instead of writing out the class name, 
each format can also be referred to by a shorthand string name:

```{code-cell} ipython3
import crowsetta
path = crowsetta.example('AVO-maea-basic', return_path=True)
a_textgrid = crowsetta.formats.by_name('textgrid').from_file(path)
print(f"`a_textgrid` is a {type(a_textgrid)} (even when we load it with `formats.by_name`)")
```

The shorthand string names of built-in format can be listed 
by calling `crowsetta.formats.as_list()`:

```{code-cell} ipython3
import crowsetta
crowsetta.formats.as_list()
```

<h3>Load annotations from any format, using just one class</h3>

To make things even simpler, you only need to remember a single class,
``crowsetta.Transcriber``,  that you can use to work with any format, 
given the format's shorthand string name.
The class also makes it easier to operate on many annotation files all at once.

Here is an example of using ``crowsetta.Transcriber`` to load 
multiple annotation files.  
This class can be used to write succinct scripts for data processing, 
or even to write applications that work with multiple annotation formats.

```{code-cell} ipython3
:tags: [remove-cell]

!curl --no-progress-meter -L 'https://ndownloader.figshare.com/files/9537253' -o './data/sober.repo1.gy6or6.032612.tar.gz'
```

```{code-cell} ipython3
:tags: [remove-cell]

import shutil
shutil.unpack_archive('./data/sober.repo1.gy6or6.032612.tar.gz', './data/')
```

```{code-cell} ipython3
annotation_files = [
    './data/032612/gy6or6_baseline_260312_0810.3440.cbin.not.mat',
    './data/032612/gy6or6_baseline_260312_0810.3442.cbin.not.mat',
    './data/032612/gy6or6_baseline_260312_0811.3453.cbin.not.mat'
]
from crowsetta import Transcriber
scribe = Transcriber(format='notmat')
seqs = [scribe.from_file(annotation_file).to_seq() 
        for annotation_file in annotation_files]
print(f"Loading {len(seqs)} sequence-like annotations")
print(f"Sequence 1:\n{seqs[0]}")
```

<h3>Write readable code, using classes that represent annotation formats</h3>

Although it is convenient to use the `Transcriber` class, 
it can also be helpful to be very clear, 
especially when writing code that is read and used by others, 
such as libraries developed by a team of research software engineers.
To help make code readable and to make intent explicit, 
crowsetta also provides classes for each format.

Here's an example script written using one of the built-in 
annotation formats, to make spectrograms of all the annotated 
syllables in a bout of bird song.
Notice that we explicitly access the `segments` attribute 
of a `sequence`

```python
import librosa
import numpy as np

import crowsetta

# load an example annotation file
path = crowsetta.example('Annotation.xml', return_path=True)
# in the next line we use the class, to make it absolutely clear which format we are working with
birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(path)
annots = birdsongrec.to_annot()  # returns a list of `crowsetta.Annotation`s

syllables_spects = []
for annot in annots:
    # get name of the audio file associated with the Sequence
    audio_path = annot.notated_path
    # then create a spectrogram from that audio file
    y, sr = librosa.load(audio_path, sr=None)
    D = librosa.stft(y, n_fft=512, hop_length=256, win_length=512)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    syllables = []
    for segment in annot.seq.segments:
        ## spectrogram is a 2d numpy array so we index into using onset and offset from segment
        syllable = S_db[:, segment.onset_s:segment.offset_s]
        syllables.append(syllable)
    syllables_spects.append(syllables)
```

+++

<h3>Convert annotations to common file formats like csv files that anyone can work with</h3>

crowsetta makes it easier to share data 
by converting formats to plain text files, 
such as a csv (comma-separated values) file.

Here is an example of converting a common format 
to a generic sequence format that can then be saved to 
a csv file.

```{code-cell} ipython3
import crowsetta
path = crowsetta.example('Annotation.xml', return_path=True)
birdsongrec = crowsetta.formats.by_name('birdsong-recognition-dataset').from_file(path)
annots = birdsongrec.to_annot(samplerate=32000)  # returns a list of `crowsetta.Annotation`s
# the 'generic-seq' format can write csv files from `Annotation`s with `Sequence`s.
generic_seq = crowsetta.formats.by_name('generic-seq')(annots=annots)
generic_seq.to_file(annot_path='./data/birdsong-rec.csv')
```

We load the csv into a pandas `DataFrame` to inspect the first few lines.

```{code-cell} ipython3
import pandas as pd
df = pd.read_csv("./data/birdsong-rec.csv")

from IPython.display import display
display(df.head(10))
```

Now that you have that csv file, you can load it into a pandas `DataFrame` 
or an Excel spreadsheet or an SQLite database, or whatever you want.

You might find this useful in any situation where you want to share audio files of
song and some associated annotations, but you don't want to require the user to
install a large application in order to work with those annotation files.

For more detail and examples, please see 
{ref}`howto-convert-to-generic-seq`

+++

<h3>Write custom classes for formats that are not built in, and then register them</h3>

You can even easily tell the `Transcriber` to use your own in-house format, like so:

```python
import crowsetta

import MyFormatClass

crowsetta.register_format(MyFormatClass)
```

For more about how that works, please see {ref}`howto-user-format`.

# Getting Started

If you are new to the library, start with {ref}`tutorial`.

To see an example of using crowsetta to work with your own annotation format,
see {ref}`howto-user-format`.

```{toctree}
:hidden: true
:maxdepth: 2

tutorial
howto
formats/index
api/index
development/index
```

# Support

To report a bug or request a feature (such as a new annotation format), 
please use the issue tracker on GitHub:  
<https://github.com/vocalpy/crowsetta/issues>

To ask a question about crowsetta, discuss its development, 
or share how you are using it, 
please start a new topic on the VocalPy forum 
with the crowsetta tag:  
<https://forum.vocalpy.org/>

# Contribute

- Issue Tracker: <https://github.com/vocalpy/crowsetta/issues>
- Source Code: <https://github.com/vocalpy/crowsetta>

# License

The project is licensed under the
[BSD license](https://github.com/vocalpy/crowsetta/blob/master/LICENSE).

# CHANGELOG

You can see project history and work in progress in the
[CHANGELOG](https://github.com/vocalpy/crowsetta/blob/main/doc/CHANGELOG.md).

# Citation

If you use crowsetta, please cite the DOI:

```{image} https://zenodo.org/badge/159904494.svg
:target: https://zenodo.org/badge/latestdoi/159904494
```
