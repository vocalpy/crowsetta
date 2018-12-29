import numpy as np
from scipy.io import loadmat

from crowsetta.classes import Sequence


def batlab2seq(file):
    """unpack BatLAB annotation into Sequence object

    example of a function that unpacks annotation from
    a complicated data structure and returns the necessary
    data from a Sequence object"""
    mat = loadmat(file, squeeze_me=True)
    seq_list = []
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
        onsets_s = annotation['segOnset'].tolist()
        offsets_s = annotation['segOffset'].tolist()
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
                             "not recognized.".format(wav_filename,
                                                      type(labels)))
        BATLAB_SAMP_FREQ = 33100
        onsets_Hz = np.round(onsets_s * BATLAB_SAMP_FREQ).astype(int)
        offsets_Hz = np.round(onsets_s * BATLAB_SAMP_FREQ).astype(int)

        seq = Sequence.from_keyword(file=filename,
                                    labels=labels,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz)
        seq_list.append(seq)
    return seq_list
