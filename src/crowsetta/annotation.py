"""A class to represent annotations for a single file."""

from __future__ import annotations

import reprlib
from pathlib import Path
from typing import Optional

import crowsetta

from .bbox import BBox
from .sequence import Sequence
from .typing import PathLike


class Annotation:
    """A class to represent annotations for a single file.

    The annotations can be one of two types:
    a single sequence, or a list of bounding boxes.

    Attributes
    ----------
    annot_path : str, pathlib.Path
        Path to file from which annotations were loaded.
    notated_path : str, pathlib.Path
        Path to file that ``annot_path`` annotates.
        E.g., an audio file, or an array file
        that contains a spectrogram generated from audio.
        Optional, default is None.
    seq : crowsetta.Sequence, list
        A :class:`crowsetta.Sequence` instance,
        or a list of :class:`crowsetta.Sequence` instances.
        Each :class:`crowsetta.Sequence` instance
        represents a sequence of annotated segments,
        with a segment having an onset time, offset time,
        and label.
    bboxes : list
        List of annotated bounding boxes,
        each having an onset time, offset time,
        lowest frequency, highest frequency,
        and label.
        Each item in the list will be a
        :class:`crowsetta.BBox` instance.

    Notes
    -----
    A :class:`crowsetta.Annotation` can have either a ``seq``
    attribute or a ``bboxes`` attribute, but not both.

    Examples
    --------

    A toy example of a sequence-like annotation.

    >>> import numpy as np
    >>> import crowsetta
    >>> onsets_s = np.array([1.0, 3.0, 5.0])
    >>> offsets_s = np.array([2.0, 4.0, 6.0])
    >>> labels = np.array(['a', 'a', 'b'])
    >>> seq = crowsetta.Sequence.from_keyword(labels=labels, onsets_s=onsets_s, offsets_s=offsets_s)
    >>> annot = crowsetta.Annotation(notated_path='bird1.wav', annot_path='bird1.csv', seq=seq)
    >>> print(annot)
    Annotation(annot_path=PosixPath('bird1.csv'), notated_path=PosixPath('bird1.wav'), seq=<Sequence with 3 segments>)

    A toy example of a bounding box-like annotation.

    >>> bbox1 = crowsetta.BBox(label='Pinacosaurus grangeri', onset=1.0, offset=2.0, low_freq=3e3, high_freq=1e4)
    >>> bbox2 = crowsetta.BBox(label='Pinacosaurus grangeri', onset=3.0, offset=4.0, low_freq=3.25e3, high_freq=1.25e4)
    >>> bboxes = [bbox1, bbox2]
    >>> annot = crowsetta.Annotation(notated_path='prebird1.wav', annot_path='prebird1.csv', bboxes=bboxes)
    >>> print(annot)
    Annotation(annot_path=PosixPath('prebird1.csv'), notated_path=PosixPath('prebird1.wav'),
    bboxes=[BBox(onset=1.0, offset=2.0, low_freq=3000.0, high_freq=10000.0, label='Pinacosaurus grangeri'),
    BBox(onset=3.0, offset=4.0, low_freq=3250.0, high_freq=12500.0, label='Pinacosaurus grangeri')])
    """

    def __init__(
        self,
        annot_path: PathLike,
        notated_path: Optional[PathLike] = None,
        seq: Optional[Sequence | list[Sequence]] = None,
        bboxes: Optional[list[BBox]] = None,
    ):
        if seq is None and bboxes is None:
            raise ValueError("an Annotation must have either a ``seq`` or ``bboxes``")

        if seq is not None and bboxes is not None:
            raise ValueError("an Annotation can have either a ``seq``" "or ``bboxes``, but not both.")

        if seq:
            if not (
                isinstance(seq, crowsetta.Sequence)
                or (isinstance(seq, list) and all([isinstance(seq_, crowsetta.Sequence) for seq_ in seq]))
            ):
                raise TypeError(f"``seq`` should be a crowsetta.Sequence or list of Sequences but was: {type(seq)}")
            self.seq = seq

        if bboxes:
            if not isinstance(bboxes, list):
                raise ValueError("``bboxes`` should be a list")
            if not all([isinstance(bbox, BBox) for bbox in bboxes]):
                raise ValueError("``bboxes`` should be a list of ``crowsetta.BBox`` instances")
            self.bboxes = bboxes

        self.annot_path = Path(annot_path)
        if notated_path:
            self.notated_path = Path(notated_path)
        else:
            self.notated_path = notated_path

    def __repr__(self):
        repr_ = f"Annotation(annot_path={repr(self.annot_path)}, notated_path={repr(self.notated_path)}, "
        if hasattr(self, "seq"):
            repr_ += f"seq={reprlib.repr(self.seq)})"
        elif hasattr(self, "bboxes"):
            repr_ += f"bboxes={reprlib.repr(self.bboxes)})"
        return repr_

    def __eq__(self, other):
        is_annot_and_audio_eq = self.annot_path == other.annot_path and self.notated_path == other.notated_path
        if hasattr(self, "seq") and hasattr(other, "seq"):
            return is_annot_and_audio_eq and self.seq == other.seq
        elif hasattr(self, "bboxes") and hasattr(other, "bboxes"):
            return is_annot_and_audio_eq and self.bboxes == other.bboxes
        else:
            return False

    def __ne__(self, other):
        return not self == other
