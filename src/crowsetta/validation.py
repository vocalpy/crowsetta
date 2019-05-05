"""utilities for input validation.

Some utilities adapted from scikit-learn under BSD 3 License
https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/validation.py
"""
import numbers
from pathlib import Path

import numpy as np


def _num_samples(x):
    """Return number of samples in array-like x."""
    if not hasattr(x, '__len__') and not hasattr(x, 'shape'):
        if hasattr(x, '__array__'):
            x = np.asarray(x)
        else:
            raise TypeError("Expected sequence or array-like, got %s" %
                            type(x))
    if hasattr(x, 'shape'):
        if len(x.shape) == 0:
            raise TypeError("Singleton array %r cannot be considered"
                            " a valid collection." % x)
        # Check that shape is returning an integer or default to len
        # Dask dataframes may not return numeric shape[0] value
        if isinstance(x.shape[0], numbers.Integral):
            return x.shape[0]
        else:
            return len(x)
    else:
        return len(x)


def check_consistent_length(arrays):
    """Check that all arrays have consistent first dimensions.
    Checks whether all objects in arrays have the same shape or length.
    Parameters
    ----------
    arrays : list or tuple of input objects.
        Objects that will be checked for consistent length.
    """
    lengths = [_num_samples(X) for X in arrays if X is not None]
    uniques = np.unique(lengths)
    if len(uniques) > 1:
        raise ValueError("Found input variables with inconsistent numbers of"
                         " samples: %r" % [int(l) for l in lengths])


def column_or_row_or_1d(y):
    """Ravel column or row vector or 1d numpy array, else raises an error

    Parameters
    ----------
    y : array-like

    Returns
    -------
    y : array
    """
    shape = np.shape(y)
    if (len(shape) == 1) or (len(shape) == 2 and (shape[1] == 1 or shape[0] == 1)):
        return np.ravel(y)
    else:
        raise ValueError("bad input shape {0}".format(shape))


def _parse_file(file, extension):
    """helper function that parses/validates value for file argument;
    puts a single string or Path into a list to iterate over it (cheap hack
    that lets functions accept multiple types), and checks list to make sure
    all types are consistent
    """
    if type(file) == str or type(file) == Path:
        # put in a list to iterate over
        file = [file]

    for a_file in file:
        # cast to string (if it's not already, e.g. it's a Path)
        # so we can use .endswith() to compare extensions
        # (because using Path.suffixes() would require too much special casing)
        a_file = str(a_file)
        if not a_file.endswith(extension):
            raise ValueError(f"all filenames in 'file' must end with '{extension}' "
                             f"but {a_file} does not")

    return file
