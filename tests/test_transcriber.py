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
        scribe = crowsetta.Transcriber(voc_format='koumura')
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        seq = scribe.to_seq(file=xml_file, wavpath=wavpath)
        self.assertTrue(type(seq) == list)
        self.assertTrue(all([type(a_seq) == crowsetta.sequence.Sequence
                             for a_seq in seq]))

    def test_koumura_to_csv(self):
        scribe = crowsetta.Transcriber(voc_format='koumura')
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=xml_file, wavpath=wavpath, csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_notmat_to_seq(self):
        scribe = crowsetta.Transcriber(voc_format='notmat')
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        for notmat in notmats:
            seq = scribe.to_seq(file=notmat)
            self.assertTrue(type(seq) == crowsetta.sequence.Sequence)

    def test_notmat_to_csv(self):
        scribe = crowsetta.Transcriber(voc_format='notmat')
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=notmats, csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_example_to_seq_name_import(self):
        sys.path.append(str(self.example_script_dir))
        config = {
            'module': 'example',
            'to_seq': 'example2seq',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(voc_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        seq = scribe.to_seq(mat_file=annotation)
        self.assertTrue(all([type(a_seq) == crowsetta.Sequence for a_seq in seq]))
        sys.path.remove(str(self.example_script_dir))

    def test_only_module_and_to_seq_required(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'to_seq': 'example2seq',
            }
        scribe = crowsetta.Transcriber(voc_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        seq = scribe.to_seq(mat_file=annotation)
        self.assertTrue(all([type(a_seq) == crowsetta.Sequence for a_seq in seq]))

    def test_example_to_seq_path_import(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'to_seq': 'example2seq',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(voc_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        seq = scribe.to_seq(mat_file=annotation)
        self.assertTrue(all([type(a_seq) == crowsetta.Sequence for a_seq in seq]))

    def test_config_wrong_types_raise(self):
        # should raise an error because config should be a dict
        # not list of dicts
        config = list({
                'module': 'example',
                'to_seq': 'example2seq',
                'to_csv': 'example2csv',
                'to_format': 'None',
            }
        )
        with self.assertRaises(TypeError):
            crowsetta.Transcriber(config=config)

    def test_missing_keys_in_config_raises(self):
        config = {
            # missing 'module' key
            'to_seq': 'example2seq',
            'to_csv': None,
            'to_format': None,
        }

        with self.assertRaises(KeyError):
            crowsetta.Transcriber(voc_format='example', config=config)

        config = {
            'module': 'example',
            # missing 'to_seq' key
            'to_csv': None,
            'to_format': None,
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(voc_format='example', config=config)

    def test_extra_keys_in_config_raises(self):
        config = {
            'module': 'example',
            'to_seq': 'example2seq',
            'to_csv': 'example2csv',
            'extra': 'key_right_here',
            'to_format': 'None',
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(voc_format='example', config=config)

    def test_call_to_csv_when_None_raises(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'to_seq': 'example2seq',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(voc_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        with self.assertRaises(NotImplementedError):
            scribe.to_csv(mat_mat_file=annotation, csv_filename='bad.csv')

    def test_call_to_format_when_None_raises(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'to_seq': 'example2seq',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(voc_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        with self.assertRaises(NotImplementedError):
            scribe.to_format(mat_mat_file=annotation, to_format='example')


if __name__ == '__main__':
    unittest.main()
