import pytest


@pytest.fixture
def yarden_annot_mat(test_data_root):
    return test_data_root / 'audio_wav_annot_yarden' / 'llb16_annotation_May_2019_alexa_4TF.mat'
