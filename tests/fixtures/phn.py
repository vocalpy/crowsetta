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
def audio_wav_nist_annot_phn_root(test_data_root):
    return test_data_root / 'audio_wav_nist_annot_phn'


@pytest.fixture
def wav_nist_phns(audio_wav_nist_annot_phn_root):
    return sorted(audio_wav_nist_annot_phn_root.glob('*.PHN'))


@pytest.fixture
def a_wav_nist_phn(wav_nist_phns):
    return wav_nist_phns[0]
