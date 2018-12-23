.. Crowsetta documentation master file, created by
   sphinx-quickstart on Sat Dec 22 21:16:45 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Crowsetta
=========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

``crowsetta`` is a tool to work with any format for annotating birdsong.
**The goal of** ``crowsetta`` **is to make sure that your ability to work with a dataset 
of birdsong does not depend on your ability to work with any given format for 
annotating that dataset.** 

.. code-block:: python

    from crowsetta import Crowsetta
    crow = Crowsetta(extra_config=your_config_info)
    crow.to_csv(file_'your_annotation_file.mat',
                csv_filename='your_annotation.csv')

Features
--------

- convert annotation formats to ``Sequence`` objects that can be easily used in a Python program
- convert ``Sequence`` objects to comma-separated value text files that can be read on any system
- load comma-separated values files back into Python and convert to other formats
- easily use with your own annotation format

Getting Started
---------------

Install ``crowsetta`` by running:

.. code-block:: console

    $ pip install crowsetta
    

If you are new to the library, start with :doc:`intro`.

To see an example of using ``crowsetta`` to work with your own annotation format, 
see :doc:`example`.

Project Information
-------------------

Support
~~~~~~~

If you are having issues, please let us know.

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues

Contribute
~~~~~~~~~~

- Issue Tracker: https://github.com/NickleDave/crowsetta/issues
- Source Code: https://github.com/NickleDave/crowsetta

License
~~~~~~~

The project is licensed under the 
`BSD license <https://github.com/NickleDave/crowsetta/blob/master/LICENSE>`_.

CHANGELOG
~~~~~~~~~
You can see project history and work in progress in the 
`CHANGELOG <https://github.com/NickleDave/crowsetta/blob/master/doc/CHANGELOG.md>`_.

Citation
~~~~~~~~
If you use ``crowsetta``, please cite the DOI:


Table of Contents
-----------------
.. toctree::
   intro
   example
