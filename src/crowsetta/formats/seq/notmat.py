"""Module with functions that handle .not.mat annotation files
produced by evsonganaly GUI.
"""

from __future__ import annotations

import pathlib
from typing import ClassVar, Dict, Optional

import attr
import numpy as np
import scipy.io

import crowsetta
from crowsetta.typing import PathLike


def load_notmat(filename: PathLike) -> dict:
    """loads .not.mat files created by evsonganaly (Matlab GUI for labeling song)

    Parameters
    ----------
    filename : str
        name of .not.mat file, can include path

    Returns
    -------
    notmat_dict : dict
        variables from .not.mat files

    Examples
    --------
    >>> a_notmat = 'gy6or6_baseline_230312_0808.138.cbin.not.mat'
    >>> notmat_dict = load_notmat(a_notmat)
    >>> notmat_dict.keys()
    dict_keys(['__header__', '__version__', '__globals__', 'Fs', 'fname', 'labels',
    'onsets', 'offsets', 'min_int', 'min_dur', 'threshold', 'sm_win'])

    Notes
    -----
    Basically a wrapper around `scipy.io.loadmat`. Calls `loadmat` with `squeeze_me=True`
    to remove extra dimensions from arrays that `loadmat` parser sometimes adds.

    Also note that **onsets and offsets from .not.mat files are in milliseconds**.
    The GUI `evsonganaly` saves onsets and offsets in these units,
    and we avoid converting them here for consistency and interoperability
    with Matlab code.
    """
    filename = pathlib.Path(filename)

    # have to cast to str and call endswith because 'ext' from Path will just be .mat
    if str(filename).endswith(".not.mat"):
        pass
    elif str(filename).endswith("cbin"):
        filename = filename.parent.joinpath(filename.name + ".not.mat")
    else:
        ext = filename.suffix
        raise ValueError(f"Filename should have extension .cbin.not.mat or .cbin but extension was: {ext}")
    notmat_dict = scipy.io.loadmat(filename, squeeze_me=True)
    # ensure that onsets and offsets are always arrays, not scalar
    for key in ("onsets", "offsets"):
        if np.isscalar(notmat_dict[key]):  # `squeeze_me` makes them a ``float``, this will be True in that case
            value = np.array(notmat_dict[key])[np.newaxis]  # ``np.newaxis`` ensures 1-d array with shape (1,)
            notmat_dict[key] = value
    return notmat_dict


