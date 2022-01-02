
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
annotation format. Here’s an outline of the steps we’ll go through:

1. get your annotations into some variables in Python (maybe you already
   wrote code to do this)
2. use one of the ``Sequence`` “factory functions” (we’ll explain what
   that means) to conveniently turn your annotations into
   ``Sequence``\ s
3. turn the code you just wrote into a function that takes annotation
   files as an argument, and returns ``Sequence``\ s
4. make a ``Transcriber`` that knows to use this function when you tell
   it you want to turn your annotation files into ``Sequence``\ s

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
code has some weird, hard-to-read lines to deal with the complicated
MATLAB ``struct``\ s created by ``BatLAB`` and how they load into
Python. The code also has several repetitive steps to deal with the
idiosyncracies of how ``SoNAR`` and ``BatLAB`` save data: unit
conversion, data types, etcetera. You can’t change ``BatLAB`` or
``SoNAR`` though, because that’s Alfred’s job, and everyone else’s code
that was written ten years ago (and still works!) expects those
idiosyncracies.

You know that it’s a good idea to turn the code you wrote into a
function (because you took part in a `Software
Carpentry <https://software-carpentry.org/>`__ workshop and then you
read `this
paper <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>`__.)
You figured out which bits of the code will be common to all your
projects and you make that into a function, called ``parse_batlab_mat``.
At first you just copy and paste it into all your projects. Then you
decide you also want to save everyone else in your lab the effort of
writing the same code, so you put the script on your lab’s Github page.
This is a step in the right direction, although ``parse_batlab_mat``
gives you back a Python ``list`` of ``dict``\ s, and you end up typing a
lot of things like:

.. code:: python

   labels = annot_list[0]['seg_type']
   onsets = annot_list[0]['seg_onsets']
   offsets = annot_list[0]['seg_offsets']

Typing all those very similar ``['keys']`` in particular gets kind of
annoying and makes you wonder if you should spend your vacation learning
how to use one of those hacker text editors like ``vim``.

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

1. get your annotation into some variables in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

2. use one of the ``Sequence`` “factory functions” to conveniently turn annotations in your format into ``Sequence``\ s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, to get the ``Sequence``, we’ll use a “factory function”, which
just means it’s a function built into the ``Sequence`` class that gives
us back an instance of a ``Sequence``. One such factory function is
``Sequence.from_keyword``. Here’s an example of using it:

.. code:: ipython3

    from parsebat import parse_batlab_mat
    from crowsetta.sequence import Sequence
    
    # you, using the function you already wrote
    annot_list = parse_batlab_mat(mat_file='bat1_annotation.mat')
    
    # you have annotation from one file in an "annot_dict"
    annot_dict = annot_list[0]
    
    a_sequence = Sequence.from_keyword(labels=annot_dict['seg_types'],
                                       onsets_s=annot_dict['seg_start_times'],
                                       offsets_s=annot_dict['seg_end_times'],
                                       onset_inds=annot_dict['seg_start_times_Hz'],
                                       offset_inds=annot_dict['seg_end_times_Hz'],
                                       file=annot_dict['audio_file'])
    print("a_sequence:\n", a_sequence)


.. parsed-literal::

    a_sequence:
     <Sequence with 15 segments>


3. turn the code we just wrote into a function that takes annotation files as an argument, and returns ``Sequence``\ s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again, you pretty much already wrote this. Just take your
``parse_batlab_mat`` function from above and change a couple lines.
First, you’re going to return a list of sequences instead of your
``annot_list`` from before. You probably want to make that explicit in
your function.

.. code:: ipython3

    # %load -r 4-7,24-25 batlab2seq.py
    from crowsetta.sequence import Sequence
    
    
    def batlab2seq(mat_file):
        mat = loadmat(mat_file, squeeze_me=True)
        seq_list = []

Then at the end of your main loop, instead of making your
``annot_dict``, you’ll make a new ``Sequence`` from each file using the
``from_keyword`` factory function, append the new ``Sequence`` to your
``seq_list``, and then finally return that ``list`` of ``Sequence``\ s.

.. code:: ipython3

    # %load -r 56-63 batlab2seq.py
    seq = Sequence.from_keyword(file=filename,
                                labels=seg_types,
                                onsets_s=seg_start_times,
                                offsets_s=seg_end_times,
                                onset_inds=seg_start_times_Hz,
                                offset_inds=seg_end_times_Hz)
    seq_list.append(seq)
        return seq_list

   If this still feels too wordy and repetitive for you, you can put
   ``segFileStartTimes``, ``segFileEndTimes``, et al., into a Python
   ``dict`` with ``keys`` corresponding to the parameters for
   ``Segment.from_keyword``:

..

   .. code:: python

      annot_dict = {
          'file': filename,
          'onsets_s': annotation['segFileStartTimes'].tolist(),
          'offsets_s': annotation['segFileEndTimes'].tolist()
          'labels': seg_types
      }

      Note here that you only have to specify the onsets an offsets of
      segments *either* in seconds or in Hertz (but you can define
      both).

..

   and then use another factory function, ``Sequence.from_dict``, to
   create the ``Sequence``.

   .. code:: python

      seq_list.append(Sequence.from_dict(annot_dict))

Now that you have a function that takes annotation files and return
``Sequence``\ s, call it something like ``batlab2seq`` and put it in a
file that ends with ``.py``, e.g. \ ``batlab2seq.py``. This is also
known as a Python **module** (as you’ll need to know below). To see the
entire example, check out the `batlab2seq.py <./batlab2seq.py>`__ file
in this folder (and compare it with `parsebat.py <./parsebat.py>`__).

