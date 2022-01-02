
.. _tutorial:

**Tutorial**
============

This tutorial present beginners with an introduction to ``crowsetta``.
You can get the Jupyter notebook for this tutorial by going to
https://github.com/NickleDave/crowsetta and clicking on the big green
“Clone or Download” button on the right side of the screen. You can then
find this notebook and others in the ``crowsetta/notebooks/`` directory.

**Finding out what annotation formats are built in to** ``crowsetta`` **and getting some example data to work with**
--------------------------------------------------------------------------------------------------------------------

Since ``crowsetta`` is a tool to working with annotations of
vocalizations, we need some audio files containing vocalizations that
are annotated. In this case, birdsong.

The first thing we need to do to work with any Python library is import
it.

.. code:: ipython3

    import crowsetta

Now we can use the ``formats`` function to find out what formats are
built in to Crowsetta.

.. code:: ipython3

    crowsetta.formats()




.. parsed-literal::

    'Annotation formats built in to Crowsetta: notmat, koumura'



You can download small example datasets of the built-in formats with the
``fetch`` function in the ``data`` module, like so:

.. code:: ipython3

    crowsetta.data.fetch(format='notmat', destination_path='./data/')


.. parsed-literal::

    Downloading https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/13993349/cbinnotmat.tar.gz (8.6 MB)
    [........................................] 100.00000 - (  8.6 MB /   8.6 MB,   3.8 MB/s)   
    File saved as ./data/cbin-notmat.tar.gz.
    
    extracting ./data/cbin-notmat.tar.gz


Here we downloaded some ``.cbin`` audio files. Each ``.cbin`` file has
an associated ``.not.mat`` file that contains the annotation.

We use the ``glob`` function from the Python standard library to list
those files. (``glob`` gives you the full path to files that match a
string pattern; ``*`` in the string below is a wildcard that will match
zero or more characters).

.. code:: ipython3

    from glob import glob
    glob('./data/cbin-notmat/032312/*.cbin*')




.. parsed-literal::

    ['./data/cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin.not.mat',
     './data/cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat']



(It doesn’t matter much for our purposes, but … files in the
``.not.mat`` annotation format are produced by a Matlab GUI,
evsonganaly, and are used to annotate audio files produced by a Labview
program for running behavioral experiments called EvTAF.)

**Using the** ``Transcriber`` **to load annotation files into a data type we can work with in Python**
------------------------------------------------------------------------------------------------------

Now we want to use ``crowsetta`` to load the annotations into some
**data type** that makes it easy to get what we want out of audio files.
Python has several data types like a ``list`` or ``dict`` that make it
easy to work with data; the data types that ``crowsetta`` gives us,
``Sequence``\ s and ``Segment``\ s, specifically make it easy to write
clean code for working with annotation formats for birdsong and other
vocalizations.

First we need to get all the annotation files in some variable. We use
``glob`` again to do so, this time just getting the ``.not.mat`` files.

.. code:: ipython3

    notmats = glob('./data/cbin-notmat/032312/*.not.mat')
    for notmat in notmats: print(notmat)


.. parsed-literal::

    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0810.148.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0817.183.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0816.179.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0813.163.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0820.196.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0809.141.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0821.202.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0811.159.cbin.not.mat
    ./data/cbin-notmat/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat


Now that we have our annotation files in a variable, we use the
``Transcriber`` to load them.

The ``Transcriber`` is a Python ``class``, and we want to create a new
``instance`` of that class. You don’t have to understand what that
means, but you do have to know that before you can do anything with a
``Transcriber``, you have to call the class, as if it were a function,
and assign it to some variable, like this:

.. code:: ipython3

    scribe = crowsetta.Transcriber()
    print("scribe is an instance of a", type(scribe))


.. parsed-literal::

    scribe is an instance of a <class 'crowsetta.transcriber.Transcriber'>


Now we have a ``scribe`` with ``methods`` that we can use on our
annotation files (methods are functions that “belong” to a class).

**Using the** ``to_seq`` **method to load annotation format files into** ``Sequence``\ **s**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``to_seq`` method loads each file into a ``Sequence``, one of the
data types that helps us work with the annotation. We call the method,
passing our list of files as an argument for ``file`` and telling the
``scribe`` our ``file_format``.

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

    print("first element of seq: ", seq[0])
    print("\nFirst two Segments of first Sequence:")
    for seg in seq[0].segments[0:2]: print(seg)


.. parsed-literal::

    first element of seq:  <Sequence with 54 segments>
    
    First two Segments of first Sequence:
    Segment(label='i', file='./data/cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin', onset_s=0.435, offset_s=0.511, onset_ind=13924, offset_ind=16350)
    Segment(label='i', file='./data/cbin-notmat/032312/gy6or6_baseline_230312_0819.190.cbin', onset_s=0.583, offset_s=0.662, onset_ind=18670, offset_ind=21184)


**Using** ``crowsetta`` **data types to write clean code**
----------------------------------------------------------

Now that we have a ``list`` of ``Sequence``\ s, we can ``iterate``
(loop) through it to get at our audio data in a clean, Pythonic way.

