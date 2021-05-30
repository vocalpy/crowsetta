import pytest


@pytest.fixture
def audio_wav_annot_phn_root(test_data_root):
    return test_data_root / 'audio_wav_annot_phn'


@pytest.fixture
def phns(audio_wav_annot_phn_root):
    return sorted(audio_wav_annot_phn_root.glob('*.phn'))


@pytest.fixture
def a_phn(phns):
    return phns[0]


@pytest.fixture
def audio_WAV_annot_PHN_root(test_data_root):
    return test_data_root / 'audio_WAV_annot_PHN'


@pytest.fixture
def PHNs(audio_WAV_annot_PHN_root):
    return sorted(audio_WAV_annot_PHN_root.glob('*.PHN'))


@pytest.fixture
def a_PHN(PHNs):
    return PHNs[0]