4. make a ``Transcriber`` that knows to use this function when you tell it you want to turn your annotation files into ``Sequence``\ s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have worked with ``Crowsetta`` already, or gone through the
tutorial, you know that we can work with a ``Transcriber`` that does the
work of making ``Sequence``\ s of ``Segment``\ s from annotation files
for us. We create a new instance of a ``Transcriber`` by writing
something like this:

.. code:: python

   scribe = Transcriber()

You will do the same thing here, but to tell the ``Transcriber`` how to
work with your format, you will pass an argument for the ``user_config``
parameter when you create a new one:

.. code:: python

   scribe = Transcriber(user_config=your_config)

The argument you pass for ``user_config`` will be a Python dictionary
with the following structure:

.. code:: python

   your_config = {
       'batlab': {
           'module': 'batlab2seq.py',
           'to_seq': 'batlab2seq',
           'to_csv': 'None',
           'to_format': 'None',
       }
   }

Notice that this a dictionary of dictionaries, where each ``key`` in the
top-level ``dict`` is the name of a user-defined format, here
``batlab``. If you had multiple formats to use, you would add more
``dict``\ s inside the top-level ``dict``.

The ``value`` for each ``key`` is another Python dictionary that tells
the ``Transcriber`` what functions to use from your module when you call
one of its methods and specify this format. In the example above, you’re
telling the ``Transcriber`` that when you say ``file_format='batlab'``,
it should use functions from the ``batlab2seq.py`` module. More
specifically, when you call
``scribe.to_seq(file='annotation.mat', file_format='batlab')``, it
should use the ``batlab2seq`` function to convert your annotation into
``Sequence``\ s. Notice also that you can specify ``'None'`` for
``to_csv`` and ``to_format`` (which would be a function that converts
``Sequence``\ s back to the ``BatLAB`` format).

Here’s what it looks like to do all of that in a few lines of code:

.. code:: ipython3

    from crowsetta import Transcriber
    
    your_config = {
        'batlab': {
            'module': 'batlab2seq.py',
            'to_seq': 'batlab2seq',
        }
    }
    
    scribe = Transcriber(user_config=your_config)
    
    seq_list = scribe.to_seq(file='bat1_annotation.mat', file_format='batlab')

And now, just like you do with the built-in formats, you get back a list
of ``Sequence``\ s from your format:

.. code:: ipython3

    print(f'First item in seq_list: {seq_list[0]}')
    print(f'First segment in first sequence:\n{seq_list[0].segments[0]}')


.. parsed-literal::

    First item in seq_list: <Sequence with 15 segments>
    First segment in first sequence:
    Segment(label='1', file='lbr3009_0005_2017_04_27_06_14_46.wav', onset_s=0.0029761904761904934, offset_s=0.14150432900432905, onset_ind=143, offset_ind=6792)


Notice that we also get a ``to_csv`` function for free:

.. code:: ipython3

    scribe.to_csv(file='bat1_annotation.mat', 
                  csv_filename='test.csv',
                  file_format='batlab')
    
    import csv
    with open('test.csv', 'r', newline='') as csv_file:
         reader = csv.reader(csv_file)
         for _ in range(4):
             print(next(reader))


.. parsed-literal::

    ['label', 'onset_s', 'offset_s', 'onset_ind', 'offset_ind', 'file']
    ['1', '0.0029761904761904934', '0.14150432900432905', '143', '6792', 'lbr3009_0005_2017_04_27_06_14_46.wav']
    ['1', '0.279125', '0.504625', '13398', '24222', 'lbr3009_0005_2017_04_27_06_14_46.wav']
    ['5', '0.5556472915365209', '0.5962916666666667', '26671', '28622', 'lbr3009_0005_2017_04_27_06_14_46.wav']


How does that work? Well, as long as we can convert our annotation
format to ``Sequence``\ s, then we can pass those ``Sequence``\ s to the
``crowsetta.csv2seq`` function, which will output them as a ``.csv``
file. The ``Transcriber`` does this by default. Under the hood, when you
make a new ``Transcriber`` with your ``user_config``, it wraps your
``format2seq`` function and the ``seq2csv`` function into one, using the
function ``crowsetta.csv.toseq_func_to_csv``.

Summary
-------

Now you have seen in detail the process of working with your own
annotation format in ``Crowsetta``. Here’s a review of the steps, with
some code snippets worked in to tie it all together:

1. get your annotations into some variables in Python, perhaps using
   code you already wrote
2. use one of the ``Sequence`` “factory functions” to conveniently turn
   your annotations into ``Sequence``\ s
3. turn all that code into a function that takes annotation files as an
   argument, and returns ``Sequence``\ s

..

   steps 1-3 will give you something like this in a file named something
   like ``myformat.py``

   .. code:: python

      from Crowsetta import Sequence


      def myformat2seq(my_format_files):
          seq_list = []
          for format_file in my_format_files:
          # load annotation into some Python variables, e.g. a dictionary
              annot_dict = magic_annotation_unpacking_function(format_file)
              seq = Sequence.from_dict(annot_dict)
              seq_list.append(seq)
          return seq_list

4. make a ``Transcriber`` that knows to use this function when you tell
   it you want to turn your annotation files into ``Sequence``\ s,
   and/or csv files, or to convert back to your format from
   ``Sequence``\ s (assuming you wrote a function in your module that
   will do so).

..

   .. code:: python

      from Crowsetta import Transcriber

      my_config = {
          'my_format': {
              'module': 'myformat.py',
              'to_seq': 'myformat2seq',
              'to_csv': 'myformat2csv',
              'to_format': 'seq2myformat,
          }
      }
      scribe = Transcriber(user_config=my_config)
      seq_list = scribe.to_seq(file='my_annotations.txt', file_format='my_format')
