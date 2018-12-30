
.. _howto-user-format:

**How to use** ``crowsetta`` **with your own annotation format**
================================================================

This section shows you how to use ``crowsetta`` for working with your
own annotation format for vocalizations (or some other format not
currently built into the library).

You can get the Jupyter notebook for this section by going to
https://github.com/NickleDave/crowsetta and clicking on the big green
“Clone or Download” button on the right side of the screen. You can then
find this notebook and others in the ``crowsetta/notebooks/`` directory.

Steps to using ``crowsetta`` with your own annotation format
------------------------------------------------------------

Below we’ll walk through a case study for using ``crowsetta`` with your
annotation format. Here’s an outline of the steps we’ll walk through:

1. use the ``Sequence`` “factory function” (we’ll explain what that
   means) to conveniently turn annotations in your format into
   ``Sequence``\ s
2. create a function that uses this code to take annotation files as an
   argument, and return ``Sequence``\ s
3. make a ``Transcriber`` that knows to use this function when you tell
   it you want to turn your annotation files into ``Sequence``\ s
4. use the ``to_seq`` method of the ``Transcriber`` that you make to
   turn your annotation files into ``Sequence``\ s that you can use in
   Python code for your analysis
5. use the ``to_csv`` method to share your annotation in a simple text
   file that others can use without having to know about the format

Case Study: the ``BatLAB`` format
---------------------------------

Let’s say you work in the Schumacher lab, studying bat vocalizations.
The lab research specialist, Alfred, has spent years writing an
application in Labview to capture bat calls, called ``SoNAR`` (“Sound
and Neural Activity Recorder”). Alfred has also written a GUI in MATLAB
called ``BatLAB`` that lets you interactively annotate audio files
containing the bats’ calls, and saves the annotations in ``.mat``
(MATLAB data) files.

You’ve started to work with Python to analyze your data, because you
like the data science and machine learning libraries. However, you find
yourself writing the same code over and over again to unpack the
annotations from the ``.mat`` files made by ``BatLAB``. Every time you
use the code for a new analysis, you have to modify it slightly. The
code has some weird, hard-to-read lines to deal with the way that the
complicated MATLAB ``struct``\ s created by ``BatLAB`` load into Python.
The code also has several repetitive steps to deal with the
idiosyncracies of how ``SoNAR`` and ``BatLAB`` save data. You can’t
change ``BatLAB`` or ``SoNAR`` though, because that’s Alfred’s job, and
everyone else’s code that was written ten years ago (and still works!)
expects those idiosyncracies.

You know that it’s a good idea to turn the code you wrote into a
function (because you took part in a `Software
Carpentry <https://software-carpentry.org/>`__ workshop and then you
read `this
paper <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>`__.)
You figured out which bits of the code will be common to all your
projects (the bits above) and you make that into a function, called
``parse_batlab_mat``. At first you just copy and paste it into all your
projects. Then you decide you also want to save everyone else in your
lab the effort of writing the same code, so you put the script on your
lab’s Github page. This is a step in the right direction, although
``parse_batlab_mat`` gives you back a Python ``list`` of ``dict``\ s,
and you end up typing a lot of things like:

.. code:: python

   labels = annot_list[0]['seg_type']
   onsets = annot_list[0]['seg_onsets']
   offsets = annot_list[0]['seg_offsets']

This gets kind of annoying and makes you wonder if you should spend your
vacation learning how to use one of those hacker text editors like
``vim``.

But before you can worry about that, you get back reviews of your paper
in *PLOS Comp. Bio.* called “Pidgeon Bat: Emergence of Dialects in
Colonies of Multiple Bat Species”. Reviewer #3 doesn’t buy your
conclusions (and you are pretty sure from the way they write that it is
Oswald Cobblepot, professor emeritus of ethology at Metropolitan
University of Fruitville, Florida, and author of the seminal review from
1982, “Bat Calls: A Completely Innate Behavior Encoded Genetically”).
You want to share your data with the world, mainly to mollify reviewer
#3. The problem is that this reviewer (if he is who you think he is)
only knows how to write Fortran code and is definitely not going to
figure out how to copy and use your function ``parse_batlab_mat`` so he
can run your analysis scripts and reproduce your figures for himself.

What you really want is to share your data and write your code in a way
that doesn’t depend on anyone knowing anything about ``BatLAB``
or\ ``SoNAR`` and how those programs save data and annotations. This is
where ``crowsetta`` comes to your rescue.

Okay, now that we’ve set up some background for our case study, let’s go
through the steps we outlined above.

1. use the ``Sequence`` “factory function” to conveniently turn annotations in your format into Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Let’s look at this complicated data structure that we have our
  annotation in. The ``BatLAB`` GUI saves annotation into
  ``annotation.mat`` files with two variables:
| - ``filenames``: a vector where each element is the name of an audio
  file - ``annotations``: a ``struct`` that has a record for each
  element in ``filenames``, and that record is the annotation
  corresponding to the audio file with the same index in ``filenames``

.. code:: ipython3

    from scipy.io import loadmat
    bat1_annotation = loadmat('bat1_annotation.mat')
    print('variables in .mat file:',
          [var for var in list(bat1_annotation.keys())
           if not var.startswith('__')]
         )


.. parsed-literal::

    variables in .mat file: ['filenames', 'annotations']


Below is the code you wrote to unpack the ``.mat`` files. Like we said
above, the code has some weird, hard-to-read lines to deal with the way
that the complicated MATLAB ``struct``\ s created by ``BatLAB`` load
into Python, such as calling ``tolist()`` just to unpack an array, and
some logic to make sure the labels get loaded correctly into a numpy
array. And the code has several repetitive steps to deal with the
idiosyncracies of ``SoNAR`` and ``BatLAB``, like converting the start
and stop times of the calls from seconds back to Hertz so you can find
those times in the raw audio files.

