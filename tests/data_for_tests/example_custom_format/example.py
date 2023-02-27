import pathlib
from typing import ClassVar

import attr
import numpy as np
import scipy.io

import crowsetta
from crowsetta import Annotation, Sequence
from crowsetta.typing import PathLike


@crowsetta.formats.register_format
@crowsetta.interface.SeqLike.register
@attr.define
class Custom:
    """Example custom annotation format"""
    name: ClassVar[str] = 'example-custom-format'
    ext: ClassVar[str] = '.mat'

    annotations: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    audio_paths: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path = attr.field(converter=pathlib.Path)

    @classmethod
    def from_file(cls,
                  annot_path: PathLike) -> 'Self':
        """load annotations from .mat files

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
        audio_paths = annot_mat['filenames']
        annotations = annot_mat['annotations']
        if len(audio_paths) != len(annotations):
            raise ValueError(
                f'list of filenames and list of annotations in {annot_path} do not have the same length'
            )

        return cls(annotations=annotations,
                   audio_paths=audio_paths,
                   annot_path=annot_path)

    def to_seq(self):
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
                labels = np.asarray([labels])  # so make it a one-element list
            elif type(labels) == np.ndarray:
                # this should happen whenever there's more than one label
                pass
            else:
                # something unexpected happened
                raise ValueError("Unable to load labels from {}, because "
                                 "the segType parsed as type {} which is "
                                 "not recognized.".format(filename,
                                                          type(labels)))
            seq = Sequence.from_keyword(labels=labels,
                                        onsets_s=onsets_s,
                                        offsets_s=offsets_s)
            seqs.append(seq)
        return seqs

    def to_annot(self):
        """example of a function that unpacks annotation from
        a complicated data structure and returns the necessary
        data from an Annotation object"""
        seqs = self.to_seq()

        annot_list = []
        # annotation structure loads as a Python dictionary with two keys
        # one maps to a list of filenames,
        # and the other to a Numpy array where each element is the annotation
        # coresponding to the filename at the same index in the list.
        # We can iterate over both by using the zip() function.
        for filename, seq in zip(self.audio_paths, seqs):
            annot_list.append(Annotation(annot_path=self.annot_path,
                                         notated_path=filename,
                                         seq=seq))

        return annot_list
