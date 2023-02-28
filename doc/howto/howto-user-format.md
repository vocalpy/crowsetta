---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(howto-user-format)=

# How to use crowsetta with your own annotation format

This section shows you how to use crowsetta for working with your
own annotation format for vocalizations (or some other format not
currently built into the library).

## Steps to using crowsetta with your own annotation format

Below we’ll walk through a case study for using crowsetta with your
annotation format. Here’s an outline of the steps we’ll go through:

1. get your annotations into some variables in Python (maybe you already
   wrote code to do this)
2. write a class that represents your format
3. register your new format by calling `crowsetta.register_format`
4. use your format with the `crowsetta.Transcriber` class to work with your annotations

If writing a class to represent your format sounds difficult, 
don't worry. We show you how and crowsetta gives you tools that 
make it easy. If you've written some Python code 
to work with your annotations before 
then you're probably already halfway done.

In this walkthrough we show you how to write a {ref}`sequence-like <formats-seq-like>` format.
By sequence-like, we mean a format 
that can be represented as a sequence of segments, where each segment has a start time, 
stop time, and label. Many common annotation formats for animal vocalizations 
are sequence-like.

```{note}
Sequence-like formats are one of the two types in crowsetta. 
The other is {ref}`bounding-box <formats-bbox-like>` formats, 
which annotate sound events with boxes, as the name implies. 
The steps for working with your own bounding box-like format 
would be exactly the same, 
except below where we talk about `crowsetta.Sequence`s, 
you should replace that with `crowsetta.Bbox`es.
```

## Case Study: the `BatLAB` format

Let’s say you work in the Schumacher lab, studying bat vocalizations.
The lab research specialist, Alfred, has spent years writing an
application in Labview to capture bat calls, called `SoNAR` (“Sound
and Neural Activity Recorder”). Alfred has also written a GUI in MATLAB
called `BatLAB` that lets you interactively annotate audio files
containing the bats’ calls, and saves the annotations in `.mat`
(MATLAB data) files.

You’ve started to work with Python to analyze your data, because you
like the data science and machine learning libraries. However, you find
yourself writing the same code over and over again to unpack the
annotations from the `.mat` files made by `BatLAB`. Every time you
use the code for a new analysis, you have to modify it slightly. The
code has some weird, hard-to-read lines to deal with the complicated
MATLAB `struct`s created by `BatLAB` and how they load into
Python. The code also has several repetitive steps to deal with the
idiosyncracies of how `SoNAR` and `BatLAB` save data: unit
conversion, data types, etcetera. You can’t change `BatLAB` or
`SoNAR` though, because that’s Alfred’s job, and everyone else’s code
that was written ten years ago (and still works!) expects those
idiosyncracies.