Let’s say we’re interested in the mean amplitude of each type of
syllable in an individual bird’s song. How do we get that data into
something in Python we can analyze? One approach would be to create a
Python ``dict`` that maps the name of each syllable type to a list of
the mean amplitudes of every occurrence of that syllable in our dataset.

Something like this:

.. code:: python

   syl_amp_dict = {
       'a': [0.01, 0.023, ..., 0.017],
       'b': [0.03, 0.032, ..., 0.291],
       ...,
       'j': [0.07, 0.068, ..., 0.71],
   }

So to do that, we need to first figure out the unique types of syllables
that will be the ``keys`` of our dictionary, ``a``, ``b``, …, ``n``.

We’ll ``iterate`` over all the ``Sequence``\ s, and then in an inner
loop, we’ll ``iterate`` through all the ``Segment``\ s in that
``Sequence``, using the ``label`` property of the segment to figure out
which syllable type we’re looking at from this bird.

.. code:: ipython3

    import numpy as np
    
    all_labels = []
    for sequence in seq:
        for segment in sequence.segments:
            all_labels.append(segment.label)
    
    unique_labels = np.unique(all_labels)
    
    # now we make our dict,.
    # with some fancy Pythoning
    syl_amp_dict = dict(
        zip(unique_labels,
           [[] for _ in range(len(unique_labels))])
    )
    
    print("syl_amp_dict", syl_amp_dict)


.. parsed-literal::

    syl_amp_dict {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': []}


(There are more concise ways to do that, but doing it the way we did let
us clearly see iterating through the ``Segment``\ s and
``Sequence``\ s.)

Now we want to get the amplitude for each syllable. We’ll take the
amplitude from the audio waveform (instead of, say, making a spectrogram
out of it and then getting an amplitude measure by summing power of
every time bin in the spectrogram).

Since the audio signal might be a bit noisy, we’ll use a function,
``smooth_data`` (from the
```evfuncs`` <https://github.com/soberlab/evfuncs>`__ library) that
takes the raw audio from a file, applies a bandpass filter, rectifies
the signal, and then smooths it with a sliding window.

.. code:: ipython3

    import evfuncs
    help(evfuncs.smooth_data)


.. parsed-literal::

    Help on function smooth_data in module evfuncs.evfuncs:
    
    smooth_data(rawsong, samp_freq, freq_cutoffs=(500, 10000), smooth_win=2)
        filter raw audio and smooth signal
        used to calculate amplitude.
        
        Parameters
        ----------
        rawsong : ndarray
            1-d numpy array, "raw" voltage waveform from microphone
        samp_freq : int
            sampling frequency
        freq_cutoffs: list
            two-element list of integers, [low freq., high freq.]
            bandpass filter applied with this list defining pass band.
            If None, in which case bandpass filter is not applied.
        smooth_win : integer
            size of smoothing window in milliseconds. Default is 2.
        
        Returns
        -------
        smooth : ndarray
            1-d numpy array, smoothed waveform
        
        Applies a bandpass filter with the frequency cutoffs in spect_params,
        then rectifies the signal by squaring, and lastly smooths by taking
        the average within a window of size sm_win.
        This is a very literal translation from the Matlab function SmoothData.m
        by Evren Tumer. Uses the Thomas-Santana algorithm.
    


.. code:: ipython3

    for sequence in seq:
        cbin = sequence.file
        raw_audio, samp_freq = evfuncs.load_cbin(cbin)
        smoothed = evfuncs.smooth_data(raw_audio, samp_freq,
                                       freq_cutoffs=(500, 10000))
        for segment in sequence.segments:
            smoothed_seg = smoothed[segment.onset_ind:segment.offset_ind]
            mean_seg_amp = np.mean(smoothed_seg)
            syl_amp_dict[segment.label].append(mean_seg_amp)
    
    mean_syl_amp_dict = {}
    for syl_label, mean_syl_amps_list in syl_amp_dict.items():
        # get mean of means
        mean_syl_amp_dict[syl_label] = np.mean(mean_syl_amps_list)

.. code:: ipython3

    for syl_label, mean_syl_amp in mean_syl_amp_dict.items():
        print(f'mean of mean amplitude for syllable {syl_label}:',
              mean_syl_amp)


.. parsed-literal::

    mean of mean amplitude for syllable a: 208207.1240286356
    mean of mean amplitude for syllable b: 16679.46415410411
    mean of mean amplitude for syllable c: 1327150.5563241516
    mean of mean amplitude for syllable d: 510289.3285039273
    mean of mean amplitude for syllable e: 846590.5009779687
    mean of mean amplitude for syllable f: 522099.1725575389
    mean of mean amplitude for syllable g: 192993.6353244887
    mean of mean amplitude for syllable h: 167343.74232649207
    mean of mean amplitude for syllable i: 16903.56906972767
    mean of mean amplitude for syllable j: 3005979.1576137305
    mean of mean amplitude for syllable k: 170753.7788673711


Okay, now you’ve seen the basics of working with ``crowsetta``. Get out
there and analyze some vocalizations!
