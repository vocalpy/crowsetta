import numpy as np
from scipy.io import loadmat


def parse_batlab_mat(mat_file):
    """parse batlab annotation.mat file"""
    mat = loadmat(mat_file, squeeze_me=True)
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
        seg_start_times = annotation['segFileStartTimes'].tolist()
        seg_end_times = annotation['segFileEndTimes'].tolist()
        seg_types = annotation['segType'].tolist()
        if type(seg_types) == int:
            # this happens when there's only one syllable in the file
            # with only one corresponding label
            seg_types = np.asarray([seg_types])  # so make it a one-element list
        elif type(seg_types) == np.ndarray:
            # this should happen whenever there's more than one label
            pass
        else:
            # something unexpected happened
            raise ValueError("Unable to load labels from {}, because "
                             "the segType parsed as type {} which is "
                             "not recognized.".format(filename,
                                                      type(seg_types)))
        samp_freq = annotation['fs'].tolist()
        seg_start_times_Hz = np.round(seg_start_times * samp_freq).astype(int)
        seg_end_times_Hz = np.round(seg_end_times * samp_freq).astype(int)
        annot_dict = {
            'audio_file': filename,
            'seg_types': seg_types,
            'seg_start_times': seg_start_times,
            'seg_end_times': seg_end_times,
            'seg_start_times_Hz': seg_start_times_Hz,
            'seg_end_times_Hz': seg_end_times_Hz,
        }
        annot_list.append(annot_dict)

    return annot_list
