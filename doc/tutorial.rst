.. _tutorial:

**Tutorial**
============

This tutorial present beginners with an introduction to ``crowsetta``.

The first thing we need to do to work with any Python library is import
it.

.. code:: ipython3

    import crowsetta

Getting some data to take ``crowsetta`` for a test drive
--------------------------------------------------------

Since ``crowsetta`` is a tool to working with annotations of
vocalizations, we need some audio files containing vocalizations that
are annotated. In this case, birdsong.

The ``formats`` function tells us what formats are built in to
Crowsetta.

.. code:: ipython3

    crowsetta.formats()

.. parsed-literal::

    'Annotation formats built in to Crowsetta: notmat, koumura'

You can download small example datasets of the built-in formats with the
``fetch`` function in the ``data`` module, like so:

.. code:: ipython3

    crowsetta.data.fetch(format='notmat')

.. parsed-literal::

    Downloading https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/13993349/cbinnotmat.tar.gz (8.6 MB)
    [........................................] 100.00000 - (  8.6 MB /   8.6 MB,    12 kB/s)   
    File saved as ./cbin-notmat.tar.gz.
    
    extracting ./cbin-notmat.tar.gz

Here we downloaded some ``.cbin`` audio files. Each ``.cbin`` file has
an associated ``.not.mat`` file that contains the annotation.

.. code:: ipython3

    !ls ./cbin-notmat/032312/*.cbin*

.. parsed-literal::

    ./cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin.not.mat
    ./cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin
    ./cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin.not.mat


(It doesn’t matter much for our purposes, but … files in the
``.not.mat`` annotation format are produced by a Matlab GUI,
evsonganaly, and are used to annotate audio files produced by a Labview
program for running behavioral experiments called EvTAF.)

Using the ``Transcriber`` to load annotation files into a data type we can work with in Python
----------------------------------------------------------------------------------------------

| Now we want to use ``crowsetta`` to load the annotations into some
  data type that makes it easy to get what we want out of audio files.
| First we need all the annotation files.

.. code:: ipython3

    from glob import glob  # function that finds files matching an expression
    notmats = glob('./cbin-notmat/032312/*.not.mat')
    notmats

.. parsed-literal::

    ['./cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin.not.mat',
     './cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat']

Now that we have our annotation files in a variable, we use the
``Transcriber`` to load them.

The ``Transcriber`` is a Python ``class``, and we want to create a new
``instance`` of that class. You don’t have to understand what that
means, but you do have to know that before you can do anything with a
``Transcriber``, you have to call the class, as if it were a function,
and assign it to some variable, like this:

.. code:: ipython3

    scribe = crowsetta.Transcriber()

Now our ``scribe`` object has ``methods`` (functions that “belong” to
it) that we can use on our annotation files.

The ``to_seq`` method converts each file to a ``Sequence``, one of the
data types that helps us work with the annotation.

.. code:: ipython3

    seq = scribe.to_seq(file=notmats, file_format='notmat')

For each annotation file, we should have a ``Sequence``.

.. code:: ipython3

    print("Number of annotation files: ", len(notmats))
    print("Number of Sequences: ", len(seq))
    if len(notmats) == len(seq):
        print("The number of annotation files is equal to number of sequences.")

.. parsed-literal::

    Number of annotation files:  10
    Number of Sequences:  10
    The number of annotation files is equal to number of sequences.

Each ``Sequence`` consists of some number of ``Segment``\ s, i.e., a
part of the sequence defined by an ``onset`` and ``offset`` that has a
``label`` associated with it.

.. code:: ipython3

    print("type of first element of seq: ", type(seq[0]))
    print("\nFirst two Segments of first Sequence:\n", seq[0].segments[0:2])

.. parsed-literal::

    type of first element of seq:  <class 'crowsetta.classes.Sequence'>
    
    First two Segments of first Sequence:
     [Segment(label='i', onset_s=0.435, offset_s=0.511, onset_Hz=13924, offset_Hz=16350, file='./cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin'), Segment(label='i', onset_s=0.583, offset_s=0.662, onset_Hz=18670, offset_Hz=21184, file='./cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin')]
