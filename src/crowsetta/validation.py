"""Module with functions for data validation.

Some utilities adapted from scikit-learn under BSD 3 License
https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/validation.py
"""

import numbers
from pathlib import PurePath
from typing import Sequence, Union

import numpy as np
import numpy.typing as npt

from .typing import PathLike


def _num_samples(x: npt.ArrayLike) -> int:
    """Return number of samples in array-like x."""
    if not hasattr(x, "__len__") and not hasattr(x, "shape"):
        if hasattr(x, "__array__"):
            x = np.asarray(x)
        else:
            raise TypeError("Expected sequence or array-like, got %s" % type(x))
    if hasattr(x, "shape"):
        if len(x.shape) == 0:
            raise TypeError("Singleton array %r cannot be considered" " a valid collection." % x)
        # Check that shape is returning an integer or default to len
        # Dask dataframes may not return numeric shape[0] value
        if isinstance(x.shape[0], numbers.Integral):
            return x.shape[0]
        else:
            return len(x)
    else:
        return len(x)


def check_consistent_length(arrays: Sequence[npt.ArrayLike]) -> None:
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
        raise ValueError(
            "Found input variables with inconsistent numbers of" " samples: %r" % [int(length) for length in lengths]
        )


def column_or_row_or_1d(y: npt.NDArray) -> npt.NDArray:
    """Ravel column or row vector or 1d numpy array,
    else raises an error

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


def validate_ext(file: PathLike, extension: Union[str, tuple]) -> None:
    """Check that a file has a valid extension.

    Parameters
    ----------
    file : str, pathlib.Path
        Path to a file.
    extension : str, tuple
        Valid file extension(s). Tuple must be tuple of strings.
        Function expects that extensions will be specified with a period,
        e.g. {'.phn', '.PHN'}
    """
    if isinstance(extension, str):
        extension = (extension,)
    elif isinstance(extension, tuple):
        if not all([isinstance(element, str) for element in extension]):
            raise TypeError(
                "Must specify all valid extensions as strings, but value was \n"
                f"'{extension}' with types: {[type(element) for element in extension]}"
            )
    else:
        raise TypeError(f"Extension must be str or tuple but type was {type(extension)}")

    if not (isinstance(file, str) or isinstance(file, PurePath)):
        raise TypeError(f"File must be a str or a pathlib.Path, but type of file was {type(file)}.\n" f"File: {file}")

    # we need to use `endswith` instead of
    # e.g. comparing with `pathlib.Path.suffix`
    # because suffix won't work for "multi-part" extensions like '.not.mat'
    if not any([str(file).endswith(ext) for ext in extension]):
        raise ValueError(f"Invalid extension for file: {file}.\n" f"Valid extension(s): '{extension}'")