You know that it’s a good idea to turn the code you wrote into a
function (because you took part in a [Software
Carpentry](https://software-carpentry.org/) workshop and then you
read [this
paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510).)
You figured out which bits of the code will be common to all your
projects and you make that into a function, called `parse_batlab_mat`.
At first you just copy and paste it into all your projects. Then you
decide you also want to save everyone else in your lab the effort of
writing the same code, so you put the script on your lab’s Github page.
This is a step in the right direction, although `parse_batlab_mat`
gives you back a Python `list` of `dict`s, and you end up typing a
lot of things like:

```python
labels = annot_list[0]['seg_type']
onsets = annot_list[0]['seg_onsets']
offsets = annot_list[0]['seg_offsets']
```

Typing all those very similar `['keys']` in particular gets kind of
annoying and makes you wonder if you should spend your vacation learning
how to use one of those hacker text editors like `vim`.

But before you can worry about that, you get back reviews of your paper
in *PLOS Comp. Bio.* called “Pidgeon Bat: Emergence of Dialects in
Colonies of Multiple Bat Species”. Reviewer #3 doesn’t buy your
conclusions (and you are pretty sure from the way they write that it is
Oswald Cobblepot, professor emeritus of ethology at Metropolitan
University of Fruitville, Florida, and author of the seminal review from
1982, “Bat Calls: A Completely Innate Behavior Encoded Genetically”).
You want to share your data with the world, mainly to mollify reviewer
\#3. The problem is that this reviewer (if he is who you think he is)
only knows how to write Fortran code and is definitely not going to
figure out how to copy and use your function `parse_batlab_mat` so he
can run your analysis scripts and reproduce your figures for himself.

What you really want is to share your data and write your code in a way
that doesn’t depend on anyone knowing anything about `BatLAB`
or`SoNAR` and how those programs save data and annotations. This is
where crowsetta comes to your rescue.

Okay, now that we’ve set up some background for our case study, let’s go
through the steps we outlined above.

### 1. get your annotation into some variables in Python

Let’s look at this complicated data structure that we have our
annotation in. For this tutorial you'll need the 
file `bat1_annotation.mat` that you should be able to download 
from [this link](./bat1_annotation.mat) 
or by going to 
<https://github.com/vocalpy/crowsetta/blob/main/doc/howto/bat1_annotation.mat>.

The `BatLAB` GUI saves annotation into these `annotation.mat` 
files, with two variables in each mat file:
- `filenames`: a vector where each element is the name of an audio file
- `annotations`: a `struct` that has a record for each element in `filenames`, 
  and that record is the annotation corresponding 
  to the audio file with the same index in `filenames`

The following snippet will let you load and inspect the data:  

```{code-cell} ipython3
from scipy.io import loadmat
bat1_annotation = loadmat('bat1_annotation.mat')
print('Variables in .mat file:',
      [var for var in list(bat1_annotation.keys())
       if not var.startswith('__')],'\n'
     )
print(f"First 3 filenames:\n{bat1_annotation['filenames'][:,:3]}\n")
print(f"First annotation:\n{bat1_annotation['annotations'][:,0]}")
```

Below is the code you wrote to unpack the `.mat` files. Like we said
above, the code has some weird, hard-to-read lines to deal with the way
that the complicated MATLAB `struct`s created by `BatLAB` load
into Python, such as calling `tolist()` just to unpack an array, and
some logic to make sure the labels get loaded correctly into a numpy
array. And the code has several repetitive steps to deal with the
idiosyncracies of `SoNAR` and `BatLAB`, like converting the start
and stop times of the calls from seconds back to Hertz so you can find
those times in the raw audio files.

```{code-cell} ipython3
# %load parsebat.py
import numpy as np
from scipy.io import loadmat


def parse_batlab_mat(mat_file):
    """parse batlab annotation.mat file"""
    mat = loadmat(mat_file, squeeze_me=True)
    annot_list = []
    # annotation structure loads as a Python dictionary with two keys
    # one maps to a list of filenames,
    # and the other to a Numpy array where each element is the annotation
    # coresponding to the filename at the same index in the list.
    # We can iterate over both by using the zip() function.
    for filename, annotation in zip(mat['filenames'], mat['annotations']):
        # below, .tolist() does not actually create a list,
        # instead gets ndarray out of a zero-length ndarray of dtype=object.
        # This is just weirdness that results from loading complicated data
        # structure in .mat file.
        seg_start_times = annotation['segFileStartTimes'].tolist()
        seg_end_times = annotation['segFileEndTimes'].tolist()
        seg_types = annotation['segType'].tolist()
        if type(seg_types) == int:
            # this happens when there's only one syllable in the file
            # with only one corresponding label
            seg_types = np.asarray([seg_types])  # so make it a one-element list
        elif type(seg_types) == np.ndarray:
            # this should happen whenever there's more than one label
            pass
        else:
            # something unexpected happened
            raise ValueError("Unable to load labels from {}, because "
                             "the segType parsed as type {} which is "
                             "not recognized.".format(filename,
                                                      type(seg_types)))
        samp_freq = annotation['fs'].tolist()
        seg_start_times_Hz = np.round(seg_start_times * samp_freq).astype(int)
        seg_end_times_Hz = np.round(seg_end_times * samp_freq).astype(int)
        annot_dict = {
            'audio_file': filename,
            'seg_types': seg_types,
            'seg_start_times': seg_start_times,
            'seg_end_times': seg_end_times,
            'seg_start_times_Hz': seg_start_times_Hz,
            'seg_end_times_Hz': seg_end_times_Hz,
        }
        annot_list.append(annot_dict)

    return annot_list
```

When it runs on a file, you end up with an `annot_list` where each
item in the list is an `annot_dict` that contains the annotations for
a file, like this:

```python
annot_dict = {
    'seg_types': array([1, 1, 5, 2, ...]),
    'seq_start_times': array([0.00297619, 0.279125, 0.55564729,... ]),
    ... # end times, start and end times in Hertz
}
```

Again, as we said above, you turned your code into a function to make it
easier to use across projects:

```python
import numpy as np
from scipy.io import loadmat

def parse_batlab_mat(mat_file):
    """parse batlab annotation.mat file"""
    # code from above
    return annot_list
```

As we’ll see in a moment, all you need to do is take this code you
already wrote, and instead of returning your `list` of `dict`s,
you return a list of `Sequence`s.

+++

### 2. write a class that represents your format

Since we are dealing with a sequence-like format, 
what we ultimately want to do is convert the format into a `crowsetta.Sequence`, 
so that it acts like all the other sequence-like formats.

So before we even worry about writing a class, 
let's see how to make some `Sequence`s.

#### Use one of the `Sequence` “factory functions” to conveniently turn annotations in your format into `Sequence`s

First, to get the `Sequence`, we’ll use a “factory function”.
That means it’s a function built into the `Sequence` class that gives
us back a new instance of a `Sequence`. One such factory function is
`Sequence.from_keyword`. Here’s an example of using it with our `parsebat` code from above:

```{code-cell} ipython3
from parsebat import parse_batlab_mat
from crowsetta.sequence import Sequence

# you, using the function you already wrote
annot_list = parse_batlab_mat(mat_file='bat1_annotation.mat')

# you have annotation from one file in an "annot_dict"
annot_dict = annot_list[0]

a_sequence = Sequence.from_keyword(labels=annot_dict['seg_types'],
                                   onsets_s=annot_dict['seg_start_times'],
                                   offsets_s=annot_dict['seg_end_times'],
                                   onset_samples=annot_dict['seg_start_times_Hz'],
                                   offset_samples=annot_dict['seg_end_times_Hz'])
print("a_sequence:\n", a_sequence)
```

Okay now that we saw how to make a `crowsetta.Sequence` from our annotations 
loaded into Python and `numpy` data types, let's actually start writing our class.

+++

#### Start to write the class

```{note}
If the idea of writing a class is completely new to you, 
we suggest reading up on that first. 

A very good place to start would be 
[Think Python](https://greenteapress.com/wp/think-python-2e/)
by Alan Downey, 
in particular the 
[chapter on Classes and objects](https://greenteapress.com/thinkpython2/html/thinkpython2016.html)
```

The first thing we want to do is just sketch out a class 
that will represent the annotations loaded into good old-fashioned Python data types. 
That way when we make a new instance of this class, 
it will contain the annotations we loaded from a single file. 
To make a class that holds our data, we use 
the [`attrs` library](https://www.attrs.org/en/stable/). 
Then we later add a couple methods to this class that do things 
like turn the annotations into `crowsetta.Sequence`s and `crowsetta.Annotation`s.

To start writing the class, copy one of the existing classes in crowsetta, by looking at its code.  
Here's a stub of a `Batlab` class that we wrote by 
copying the [`'yarden'` format](https://github.com/vocalpy/crowsetta/blob/main/src/crowsetta/formats/seq/yarden.py) and changing a couple things -- we'll explain what we changed below.

+++

```python
# %load -r 1-10,14-48 batlab.py
import pathlib
from typing import ClassVar

import attr
import numpy as np
import scipy.io

from crowsetta import Sequence, Annotation
from crowsetta.typing import PathLike
import crowsetta
@crowsetta.interface.SeqLike.register
@attr.define
class Batlab:
    """Example custom annotation format"""
    name: ClassVar[str] = 'batlab'
    ext: ClassVar[str] = '.mat'

    annotations: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    audio_paths: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path = attr.field(converter=pathlib.Path)

    @classmethod
    def from_file(cls,
                  annot_path: PathLike):
        """load BatLAB annotations from .mat file

        Parameters
        ----------
        mat_path : str, pathlib.Path
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        annot_mat = scipy.io.loadmat(annot_path, squeeze_me=True)

        audio_paths = annot_mat['filenames']
        annotations = annot_mat['annotations']
        if len(audio_paths) != len(annotations):
            raise ValueError(
                f'list of filenames and list of annotations in {mat_path} do not have the same length'
            )

        return cls(annotations=annotations,
                   audio_paths=audio_paths,
                   annot_path=annot_path)
```

+++

This might seem overwhelming at first, but we only changed a few things.

To tell crowsetta how to handle our format,
we need to change exactly two of the class attributes: 
(1) the `name` and (2) the `ext`.

The `name` attribute is the shorthand string name that we use to refer to our format, 
for example when we call `crowsetta.format.by_name` or we make a new `Transcriber`, 
passing in this `name` as the `format` argument (like so: `scribe = crowsetta.Transcriber(format='name')`).

The `ext` attribute tells crowsetta what a valid file extension is for this annotation format: 
is it a `.mat` file or a `.csv` file? Can it be both `('txt', 'csv')`? 
We then use this attribute in other places in the class, 
like when we write a `from_file` method, to validate the file name that gets passed into that method.

Re-writing the `from_file` method is the other thing we changed. 
Notice that this `from_file` method is basically 
the few lines from our `parse_batlab` function, 
where we unpack the `filenames` and the `annotations` from the `.mat` file. 
We don't loop through them to put them in a Python `dict` though. 
Instead we assign them to the class' attributes `audio_paths` and `annotations`. 
You don't have to completely understand what's going on here; 
basically we are writing our own "factory function" (like the one we used for `Sequence`s above) 
that gives us a new instance of our `Batlab` class 
that will have the specific annotations from a file loaded into it. 
(Writing a factory method is consistent with advice 
from [the `attrs` docs](https://www.attrs.org/en/stable/init.html?highlight=classmethod#initialization)). 
To achieve this we use the `@classmethod` decorator and pass in `cls` as the first argument (by convention) 
that we can then call to create a new instance. 
(To learn more about `classmethod`s see https://realpython.com/instance-class-and-static-methods-demystified/).

+++

#### Now write a `to_seq` method that converts the annotations to `crowsetta.Sequence`s

Again, you pretty much already wrote this. Just take your
`parse_batlab_mat` function from above and change a couple lines.
First, you’re going to return a list of sequences instead of your
`annot_list` from before. You probably want to make that explicit in
your function.

+++

```python
# %load -r 51-96 batlab.py
def to_seq(self):
    """unpack BatLAB annotation into list of Sequence objects

        example of a function that unpacks annotation from
        a complicated data structure and returns the necessary
        data as a Sequence object

        Returns
        -------
        seqs : list
            of Sequence objects
        """
        seqs = []
        # annotation structure loads as a Python dictionary with two keys
        # one maps to a list of filenames,
        # and the other to a Numpy array where each element is the annotation
        # coresponding to the filename at the same index in the list.
        # We can iterate over both by using the zip() function.
        for filename, annotation in zip(self.audio_paths, self.annotations):
            # below, .tolist() does not actually create a list,
            # instead gets ndarray out of a zero-length ndarray of dtype=object.
            # This is just weirdness that results from loading complicated data
            # structure in .mat file.
            onsets_s = annotation['segFileStartTimes'].tolist()
            offsets_s = annotation['segFileEndTimes'].tolist()
            labels = annotation['segType'].tolist()
            if type(labels) == int:
                # this happens when there's only one syllable in the file
                # with only one corresponding label
                seg_types = np.asarray([seg_types])  # so make it a one-element list
            elif type(labels) == np.ndarray:
                # this should happen whenever there's more than one label
                pass
            else:
                # something unexpected happened
                raise ValueError("Unable to load labels from {}, because "
                                 "the segType parsed as type {} which is "
                                 "not recognized.".format(audio_path,
                                                          type(seg_types)))
            samp_freq = annotation['fs'].tolist()

            seq = Sequence.from_keyword(labels=labels,
                                        onsets_s=onsets_s,
                                        offsets_s=offsets_s)
            seqs.append(seq)
        return seqs
```

+++

Then at the end of your main loop, instead of making your
`annot_dict`, you’ll make a new `Sequence` from each file using the
`from_keyword` factory function, append the new `Sequence` to your
`seq_list`, and then finally return that `list` of `Sequence`s.

+++

```python
# %load -r 92-95 batlab.py
seq = Sequence.from_keyword(labels=labels,
                            onsets_s=onsets_s,
                            offsets_s=offsets_s)
seqs.append(seq)
```

+++

If this still feels too wordy and repetitive for you, you can put
``segFileStartTimes``, ``segFileEndTimes``, et al., into a Python
``dict`` with ``keys`` corresponding to the parameters for
``Segment.from_keyword``:


```python
annot_dict = {
    'file': filename,
    'onsets_s': annotation['segFileStartTimes'].tolist(),
    'offsets_s': annotation['segFileEndTimes'].tolist()
    'labels': seg_types
}
```

Note here that you only have to specify the onsets an offsets of
segments *either* in seconds or in sample number (but you can specify 
both if you want).

and then use another factory function, `Sequence.from_dict`, to
create the `Sequence`.
```python
seq_list.append(Sequence.from_dict(annot_dict))
```

Now you have a `Batlab` class with a `to_seq` function, 
that takes annotation files and return
`Sequence`s.
You want to and put this in a
file that ends with `.py`, e.g., `batlab.py`
(otherwise known as a Python *module*). 
To see the entire example, check out the [batlab.py](./batlab.py) file
(and compare it with [parsebat.py](./parsebat.py)).

+++

### 3. Register your new format by calling `crowsetta.register_format`

To make it so that crowsetta knows about your format, 
you call the `crowsetta.register_format` function 
and pass in the class you have written.

After you do this, you should see that the shorthand string `name` 
that you defined for the class appears in the `list` 
returned when you call `crowsetta.formats.as_list()`.

```{code-cell} ipython3
import crowsetta
import batlab

crowsetta.register_format(batlab.Batlab)

crowsetta.formats.as_list()

formats_list = crowsetta.formats.as_list()
assert batlab.Batlab.name in formats_list  # no AsssertionError, because `batlab` is in the list
```

#### Use `crowsetta.register_format` as a decorator

Instead of calling `crowsetta.register_format` "manually", 
you can use it as a decorator, 
that causes it to get registered automatically when you import the module. 

To use `crowsetta.register_format` as a decorator, 
we write it with the `@` symbol at the top of our class:

```python
@crowsetta.formats.register_format
@crowsetta.interface.SeqLike.register
@attr.define
class Batlab:
    """Example custom annotation format"""
    name: ClassVar[str] = 'batlab'
    ext: ClassVar[str] = '.mat'
```

(If you're unfamiliar with decorators, 
check out this primer: https://realpython.com/primer-on-python-decorators/)

This works because decorators are executed at import time. 
Notice we also used other decorators, another from crowsetta 
that registers our class as sequence-like, 
and one from `attrs` that helps us easily define a class.
You need to make sure that `reigster_format` the outermost decorator, 
because decorators are executed "inside-out".  

Here's just the top few lines from an updated version of our class 
where we apply `crowsetta.register_format` as a decorator.

+++

```python
# %load -r 1-22 batlab.py
import pathlib
from typing import ClassVar

import attr
import numpy as np
import scipy.io

from crowsetta import Sequence, Annotation
from crowsetta.typing import PathLike
import crowsetta


@crowsetta.formats.register_format
@crowsetta.interface.SeqLike.register
@attr.define
class Batlab:
    """Example custom annotation format"""
    name: ClassVar[str] = 'batlab'
    ext: ClassVar[str] = '.mat'

    annotations: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    audio_paths: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
```

+++

### 4. Use your format with the `crowsetta.Transcriber` class to work with your annotations

If you have worked with `Crowsetta` already, or gone through the
tutorial, you know that we can work with a `Transcriber` that does the
work of making `Sequence`s of `Segment`s from annotation files
for us. We create a new instance of a `Transcriber` by writing
something like this:

```python
scribe = crowsetta.Transcriber(format='name')
```

You will do the same thing here:

```python
scribe = crowsetta.Transcriber(format='batlab')
```

Here’s what it looks like to do all of that in a few lines of code:

```{code-cell} ipython3
import crowsetta
import batlab  # gets registered automatically when we import, because of decorator

scribe = crowsetta.Transcriber(format='batlab')

seq_list = scribe.from_file('bat1_annotation.mat').to_seq()
```

And now, just like you do with the built-in formats, you get back a list
of `Sequence`s from your format:

```{code-cell} ipython3
print(f'First item in seq_list: {seq_list[0]}')
print(f'First segment in first sequence:\n{seq_list[0].segments[0]}')
```

## Summary

Now you have seen in detail the process of working with your own
annotation format in `Crowsetta`. Here’s a review of the steps, with
some code snippets worked in to tie it all together:

1. get your annotations into some variables in Python (maybe you already
   wrote code to do this)
2. write a class that represents your format
3. register your new format by calling `crowsetta.register_format`
4. use your format with the `crowsetta.Transcriber` class to work with your annotations


steps 1-3 will give you something like this in a file named something
like `myformat.py`
```python
import pathlib
from typing import ClassVar

import attr

from crowsetta import Sequence, Annotation
from crowsetta.typing import PathLike
import crowsetta


@crowsetta.formats.register_format
@crowsetta.interface.SeqLike.register
@attr.define
class MyFormat:
    """Example custom annotation format"""
    name: ClassVar[str] = 'myformat'
    ext: ClassVar[str] = '.csv'

    ...
    
    @classmethod
    def from_file(cls, annot_path):
        ...
        return cls(annotations, annot_path)

    ...
    def to_seq():
        seq_list = []
        for annotation in self.annotations:
        # load annotation into some Python variables, e.g. a dictionary
            annot_dict = magic_annotation_unpacking_function(annotation)
            seq = Sequence.from_dict(annot_dict)
            seq_list.append(seq)
        return seq_list
    
    def to_annot():
        seqs = self.to_seq()
        annots = []
        for seq in seqs:
            annots.append(Annotation(seq=seq, annot_path=self.annot_path))
        return annots
```

and then as in step 4, you will be able to 
make a `Transcriber` that knows to use this class when you tell
it you want to turn your annotation files into `Sequence`s or `Annotation`s.

```python
scribe = crowsetta.Transcriber(format='myformat')
myformat = scribe.from_file('my-annotations.txt')
seq_list = myformat.to_seq()
```
