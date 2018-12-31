import sys
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import crowsetta

TESTS_DIR = Path(__file__).resolve().parent  # same as os.path.dirname(__file__)


class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.tmp_output_dir = Path(tempfile.mkdtemp())
        self.test_data_dir = TESTS_DIR.joinpath('test_data')
        self.example_script_dir = TESTS_DIR.joinpath('test_scripts/')

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_koumura_to_seq(self):
        scribe = crowsetta.Transcriber()
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        seq = scribe.to_seq(file=xml_file, file_format='koumura', wavpath=wavpath)
        self.assertTrue(type(seq) == list)
        self.assertTrue(all([type(a_seq) == crowsetta.classes.Sequence
                             for a_seq in seq]))

    def test_koumura_to_csv(self):
        scribe = crowsetta.Transcriber()
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=xml_file, file_format='koumura', wavpath=wavpath,
                    csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_notmat_to_seq(self):
        scribe = crowsetta.Transcriber()
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        for notmat in notmats:
            seq = scribe.to_seq(file=notmat, file_format='notmat')
            self.assertTrue(type(seq) == crowsetta.classes.Sequence)

    def test_notmat_to_csv(self):
        scribe = crowsetta.Transcriber()
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=notmats, file_format='notmat', csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_example_to_seq_name_import(self):
        sys.path.append(str(self.example_script_dir))
        user_config = {
            'example': {
                'module': 'example',
                'to_seq': 'example2seq',
                'to_csv': 'example2csv',
                'to_format': 'None',
            }
        }
        scribe = crowsetta.Transcriber(user_config=user_config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        seq = scribe.to_seq(file=annotation, file_format='example')
        self.assertTrue(all([type(a_seq) == crowsetta.Sequence for a_seq in seq]))

    def test_example_to_seq_path_import(self):
        user_config = {
            'example': {
                'module': str(self.example_script_dir.joinpath('example.py')),
                'to_seq': 'example2seq',
                'to_csv': None,
                'to_format': None,
            }
        }
        scribe = crowsetta.Transcriber(user_config=user_config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        seq = scribe.to_seq(file=annotation, file_format='example')
        self.assertTrue(all([type(a_seq)==crowsetta.Sequence for a_seq in seq]))

    def test_user_config_wrong_types_raise(self):
        # should raise an error because user_config should be dict of dicts
        # not list of dicts
        user_config = list(
            {'example': {
                'module': 'example',
                'to_seq': 'example2seq',
                'to_csv': 'example2csv',
                'to_format': 'None',
            }}
        )
        with self.assertRaises(TypeError):
            crowsetta.Transcriber(user_config=user_config)

    def test_missing_keys_in_config_raises(self):
        user_config = {
            'example': {
                # missing 'module' key
                'to_seq': 'example2seq',
                'to_csv': 'example2csv',
                'to_format': None,
            }
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(user_config=user_config)

    def test_extra_keys_in_config_raises(self):
        user_config = {
            'example': {
                'module': 'example',
                'to_seq': 'example2seq',
                'to_csv': 'example2csv',
                'extra': 'key_right_here',
                'to_format': 'None',
            }
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(user_config=user_config)

    def test_from_csv(self):
        csv_filename = os.path.join(self.test_data_dir,
                                    os.path.normpath('csv/gy6or6_032312.csv'))
        # just a wrapper around `csv2seq` which has its own tests,
        # so here just make sure it works as a class method
        scribe = crowsetta.Transcriber()
        seq = scribe.from_csv(csv_filename=csv_filename)
        self.assertTrue(type(seq) == list)
        self.assertTrue(all([type(a_seq) == crowsetta.classes.Sequence
                             for a_seq in seq]))

if __name__ == '__main__':
    unittest.main()
