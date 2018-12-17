from crowsetta.sequence import Sequence


def example2seq(file):
    """example of a function that unpacks a complicated data structure
    and returns a Sequence object"""
    # below, the first .tolist() does not actually create list,
    # instead gets ndarray out of a zero-length ndarray of dtype=object.
    # This is just weirdness that results from loading complicated data
    # structure in .mat file.
    labels = file['segType'].tolist()
    if type(labels) == int:
        # this happens when there's only one syllable in the file
        # with only one corresponding label
        labels = np.asarray([labels])  # so make it a one-element list
    elif type(labels) == np.ndarray:
        pass
    else:
        raise ValueError("Unable to load labels from {}, because "
                         "the segType parsed as type {} which is "
                         "not recognized.".format(wav_filename,
                                                  type(labels)))
