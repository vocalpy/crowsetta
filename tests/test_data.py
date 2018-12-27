import tempfile
import shutil
import unittest

import crowsetta


class TestData(unittest.TestCase):
    def setUp(self):
        self.tmp_download_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_download_dir)

    def test_formats(self):
        # make sure calling formats() gives us back some string
        formats_func_output = crowsetta.formats()
        self.assertTrue(type(formats_func_output) == str)
        formats = list(crowsetta.data.FORMATS.keys())
        for format in formats:
            # and that string should have the different formats in it somewhere
            self.assertTrue(format in formats_func_output)

    def test_fetch(self):
        # make sure downloading each example works without an error
        formats = list(crowsetta.data.FORMATS.keys())
        for format in formats:
            crowsetta.data.fetch(format=format,
                                 destination_path=self.tmp_download_dir)


if __name__ == '__main__':
    unittest.main()
