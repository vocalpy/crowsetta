"""A class to represent annotations for a single file."""
from pathlib import Path
from typing import List, Optional

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
        path to file from which annotations were loaded
    notated_path : str, pathlib.Path
        path to file that ``annot_path`` annotates.
        E.g., an audio file, or an array file
        that contains a spectrogram generated from audio.
        Optional, default is None.
    seq : crowsetta.Sequence
        a sequence of annotated segments,
        each having an onset time, offset time,
        and label.
    bboxes : list
        of ``crowsetta.BBox``,
        annotated bounding boxes,
        each having an onset time, offset time,
        lowest frequency, highest frequency,
        and label.

    Notes
    -----
    A ``crowsetta.Annotation`` can have a ``seq``
    or ``bboxes``, but not both.
    """
    def __init__(self,
                 annot_path: PathLike,
                 notated_path: Optional[PathLike] = None,
                 seq: Optional[Sequence] = None,
                 bboxes: Optional[List[BBox]] = None):
        if seq is None and bboxes is None:
            raise ValueError(
                'an Annotation must have either a ``seq`` or ``bboxes``'
            )

        if seq is not None and bboxes is not None:
            raise ValueError(
                'an Annotation can have either a ``seq``'
                'or ``bboxes``, but not both.'
            )

        if seq:
            if not isinstance(seq, crowsetta.Sequence):
                raise TypeError(
                    f'``seq`` should be a ``crowsetta.Sequence`` but was: {type(seq)}'
                )
            self.seq = seq

        if bboxes:
            if not isinstance(bboxes, list):
                raise ValueError(
                    '``bboxes`` should be a list'
                )
            if not all(
                    [isinstance(bbox, BBox) for bbox in bboxes]
            ):
                raise ValueError(
                    '``bboxes`` should be a list of ``crowsetta.BBox`` instances'
                )
            self.bboxes = bboxes

        self.annot_path = Path(annot_path)
        if notated_path:
            self.notated_path = Path(notated_path)
        else:
            self.notated_path = notated_path

    def __repr__(self):
        repr_ = f'Annotation(annot_path={repr(self.annot_path)}, notated_path={repr(self.notated_path)}, '
        if hasattr(self, 'seq'):
            repr_ += f'seq={self.seq})'
        elif hasattr(self, 'bboxes'):
            repr_ += f'bboxes={self.bboxes})'
        return repr_

    def __eq__(self, other):
        is_annot_and_audio_eq = (self.annot_path == other.annot_path and
                                 self.notated_path == other.notated_path)
        if hasattr(self, 'seq') and hasattr(other, 'seq'):
            return is_annot_and_audio_eq and self.seq == other.seq
        elif hasattr(self, 'bboxes') and hasattr(other, 'bboxes'):
            return is_annot_and_audio_eq and self.bboxes == other.bboxes
        else:
            return False

    def __ne__(self, other):
        return not self == other
