"""Module for loading annotations from .mat files
created by SongAnnotationGUI:
https://github.com/yardencsGitHub/BirdSongBout/tree/master/helpers/GUI
"""

import os
import pathlib
from typing import ClassVar, List

import attr
import numpy as np
import scipy.io

import crowsetta
from crowsetta.typing import PathLike


def _cast_to_arr(val):
    """helper function that casts single elements to 1-d numpy arrays"""
    if isinstance(val, int) or isinstance(val, float):
        # this happens when there's only one syllable in the file
        # with only one corresponding label
        return np.asarray([val])  # so make it a one-element list
    elif isinstance(val, np.ndarray):
        # this should happen whenever there's more than one label
        return val
    else:
        # something unexpected happened
        raise TypeError(f"Type {type(val)} not recognized when converting annotations to arrays.")


VALID_AUDIO_FORMATS = ["wav"]


def _recursive_stem(path_str):
    """Helper function that 'recursively' removes file extensions
    to recover name of an audio file from the name of an array file

    i.e. bird1_122213_1534.wav.mat -> i.e. bird1_122213_1534.wav
    and i.e. bird1_122213_1534.cbin.not.mat -> i.e. bird1_122213_1534.cbin

    adapted from ``vak`` library
    """
    name = pathlib.Path(path_str).name
    stem, ext = os.path.splitext(name)
    ext = ext.replace(".", "")
    while ext not in VALID_AUDIO_FORMATS:
        new_stem, ext = os.path.splitext(stem)
        ext = ext.replace(".", "")
        if new_stem == stem:
            raise ValueError(f"unable to compute stem of {path_str}")
        else:
            stem = new_stem
    return stem


@crowsetta.interface.SeqLike.register
@attr.define
class SongAnnotationGUI:
    """Class that represents annotations
    from .mat files
    created by SongAnnotationGUI:
    https://github.com/yardencsGitHub/BirdSongBout/tree/master/helpers/GUI

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'yarden'``.
    ext: str
        Extension of files in annotation format: ``'.mat'``.
    annotations : numpy.ndarray
        A :mod:`numpy` record array where each record is an annotation.
    audio_paths : numpy.ndarray
        A :mod:`numpy` array where each element is a path to an audio file.
        Same length as ``annotations``. Each element in ``annotations``
        is the annotation for the corresponding path in ``audio_paths``.
    annot_path : str, pathlib.Path
        Path to mat file from which annotations were loaded.
    """

    name: ClassVar[str] = "yarden"
    ext: ClassVar[str] = ".mat"

    annotations: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    audio_paths: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path = attr.field(converter=pathlib.Path)

    @classmethod
    def from_file(cls, annot_path: PathLike) -> "Self":  # noqa: F821
        """Load annotations from mat files
        created by SongAnnotationGUI:
        https://github.com/yardencsGitHub/BirdSongBout/tree/master/helpers/GUI

        Parameters
        ----------
        annot_path: str, pathlib.Path
            Path to .mat file with annotations.
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        # annotation structure loads as a Python dictionary with two keys
        # one maps to a list of filenames,
        # and the other to a Numpy record array,
        # where each element is the annotation
        # corresponding to the filename at the same index in the list.
        annot_mat = scipy.io.loadmat(annot_path, squeeze_me=True)
        audio_paths = annot_mat["keys"]
        annotations = annot_mat["elements"]
        if len(audio_paths) != len(annotations):
            raise ValueError(f"list of filenames and list of annotations in {annot_path} do not have the same length")

        return cls(annotations=annotations, audio_paths=audio_paths, annot_path=annot_path)

    def to_seq(self, round_times: bool = True, decimals: int = 3) -> List[crowsetta.Sequence]:
        """Convert this set of annotations to a :class:`list` of
        :class:`crowsetta.Sequence` instances.

        We assume there is one :class:`~crowsetta.Sequence`
        per annotated song in the source annotations.

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
        seqs : list
            A :class:`list` of :class:`~crowsetta.Sequence` instances,
            one for each element in ``annotations``.

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        seqs = []
        for annotation in self.annotations:
            # below, .tolist() does not actually create a list,
            # instead gets ndarray out of a zero-length ndarray of dtype=object.
            # This is just weirdness that results from loading complicated data
            # structure in .mat file.
            seq_dict = {}
            seq_dict["onsets_s"] = annotation["segFileStartTimes"].tolist()
            seq_dict["offsets_s"] = annotation["segFileEndTimes"].tolist()
            seq_dict["labels"] = annotation["segType"].tolist()
            # cast all to numpy arrays
            seq_dict = dict((k, _cast_to_arr(seq_dict[k])) for k in ["onsets_s", "offsets_s", "labels"])
            # after casting 'labels' to array, convert all values to string
            seq_dict["labels"] = np.asarray([str(label) for label in seq_dict["labels"]])

            samp_freq = annotation["fs"].tolist()
            seq_dict["onset_samples"] = np.round(seq_dict["onsets_s"] * samp_freq).astype(int)
            seq_dict["offset_samples"] = np.round(seq_dict["offsets_s"] * samp_freq).astype(int)

            if round_times:
                seq_dict["onsets_s"] = np.around(seq_dict["onsets_s"], decimals=decimals)
                seq_dict["offsets_s"] = np.around(seq_dict["offsets_s"], decimals=decimals)

            seq = crowsetta.Sequence.from_dict(seq_dict)
            seqs.append(seq)

        return seqs

    def to_annot(self, round_times: bool = True, decimals: int = 3) -> List[crowsetta.Annotation]:
        """Convert this annotation to a :class:`crowsetta.Annotation`.

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
        annots : list
            A :class:`list` of :class:`crowsetta.Annotation` instances.

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        seqs = self.to_seq(round_times=round_times, decimals=decimals)
        annots = []
        for audio_path, seq in zip(self.audio_paths, seqs):
            annots.append(crowsetta.Annotation(annot_path=self.annot_path, notated_path=audio_path, seq=seq))
        return annots
