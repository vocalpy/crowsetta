import os
import shutil
import tempfile
import unittest

import crowsetta

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestConbirt(unittest.TestCase):
    def setUp(self):
        self.tmp_output_dir = tempfile.mkdtemp()
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data'
        self.example_script_dir = os.path.join(TESTS_DIR,
                                               '..', 'src', 'bin')

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_koumura_to_seq_defaults(self):
        crow = Crowsetta()
        xml_file = os.path.join(self.test_data_dir,
                                'koumura', 'Bird0',
                                'Annotation.xml')
        seq = crow.to_seq(file=xml_file, file_format='koumura')

    def test_koumura_to_csv(self):
        pass

    def test_notmat_to_csv(self):
        pass

