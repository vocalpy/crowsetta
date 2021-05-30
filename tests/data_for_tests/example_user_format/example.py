import numpy as np
from scipy.io import loadmat

from crowsetta import Sequence, Annotation


def example2annot(annot_path):
    """example of a function that unpacks annotation from
    a complicated data structure and returns the necessary
    data from an Annotation object"""
    mat = loadmat(annot_path, squeeze_me=True)
    annot_list = []
    # annotation structure loads as a Python dictionary with two keys
    # one maps to a list of filenames, 
    # and the other to a Numpy array where each element is the annotation
    # coresponding to the filename at the same index in the list.
    # We can iterate over both by using the zip() function.
    for filename, annotation in zip(mat['filenames'], mat['annotations']):
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
        annot_list.append(Annotation(annot_path=annot_path, audio_path=filename, seq=seq))

    return annot_list
