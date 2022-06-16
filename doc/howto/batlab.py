import pathlib
from typing import ClassVar

import attr
import numpy as np
import scipy.io

from crowsetta import Sequence, Annotation
from crowsetta.typing import PathLike
import crowsetta


@crowsetta.formats.register_format
@crowsetta.interface.SeqLike.register
@attr.define
class Batlab:
    """Example custom annotation format"""
    name: ClassVar[str] = 'batlab'
    ext: ClassVar[str] = '.mat'

    annotations: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    audio_paths: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path = attr.field(converter=pathlib.Path)

    @classmethod
    def from_file(cls,
                  annot_path: PathLike):
        """load BatLAB annotations from .mat file

        Parameters
        ----------
        mat_path : str, pathlib.Path
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        annot_mat = scipy.io.loadmat(annot_path, squeeze_me=True)

        audio_paths = annot_mat['filenames']
        annotations = annot_mat['annotations']
        if len(audio_paths) != len(annotations):
            raise ValueError(
                f'list of filenames and list of annotations in {mat_path} do not have the same length'
            )

        return cls(annotations=annotations,
                   audio_paths=audio_paths,
                   annot_path=annot_path)


    def to_seq(self):
        """unpack BatLAB annotation into list of Sequence objects

        example of a function that unpacks annotation from
        a complicated data structure and returns the necessary
        data as a Sequence object

        Returns
        -------
        seqs : list
            of Sequence objects
        """
        seqs = []
        # annotation structure loads as a Python dictionary with two keys
        # one maps to a list of filenames,
        # and the other to a Numpy array where each element is the annotation
        # coresponding to the filename at the same index in the list.
        # We can iterate over both by using the zip() function.
        for filename, annotation in zip(self.audio_paths, self.annotations):
            # below, .tolist() does not actually create a list,
            # instead gets ndarray out of a zero-length ndarray of dtype=object.
            # This is just weirdness that results from loading complicated data
            # structure in .mat file.
            onsets_s = annotation['segFileStartTimes'].tolist()
            offsets_s = annotation['segFileEndTimes'].tolist()
            labels = annotation['segType'].tolist()
            if type(labels) == int:
                # this happens when there's only one syllable in the file
                # with only one corresponding label
                seg_types = np.asarray([seg_types])  # so make it a one-element list
            elif type(labels) == np.ndarray:
                # this should happen whenever there's more than one label
                pass
            else:
                # something unexpected happened
                raise ValueError("Unable to load labels from {}, because "
                                 "the segType parsed as type {} which is "
                                 "not recognized.".format(audio_path,
                                                          type(seg_types)))
            samp_freq = annotation['fs'].tolist()

            seq = Sequence.from_keyword(labels=labels,
                                        onsets_s=onsets_s,
                                        offsets_s=offsets_s)
            seqs.append(seq)
        return seqs

    def to_annot(self):
        """example of a function that unpacks annotation
        and returns the necessary data as a
        ``crowsetta.Annotation``"""

        seqs = self.to_seq()

        annot_list = []
        # annotation structure loads as a Python dictionary with two keys
        # one maps to a list of filenames,
        # and the other to a Numpy array where each element is the annotation
        # corresponding to the filename at the same index in the list.
        # We can iterate over both by using the zip() function.
        for filename, seq in zip(self.audio_paths, seqs):
            annot_list.append(Annotation(annot_path=self.annot_path,
                                         notated_path=filename,
                                         seq=seq))

        return annot_list
