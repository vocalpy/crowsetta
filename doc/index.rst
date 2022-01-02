.. Crowsetta documentation master file, created by
   sphinx-quickstart on Sat Dec 22 21:16:45 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============
**Crowsetta**
=============

``crowsetta`` is a tool to work with any format for annotating vocalizations, like
birdsong or human speech. **The goal of** ``crowsetta`` **is to make sure that your
ability to work with a dataset of vocalizations does not depend on your ability to work with
any given format for annotating that dataset.**

**Features**
============

**Data types that help you write clean code**
---------------------------------------------

What ``crowsetta`` gives you is **not** yet another format for
annotation (I promise!). Instead you get some nice data types that make it easier to
work with any format: namely, ``Sequence``\ s made up of ``Segment``\ s.
The code block below shows some of the features of these data types.

.. code-block:: python

    >>> from crowsetta import Segment, Sequence
    >>> a_segment = Segment.from_keyword(
    ...     label='a',
    ...     onset_ind=16000,
    ...     offset_ind=32000,
    ...     file='bird21.wav'
    ...     )
    >>> another_segment = Segment.from_keyword(
    ...     label='b',
    ...     onset_ind=36000,
    ...     offset_ind=48000,
    ...     file='bird21.wav'
    ...     )
    >>> list_of_segments = [a_segment, another_segment]
    >>> seq = Sequence.from_segments(segments=list_of_segments)
    >>> print(seq)
    <Sequence with 2 segments>
    >>> for segment in seq.segments: print(segment)
    Segment(label='a', file='bird21.wav', onset_s=None, offset_s=None, onset_ind=16000, offset_ind=32000)
    Segment(label='b', file='bird21.wav', onset_s=None, offset_s=None, onset_ind=36000, offset_ind=48000)
    >>> seq.file
    bird21.wav
    >>> seq.onset_inds
    array([16000, 36000])

You load annotation from your format of choice into ``Sequence``\ s of ``Segment``\ s
(most conveniently with the ``Transcriber``, as explained below) and then use the 
``Sequence``\ s however you need to in your program.

For example, if you want to loop through the ``Segment``\ s of each ``Sequence`` to
pull syllables out of a spectrogram, you can do something like this:

.. code-block:: python

   >>> list_of_sequences = my_sequence_loading_function(file='annotation.txt')
   >>> syllables_from_sequences = []
   >>> for a_sequence in list_of_sequences:
   ...     # get name of the audio file associated with the Sequence
   ...     audio_file = a_sequence.file
   ...     # then create a spectrogram from that audio file
   ...     spect = some_spectrogram_making_function(audio_file)
   ...     syllables = []
   ...     for segment in a_sequence.segments:
   ...         ## spectrogram is a 2d numpy array so we index into using onset and offset from segment
   ...         syllable = spect[:, segment.onset_s:segment.offset_s]
   ...         syllables.append(syllable)
   ...     syllables_from_sequences.append(syllables)

This code is succinct, compared to the data munging code you usually write when dealing with
audio files and annotation formats. It reads like idiomatic Python.
For a deeper dive into why this is useful, see :ref:`background`.

**A**  ``Transcriber`` **that makes it convenient to work with any annotation format**
--------------------------------------------------------------------------------------

As mentioned, ``crowsetta`` provides you with a ``Transcriber`` that comes equipped
with convenience functions to do the work of loading and saving annotations for you.

.. code-block:: python

    >>> annotation_files = [
    ...     '~/Data/bird1_day1/song1_2018-12-07_072135.not.mat',
    ...     '~/Data/bird1_day1/song2_2018-12-07_072316.not.mat',
    ...     '~/Data/bird1_day1/song3_2018-12-07_072749.not.mat'
    ... ]
    >>> from crowsetta import Transcriber
    >>> scribe = Transcriber()
    >>> seq = scribe.to_seq(file=annotation_files, format='notmat')
    >>> len(seq)
    3
    >>> print(seq[0])
    <Sequence with 55 segments>

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
spreadsheet or an SQL database, or whatever you want.

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
