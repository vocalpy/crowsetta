.. _background:

==============
**Background**
==============

**Why is** ``crowsetta`` **needed**?
====================================

The target audience of ``crowsetta`` is anyone that works with birdsong
or any other vocalization that is annotated in some way, meaning someone took the time to
figure out where elements of the vocalizations start and stop, and has assigned labels to those
elements. Maybe you are a neuroscientist trying to figure out how songbirds learn their song,
or why mice emit ultrasonic calls. Or maybe you're an ecologist studying dialects of finches
distributed across Asia, or maybe you are a linguist studying accents in the
Antilles, or a speech pathologist looking for phonetic changes that indicate early onset
Alzheimer's disease, etc., etc., ...

To run a computational analysis on this kind of data, you'll need to get the annotation
out of a file, which often means you'll end up writing something like this:

.. code-block:: python

    from scipy.io import loadmat  # function from scipy library for loading Matlab data files
    annot = loadmat('bird1_experiment1_annotation_2018-11-17_083521.mat', squeeze_me=True)
    onsets = annot['onsets']  # unpack from dictionary
    onsets = np.asarray(onsets)  # convert to an array
    onsets = onsets / 1000  # convert from milliseconds to seconds

This is verbose and not easy to read. You could do some of it in one line ...

.. code-block:: python

    onsets = np.asarray(annot['onsets']) / 1000

... but now the next time you read that one-liner, you will have to mentally unpack it.

Such code quickly turns into `boilerplate <https://en.wikipedia.org/wiki/Boilerplate_code>`_
that you will write any time you need to work with this data. It becomes repetitive and
presents many opportunities for easy-to-miss bugs (e.g. a line with a variable named ``offset``
where you meant to type ``onset`` of some syllable or phoneme or whatever, because you cut and
pasted the line above it, and forgot to change ``off`` to ``on``\ ).

And things can become even more complicated if you have to deal with annotation stored
in other formats, such as a database. Here's an example of one way

.. code-block:: python

    import pymyseql

What would be nice is to have data types that represent annotation in a concise way, and
that we can manipulate like we would some native Python data type like a list or a
dictionary. ``crowsetta`` provides such data types: ``Sequence``\ s and ``Segment``\ s.

**How** ``crowsetta`` **works**
===============================

Internally, ``crowsetta`` takes whatever format you give it for a pile of files,
and turns that into a bunch of ``Sequence``\ s made up of ``Segment``\ s. For someone working
with birdsong, the ``Sequence``\ s will be single audio files / song bouts, and the
``Segment``\ s will be syllables in those song bouts (99.9% of the time). Then, if
you need it to, ``crowsetta`` can spit out your ``Sequence``\ s of ``Segment``\ s in
a simple text file with a comma-separated value (csv) format. This file format
was chosen because it is widely considered to be the most robust way to share data.

An example csv looks like this:

.. literalinclude:: ../tests/test_data/csv/gy6or6_032312.csv
   :lines: 1-5
   :language: none

Now that you have that, you can load it into a `pandas` dataframe or an Excel 
spreadsheet or a SQL database, or whatever you want.
