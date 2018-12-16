import os
import unittest

import numpy as np

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


def example_func(annot_dict):
    # below, the first .tolist() does not actually create list,
    # instead gets ndarray out of a zero-length ndarray of dtype=object.
    # This is just weirdness that results from loading complicated data
    # structure in .mat file.
    labels = annot_dict['segType'].tolist()
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


class TestConbirt(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fromfunc(self):
        pass
