
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

1. load your annotation into a ``Sequence``
2. return this ``Sequence`` from a function
3. make a ``Transcriber`` that knows to use your function when you tell
   it you want to turn your annotation files into ``Sequence``\ s
4. use the ``to_seq`` method of the ``Transcriber`` to get
   ``Sequence``\ s that you can use in your Python code for your
   analysis
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
projects (the bits above) and you make that into a function. At first
you just copy and paste it into all your projects. Then you decide you
also want to save everyone else in your lab the effort of writing the
same code, so you put the script on your lab’s Github page. This is a
step in the right direction, although your function gives you back a
``list`` of ``dict``\ s. You have to type a lot of things like
``annot_list[0].annot_dict['seg_onsets']`` which gets kind of annoying
and makes you wonder if you should spend Christmas break learning how to
use one of those hacker text editors like ``vim``.

But now you’re publishing a paper in *PLOS Comp. Bio.* called “Pidgeon
Bat: Emergence of Dialects in Colonies of Multiple Bat Species”. You
want to share your data with the world, mainly to mollify reviewer #3
(who you are pretty sure from the way they write is Oswald Cobblepot,
professor emeritus of ethology at Metropolitan University of Fruitville,
Florida, and author of the seminal review from 1982, “Bat Calls: A
Completely Innate Behavior Encoded Genetically”). The problem is that
reviewer #3 only knows how to write Fortran code and definitely doesn’t
have the patience to read through ``parse_batlab_mat`` to figure out if
they are convinced that your group can consistently record and identify
bat calls.

What you really want is to share your data and write your code in a way
that doesn’t depend on anyone knowing anything about ``BatLAB``
or\ ``SoNAR`` and how they save data and annotations. This is where
``crowsetta`` comes to your rescue.

Okay, now that we’ve set up some background for our case study, let’s go
through the steps we outlined above.

1. Load your format into a ``Sequence``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| The ``BatLAB`` GUI saves annotation into ``annotation.mat`` files with
  two variables:
| - ``filenames``: a vector where each element is the name of an audio
  file - ``annotations``: a ``struct`` that has a record for each
  element in ``filenames``, and that record is the annotation
  corresponding to the audio file with the same index in ``filenames``

.. code:: ipython3

    from scipy.io import loadmat
    bat1_annotation = loadmat('../src/bin/bird1_annotation.mat')
    print('variables in .mat file:',
          [var for var in list(bat1_annotation.keys())
           if not var.startswith('__')]
         )


.. parsed-literal::

    variables in .mat file: ['filenames', 'annotations']


Here’s the code you wrote to unpack the ``.mat`` files:

.. code:: ipython3

    # %load -r 7-8,14-45 ../src/bin/parsebat.py
    mat = loadmat(mat_file, squeeze_me=True)
    annot_list = []
    for filename, annotation in zip(mat['filenames'], mat['annotations']):
        # below, .tolist() does not actually create a list,
        # instead gets ndarray out of a zero-length ndarray of dtype=object.
        # This is just weirdness that results from loading complicated data
        # structure in .mat file.
        seg_onsets = annotation['segOnset'].tolist()
        seg_offsets = annotation['segOffset'].tolist()
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
                             "not recognized.".format(wav_filename,
                                                      type(labels)))
        BATLAB_SAMP_FREQ = 33100
        seg_onsets_Hz = np.round(seg_onsets * BATLAB_SAMP_FREQ).astype(int)
        seg_offsets_Hz = np.round(seg_offsets * BATLAB_SAMP_FREQ).astype(int)
        annot_dict = {
            'seg_types': seg_types,
            'seg_onsets': seg_onsets,
            'seg_offsets': seg_offsets,
            'seg_onsets_Hz': seg_onsets_Hz,
            'seg_offsets_Hz': seg_offsets_Hz,
        }
        annot_list.append(annot_dict)