.. code:: ipython3

    # %load -r 7-8,14-46 parsebat.py
    mat = loadmat(mat_file, squeeze_me=True)
    annot_list = []
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

When it runs on a file, you end up with an ``annot_list`` where each
item in the list is an ``annot_dict`` that contains the annotations for
a file, like this:

.. code:: python

   annot_dict = {
       'seg_types': array([1, 1, 5, 2, ...]),
       'seq_start_times': array([0.00297619, 0.279125, 0.55564729,... ]),
       ... # end times, start and end times in Hertz
   }

Again, as we said above, you turned your code into a function to make it
easier to use across projects:

.. code:: python

   import numpy as np
   from scipy.io import loadmat

   def parse_batlab_mat(mat_file):
       """parse batlab annotation.mat file"""
       # code from above
       return annot_list

As we’ll see in a moment, all you need to do is take this code you
already wrote, and instead of returning your ``list`` of ``dict``\ s,
you return a list of ``Sequence``\ s.

First, to get the ``Sequence``, we’ll use a “factory function”, which
just means it’s a function built into the ``Sequence`` class that gives
us back an instance of a ``Sequence``. Let’s see how you would make a
``Sequence`` using the ``from_keyword`` function.

.. code:: ipython3

    from parsebat import parse_batlab_mat
    from crowsetta.classes import Sequence
    
    annot_list = parse_batlab_mat(mat_file='bat1_annotation.mat')
    
    annot_dict = annot_list[0]
    
    a_sequence = Sequence.from_keyword(labels=annot_dict['seg_types'],
                                       onsets_s=annot_dict['seg_start_times'],
                                       offsets_s=annot_dict['seg_end_times'],
                                       onsets_Hz=annot_dict['seg_start_times_Hz'],
                                       offsets_Hz=annot_dict['seg_end_times_Hz'],
                                       file=annot_dict['audio_file'])
    print("a_sequence:\n", a_sequence)


.. parsed-literal::

    a_sequence:
     Sequence(segments=[Segment(label='1', onset_s=0.0029761904761904934, offset_s=0.14150432900432905, onset_Hz=143, offset_Hz=6792, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='1', onset_s=0.279125, offset_s=0.504625, onset_Hz=13398, offset_Hz=24222, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='5', onset_s=0.5556472915365209, offset_s=0.5962916666666667, onset_Hz=26671, offset_Hz=28622, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.6265416666666667, offset_s=0.6494583333333334, onset_Hz=30074, offset_Hz=31174, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.6842916666666666, offset_s=0.7044583333333333, onset_Hz=32846, offset_Hz=33814, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.7392916666666667, offset_s=0.7594583333333333, onset_Hz=35486, offset_Hz=36454, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.7942916666666666, offset_s=0.8300416666666667, onset_Hz=38126, offset_Hz=39842, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.8502083333333333, offset_s=0.884125, onset_Hz=40810, offset_Hz=42438, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.906125, offset_s=0.9409583333333333, onset_Hz=43494, offset_Hz=45166, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=0.9647916666666667, offset_s=1.013375, onset_Hz=46310, offset_Hz=48642, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=1.0234583333333334, offset_s=1.0665416666666667, onset_Hz=49126, offset_Hz=51194, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=1.0775416666666666, offset_s=1.1115676406926405, onset_Hz=51722, offset_Hz=53355, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=1.128875, offset_s=1.1765416666666666, onset_Hz=54186, offset_Hz=56474, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=1.1957916666666666, offset_s=1.2315416666666668, onset_Hz=57398, offset_Hz=59114, file='lbr3009_0005_2017_04_27_06_14_46.wav'), Segment(label='2', onset_s=1.2535416666666668, offset_s=1.2902083333333334, onset_Hz=60170, offset_Hz=61930, file='lbr3009_0005_2017_04_27_06_14_46.wav')])


2. Create a function that uses this code to take annotation files as an argument, and return Sequences
------------------------------------------------------------------------------------------------------

You already wrote this too! Just take your ``parse_batlab_mat`` function
from above and change a couple lines. First, you’re going to return a
list of sequences instead of your ``annot_list`` from before. You
probably want to make that explicit in your function.

.. code:: ipython3

    # %load -r 24-25 batlab2seq.py
        mat = loadmat(mat_file, squeeze_me=True)
        seq_list = []

Then at the end of your main loop, you’ll make a new ``Sequence`` from
each file using the factory function, append that to your ``seq_list``,
and then finally return that ``list`` of ``Sequence``\ s.

.. code:: ipython3

    # %load -r 56-63 batlab2seq.py
        seq = Sequence.from_keyword(file=filename,
                                    labels=seg_types,
                                    onsets_s=seg_start_times,
                                    offsets_s=seg_end_times,
                                    onsets_Hz=seg_start_times_Hz,
                                    offsets_Hz=seg_end_times_Hz)
        seq_list.append(seq)
        return seq_list

If this still feels too wordy and repetitive for you, you can put
``segFileStartTimes``, ``segFileEndTimes``, et al., into a Python
``dict`` with ``keys`` corresponding to the parameters for
``Segment.from_keyword``:

.. code:: python

   annot_dict = {
       'file': filename,
       'onsets_s': annotation['segFileStartTimes'].tolist(),
       'offsets_s': annotation['segFileEndTimes'].tolist()
       'labels': seg_types
   }

and then use another factory function, ``Sequence.from_dict``

.. code:: python

   seq_list.append(Sequence.from_dict(annot_dict))