@crowsetta.interface.SeqLike.register
@attr.define
class NotMat:
    """Class that represents annotations
    from .not.mat files
    produced by evsonganaly GUI.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'notmat'``.
    ext: str
        Extension of files in annotation format: ``'.not.mat'``.
    onsets : numpy.ndarray
        Onset times of segments, in seconds.
    offsets : numpy.ndarray
        Offset times of segments, in seconds.
    labels : numpy.ndarray
        Labels for segments.
    annot_path : str, pathlib.Path
        Path to .not.mat file from which
        annotations were loaded.
    audio_path : str, pathlib.Path
        Path to audio file that ``annot_path`` annotates.

    Notes
    -----
    This class uses code adapted from the Python package ``evfuncs``
    to load the annotations.
    https://github.com/NickleDave/evfuncs
    """

    name: ClassVar[str] = "notmat"
    ext: ClassVar[str] = ".not.mat"

    onsets: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    offsets: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    labels: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path
    audio_path: pathlib.Path

    @classmethod
    def from_file(cls, annot_path: PathLike) -> "Self":  # noqa: F821
        """load annotations from .not.mat file

        Parameters
        ----------
        annot_path: str, pathlib.Path
            Path to a .not.mat file saved by the evsonganaly GUI.

        Examples
        --------
        >>> path = crowsetta.example('notmat', return_path=True)
        >>> notmat = crowsetta.formats.seq.NotMat.from_file(path)
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)
        notmat_dict = load_notmat(annot_path)
        # in .not.mat files saved by evsonganaly,
        # onsets and offsets are in units of ms, have to convert to s
        onsets = notmat_dict["onsets"] / 1000
        offsets = notmat_dict["offsets"] / 1000
        labels = np.asarray(list(notmat_dict["labels"]))

        audio_path = annot_path.parent / annot_path.name.replace(".not.mat", "")
        return cls(annot_path=annot_path, onsets=onsets, offsets=offsets, labels=labels, audio_path=audio_path)

    def to_seq(self, round_times: bool = True, decimals: int = 3) -> crowsetta.Sequence:
        """Convert this .not.mat annotation to a :class:`crowsetta.Sequence`.

        Parameters
        ----------
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.

        Returns
        -------
        seq : crowsetta.Sequence

        Examples
        --------
        >>> path = crowsetta.example('notmat', return_path=True)
        >>> notmat = crowsetta.formats.seq.NotMat.from_file(path)
        >>> seq = notmat.to_seq()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        if round_times:
            onsets = np.around(self.onsets, decimals=decimals)
            offsets = np.around(self.offsets, decimals=decimals)
        else:
            onsets = self.onsets
            offsets = self.offsets

        seq = crowsetta.Sequence.from_keyword(labels=self.labels, onsets_s=onsets, offsets_s=offsets)
        return seq

    def to_annot(self, round_times: bool = True, decimals: int = 3) -> crowsetta.Annotation:
        """Convert this .not.mat annotation to a :class:`crowsetta.Annotation`.

        Parameters
        ----------
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.

        Returns
        -------
        annot : crowsetta.Annotation

        Examples
        --------
        >>> path = crowsetta.example('notmat', return_path=True)
        >>> notmat = crowsetta.formats.seq.NotMat.from_file(path)
        >>> annot = notmat.to_annot()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        seq = self.to_seq(round_times=round_times, decimals=decimals)

        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, seq=seq)

    def to_file(
        self,
        samp_freq: int,
        threshold: int,
        min_syl_dur: float,
        min_silent_dur: float,
        fname: Optional[PathLike] = None,
        dst: Optional[PathLike] = None,
        other_vars: Optional[Dict] = None,
    ) -> None:
        """Save as a .not.mat file
        that can be read by evsonganaly
        (MATLAB GUI for annotating vocalizations).

        Parameters
        ----------
        samp_freq : int
            Sampling frequency of audio file.
        threshold : int
            Value above which amplitude is considered part of a segment.
            Default is 5000.
        min_syl_dur : float
            Minimum duration of a segment.
            Default is 0.02, i.e. 20 ms.
        min_silent_dur : float
            Minimum duration of silent gap between segment.
            Default is 0.002, i.e. 2 ms.
        fname : str, pathlib.Path
            Name of audio file associated with .not.mat,
            will be used as base of name for .not.mat file.
            e.g., if filename is
            'bl26lb16\041912\bl26lb16_190412_0721.20144.cbin'
            then the .not.mat file will be
            'bl26lb16\041912\bl26lb16_190412_0721.20144.cbin.not.mat'
            Default is None,
            in which case ``self.audio_path.name`` is used.
        dst : str, pathlib.Path
            Directory where `.not.mat` should be saved.
            Default is None, in which case it is saved in the
            parent directory of ``fname``.
        other_vars : dict
            Mapping from variable names to other variables that should be saved
            in the .not.mat file, e.g., if you need to add a variable named 'pitches'
            that is an numpy array of float values.
        """
        if fname is None:
            fname = self.audio_path
        else:
            fname = pathlib.Path(fname)

        if dst is not None:
            dst = pathlib.Path(dst)
            if not dst.is_dir():
                raise NotADirectoryError(f"Destination `dst` for .not.mat is not recognized as a directory: {dst}")

        if other_vars is not None:
            if not isinstance(other_vars, dict):
                raise TypeError(f"other_vars must be a dict, not a {type(other_vars)}")
            if not all(isinstance(key, str) for key in other_vars.keys()):
                raise TypeError("all keys for other_vars dict must be of type str")

        # chr() to convert back to character from uint32
        if self.labels.dtype == "int32":
            labels = [chr(val) for val in self.labels]
        elif self.labels.dtype == "<U1":
            labels = self.labels.tolist()
        else:
            raise TypeError(f"invalid dtype for self.labels: {self.labels.dtype}")

        # convert into one long string, what evsonganaly expects
        labels = "".join(labels)
        # notmat files have onsets/offsets in units of ms
        # need to convert back from s
        onsets = (self.onsets * 1e3).astype(float)
        offsets = (self.offsets * 1e3).astype(float)

        # same goes for min_int and min_dur
        # also wrap everything in float so Matlab loads it as double
        # because evsonganaly expects doubles
        notmat_dict = {
            "fname": str(fname),
            "Fs": float(samp_freq),
            "min_dur": float(min_syl_dur * 1e3),
            "min_int": float(min_silent_dur * 1e3),
            "offsets": offsets,
            "onsets": onsets,
            "labels": labels,
            "sm_win": float(2),  # evsonganaly.m doesn't actually let user change this value
            "threshold": float(threshold),
        }

        if other_vars:
            notmat_dict.update(other_vars)

        notmat_name = fname.name + ".not.mat"
        if dst:
            notmat_path = dst / notmat_name
        else:
            notmat_path = fname.parent / notmat_name
        if notmat_path.exists():
            raise FileExistsError(f"File already exists: {notmat_path}")
        else:
            scipy.io.savemat(notmat_path, notmat_dict)
