import unittest

import numpy as np

from crowsetta.classes import Sequence


class TestSequence(unittest.TestCase):
    def test_from_keyword_bad_labels_type_raises(self):
        with self.assertRaises(TypeError):
            file = '0.wav'
            labels = 12345
            onsets_Hz = np.asarray([0, 2, 4, 6, 8])
            offsets_Hz = np.asarray([1, 3, 5, 7, 9])
            Sequence.from_keyword(file=file, labels=labels, 
                                  onsets_Hz=onsets_Hz, offsets_Hz=offsets_Hz)

    

if __name__ == '__main__':
    unittest.main()
