"""utilities for input validation.

Some utilities adapted from scikit-learn under BSD 3 License
https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/validation.py
"""
import numbers
from pathlib import Path, PurePath

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


def validate_ext(file, extension):
    """"check that all files have valid extensions,
    convert into a list that can be iterated over

    Parameters
    ----------
    file : str, pathlib.Path, list
        filename(s), list must be of str or pathlib.Path
    extension : str, tuple
        valid file extension(s). tuple must be tuple of strings.
        Function expects that extensions will be specified with a period,
        e.g. {'.phn', '.PHN'}

    Returns
    -------
    files_validated : list
        of filenames, all having validated extensions
    """
    if isinstance(extension, str):
        extension = (extension,)
    elif isinstance(extension, tuple):
        if not all([isinstance(element, str) for element in extension]):
            raise TypeError(
                "must specify all valid extensions as strings, but value was \n"
                f"'{extension}' with types: {[type(element) for element in extension]}"
            )
    else:
        raise TypeError(
            f'extension must be str or tuple but type was {type(extension)}'
        )

    if not(isinstance(file, str) or isinstance(file, PurePath) or isinstance(file, list)):
        raise TypeError(
            f"file must be a str or a pathlib.Path, but type of file was {type(file)}.\n"
            f"File was: {file}"
        )

    if isinstance(file, list):
        if not(all([isinstance(a_file, str) for a_file in file]) or
               all([isinstance(a_file, PurePath) for a_file in file])):
            raise ValueError(
                f'all files in list of files must be either string or pathlib.Path'
            )

    if isinstance(file, str) or isinstance(file, PurePath):
        # put in a list to iterate over
        file = [file]

    file_out = []
    for a_file in file:
        # cast to string (if it's not already, e.g. it's a Path)
        # so we can use .endswith() to compare extensions
        # (because using Path.suffixes() would require too much special casing)
        a_file = str(a_file)
        if not a_file.endswith(extension):
            raise ValueError(f"file does not have a valid extension: {a_file}"
                             f"valid extension(s) for filenames are: '{extension}'")
        file_out.append(a_file)

    return file_out
