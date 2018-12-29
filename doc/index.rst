.. Crowsetta documentation master file, created by
   sphinx-quickstart on Sat Dec 22 21:16:45 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============
**Crowsetta**
=============

``crowsetta`` is a tool to work with any format for annotating birdsong (or other
vocalizations). **The goal of** ``crowsetta`` **is to make sure that your ability
to work with a dataset of birdsong does not depend on your ability to work with
any given format for annotating that dataset.**

**Features**
============

**Data types that help you write clean code**
---------------------------------------------

What ``crowsetta`` gives you is **not** yet another format for
annotation (I promise!). Instead you get some nice data types that make it easy to
work with any format: namely, ``Sequence``\ s made up of ``Segment``\ s.

.. code-block:: python

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


You can load annotation from your format of choice into ``Sequence``\ s of ``Segment``\ s
(most conveniently with the ``Transcriber``, as explained below) and then use the 
``Sequence``\ s however you need to in your program.

For example, if you want to loop through the ``Segment``\ s of each ``Sequence`` to
pull syllables out of a spectrogram, you can do something like this:

.. code-block:: python

   >>> syllables_from_sequences = []
   >>> for a_seq in seq:
   ...     seq_dict = seq.to_dict()  # convert Sequence to Python dictionary
   ...     # so we can get the name of the audio file associated with the Sequence
   ...     spect = some_spectrogram_making_function(seq['file'])
   ...     syllables = []
   ...     for seg in seq.segments:
   ...         syllable = spect[:, seg.onset:seg.offset]  ## spectrogram is a 2d numpy array
   ...         syllables.append(syllable)
   ...     syllables_from_sequences.append(syllables)

This code is succinct and looks like idiomatic Python.
For a deeper dive into why this is useful, see :ref:`background`.

**A**  ``Transcriber`` **that makes it convenient to work with any annotation format**
--------------------------------------------------------------------------------------

As mentioned, ``crowsetta`` provides you with a ``Transcriber`` that comes equipped
with convenience functions to do the work of converting for you. 

.. code-block:: python

    >>> annotation_files = [
    ...     '~/Data/bird1_day1/song1_2018-12-07_072135.not.mat',
    ...     '~/Data/bird1_day1/song2_2018-12-07_072316.not.mat',
    ...     '~/Data/bird1_day1/song3_2018-12-07_072749.not.mat'
    ... ]
    >>> from crowsetta import Transcriber
    >>> scribe = Transcriber()
    >>> seq = scribe.to_seq(file=notmat_files, format='notmat')
    >>> len(seq)
    3
    >>> print(seq[0])
    Sequence(segments=[Segment(label='a', onset_s=None, offset_s=None, onset_Hz=16000,
    offset_Hz=32000, file='~/Data/bird1_day1/song1_2018-12-07_072135.cbin'),
    Segment(label='b', onset_s=None, offset_s=None, ...

**Easily use the** ``Transcriber`` **with your own annotation format**
----------------------------------------------------------------------
You can even easily tell the ``Transcriber`` to use your own in-house format, like so:

.. code-block:: python

        >>> my_config = {
        ...     'myformat_name': {
        ...         'module': '/home/MyUserName/Documents/Python/convert_myformat.py'
        ...         'to_seq': 'myformat2seq',
        ...         'to_csv': 'myformat2csv'}
        ...     }
        ... }
        >>> scribe = crowsetta.Transcriber(user_config=my_config)
        >>> seq = scribe.toseq(file='my_annotation.mat', file_format='myformat_name')

For more about how that works, please see :ref:`howto-user-format`.

**Save and load annotations in plain text files**
-------------------------------------------------
If you need it to, ``crowsetta`` can save your ``Sequence``\ s of ``Segment``\ s
as a plain text file in the comma-separated values (csv) format. This file format
was chosen because it is widely considered to be a very robust way to share data.

.. code-block:: python

    from crowsetta import Transcriber
    scribe = Transcriber(user_config=your_config)
    scribe.to_csv(file_'your_annotation_file.mat',
                  csv_filename='your_annotation.csv')


An example csv looks like this:

.. literalinclude:: ../tests/test_data/csv/gy6or6_032312.csv
   :lines: 1-5
   :language: none

Now that you have that, you can load it into a pandas_ dataframe or an Excel
spreadsheet or a SQL database, or whatever you want.

.. _pandas: https://pandas.pydata.org/

You might find this useful in any situation where you want to share audio files of
song and some associated annotations, but you don't want to require the user to
install a large application in order to work with the annotation files.

**Getting Started**
-------------------
Install ``crowsetta`` by running:

.. code-block:: console

    $ pip install crowsetta
    

If you are new to the library, start with :ref:`tutorial`.

To see an example of using ``crowsetta`` to work with your own annotation format, 
see :ref:`howto-user-format`.

**Table of Contents**
=====================

.. toctree::
   :maxdepth: 2

   tutorial
   howto
   background

**Project Information**
=======================

``crowsetta`` was developed for use with the songdeck_ and
hybrid-vocal-classifier_ libraries.

.. _songdeck: https://github.com/NickleDave/songdeck

.. _hybrid-vocal-classifier: https://hybrid-vocal-classifier.readthedocs.io/en/latest/

Support
-------

If you are having issues, please let us know.

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues

Contribute
----------

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues
- Source Code: https://github.com/NickleDave/crowsetta

License
-------

The project is licensed under the 
`BSD license <https://github.com/NickleDave/crowsetta/blob/master/LICENSE>`_.

CHANGELOG
---------
You can see project history and work in progress in the 
`CHANGELOG <https://github.com/NickleDave/crowsetta/blob/master/doc/CHANGELOG.md>`_.

Citation
--------
If you use ``crowsetta``, please cite the DOI:

.. image:: https://zenodo.org/badge/159904494.svg
   :target: https://zenodo.org/badge/latestdoi/159904494
