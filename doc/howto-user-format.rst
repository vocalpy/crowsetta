
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

Case Study: the ``BatLAB`` format:
----------------------------------

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
same code, so you put the script on your lab’s Github page. Cool, cool.

But now you’re publishing a PLOS Comp Biology paper, *Pidgeon Bat:
Emergence of Dialects in Colonies of Multiple Bat Species*. You want to
share your data with the world, mainly to satisfy reviewer #3 (who you
are pretty sure from the way they write is Oswald Cobblepot, professor
emeritus of ethology and author of the seminal review from 1982, *Bat
Calls: A Completely Innate Behavior Encoded Genetically*). The problem
is that reviewer #3 only knows how to write Fortran code and definitely
doesn’t have the patience to read through ``parse_batlab_mat`` to figure
out if they are convinced that your group can consistently record and
identify bat calls.

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
          [var for var in list(bat1.keys()) if not var.startswith('__')]
         )


.. parsed-literal::

    variables in .mat file: ['filenames', 'annotations']


Here’s the code you wrote to unpack the ``.mat`` files:

.. code:: ipython3

    # %load -r 13-14,20-43 ../src/bin/batlab2seq.py
    mat = loadmat(file, squeeze_me=True)
    seq_list = []
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

Like we said above, the code has some weird, hard-to-read lines to deal
with the way that the complicated MATLAB ``struct``\ s created by
``BatLAB`` load into Python, such as calling ``tolist()`` and making
sure the labels get loaded correctly into a numpy array. And the code
has several repetitive steps to deal with the idiosyncracies of
``SoNAR`` and ``BatLAB``, like converting the start and stop times of
the calls from seconds back to Hertz so you can find those times in the
raw audio files.

Again, as we said above, you turned your code into a function to make it
easier to use across projects:

.. code:: python

   def parse_batlab_mat(mat_file):
       # code above here
       return seg_types, seg_onsets, seg_offsets, seg_onsets_Hz, seg_offsets_Hz

This is where ``crowsetta`` comes to your rescue. All you need to do is
take this code you already wrote, and instead of returning all of those
variables, you can turn them into a ``Sequence``.

Let’s make a ``Sequence`` using the ``from_keyword`` function.

.. code:: ipython3

    %load ../src/bin/parsebat.py  # contains parse_batlab_mat function
    file0 = bat1['filenames'][0]
    annot0 = bat1['annotations'][0]


::


    ---------------------------------------------------------------------------

    SyntaxError                               Traceback (most recent call last)

    ~/anaconda3/envs/conbirt-env/lib/python3.6/site-packages/IPython/core/interactiveshell.py in find_user_code(self, target, raw, py_only, skip_encoding_cookie, search_ns)
       3586         try:                                              # User namespace
    -> 3587             codeobj = eval(target, self.user_ns)
       3588         except Exception:


    SyntaxError: invalid syntax (<string>, line 1)

    
    During handling of the above exception, another exception occurred:


    ValueError                                Traceback (most recent call last)

    <ipython-input-25-02ad1ffafe42> in <module>
    ----> 1 get_ipython().run_line_magic('load', '../src/bin/parsebat.py  # contains parse_batlab_mat function')
    

    ~/anaconda3/envs/conbirt-env/lib/python3.6/site-packages/IPython/core/interactiveshell.py in run_line_magic(self, magic_name, line, _stack_depth)
       2285                 kwargs['local_ns'] = sys._getframe(stack_depth).f_locals
       2286             with self.builtin_trap:
    -> 2287                 result = fn(*args,**kwargs)
       2288             return result
       2289 


    <decorator-gen-47> in load(self, arg_s)


    ~/anaconda3/envs/conbirt-env/lib/python3.6/site-packages/IPython/core/magic.py in <lambda>(f, *a, **k)
        185     # but it's overkill for just that one bit of state.
        186     def magic_deco(arg):
    --> 187         call = lambda f, *a, **k: f(*a, **k)
        188 
        189         if callable(arg):


    ~/anaconda3/envs/conbirt-env/lib/python3.6/site-packages/IPython/core/magics/code.py in load(self, arg_s)
        333         search_ns = 'n' in opts
        334 
    --> 335         contents = self.shell.find_user_code(args, search_ns=search_ns)
        336 
        337         if 's' in opts:


    ~/anaconda3/envs/conbirt-env/lib/python3.6/site-packages/IPython/core/interactiveshell.py in find_user_code(self, target, raw, py_only, skip_encoding_cookie, search_ns)
       3588         except Exception:
       3589             raise ValueError(("'%s' was not found in history, as a file, url, "
    -> 3590                                 "nor in the user namespace.") % target)
       3591 
       3592         if isinstance(codeobj, str):


    ValueError: '../src/bin/parsebat.py # contains parse_batlab_mat function' was not found in history, as a file, url, nor in the user namespace.