Like we said above, the code has some weird, hard-to-read lines to deal
with the way that the complicated MATLAB ``struct``\ s created by
``BatLAB`` load into Python, such as calling ``tolist()`` and making
sure the labels get loaded correctly into a numpy array. And the code
has several repetitive steps to deal with the idiosyncracies of
``SoNAR`` and ``BatLAB``, like converting the start and stop times of
the calls from seconds back to Hertz so you can find those times in the
raw audio files.

When it runs on a file, you get back an ``annot_list`` where each item
is an ``annot_dict`` that contains the annotations for a file, like
this:

.. code:: python

   annot_dict = {
       'seg_types': ,
       'seq_onsets':
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

All you need to do is take this code you already wrote, and instead of
returning all of those variables, you can turn them into a ``Sequence``.

Let’s make a ``Sequence`` using the ``from_keyword`` function.

.. code:: ipython3

    cd ../src/bin


.. parsed-literal::

    /home/ildefonso/Documents/repositories/coding/birdsong/crowsetta/src/bin


.. code:: ipython3

    from parsebat import parse_batlab_mat
    
    annot_list = parse_batlab_mat(mat_file='bird1_annotation.mat')


.. parsed-literal::

    > /home/ildefonso/Documents/repositories/coding/birdsong/crowsetta/src/bin/parsebat.py(20)parse_batlab_mat()
    -> seg_onsets = annotation['segOnset'].tolist()


.. parsed-literal::

    (Pdb)  annotation


.. parsed-literal::

    (array([0.00297619, 0.279125  , 0.55564729, 0.62654167, 0.68429167,
           0.73929167, 0.79429167, 0.85020833, 0.906125  , 0.96479167,
           1.02345833, 1.07754167, 1.128875  , 1.19579167, 1.25354167]), array([0.14150433, 0.504625  , 0.59629167, 0.64945833, 0.70445833,
           0.75945833, 0.83004167, 0.884125  , 0.94095833, 1.013375  ,
           1.06654167, 1.11156764, 1.17654167, 1.23154167, 1.29020833]), array([1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], dtype=uint8))


.. parsed-literal::

    (Pdb)  q


::


    ---------------------------------------------------------------------------

    BdbQuit                                   Traceback (most recent call last)

    <ipython-input-3-017ab488e7f0> in <module>
          1 from parsebat import parse_batlab_mat
          2 
    ----> 3 annot_list = parse_batlab_mat(mat_file='bird1_annotation.mat')
    

    ~/Documents/repositories/coding/birdsong/crowsetta/src/bin/parsebat.py in parse_batlab_mat(mat_file)
         18         # structure in .mat file.
         19         import pdb;pdb.set_trace()
    ---> 20         seg_onsets = annotation['segOnset'].tolist()
         21         seg_offsets = annotation['segOffset'].tolist()
         22         seg_types = annotation['segType'].tolist()


    ~/Documents/repositories/coding/birdsong/crowsetta/src/bin/parsebat.py in parse_batlab_mat(mat_file)
         18         # structure in .mat file.
         19         import pdb;pdb.set_trace()
    ---> 20         seg_onsets = annotation['segOnset'].tolist()
         21         seg_offsets = annotation['segOffset'].tolist()
         22         seg_types = annotation['segType'].tolist()


    ~/anaconda3/envs/conbirt-env/lib/python3.6/bdb.py in trace_dispatch(self, frame, event, arg)
         49             return # None
         50         if event == 'line':
    ---> 51             return self.dispatch_line(frame)
         52         if event == 'call':
         53             return self.dispatch_call(frame, arg)


    ~/anaconda3/envs/conbirt-env/lib/python3.6/bdb.py in dispatch_line(self, frame)
         68         if self.stop_here(frame) or self.break_here(frame):
         69             self.user_line(frame)
    ---> 70             if self.quitting: raise BdbQuit
         71         return self.trace_dispatch
         72 


    BdbQuit: 

