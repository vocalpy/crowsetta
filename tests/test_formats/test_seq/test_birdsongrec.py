"""test functions in birdsongrec module"""
import os

import numpy as np
import pytest
import soundfile

import crowsetta

from .asserts import assert_rounded_correct_num_decimals


class TestBirdsongRecSyllable:
    def test_init(self):
        syl = crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=32000, length=3200, label='0')
        for attr in ['position', 'length', 'label']:
            assert hasattr(syl, attr)

    def test_position_not_int_raises(self):
        with pytest.raises(TypeError):
            # position should be an int
            crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=1.5, length=3200, label='0')

    def test_length_not_int_raises(self):
        with pytest.raises(TypeError):
            # length should be an int
            crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=32500, length=2709.3, label='0')

    def test_label_not_str_raises(self):
        with pytest.raises(TypeError):
            # label should be a str
            crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=32500, length=2709.3, label=0)


@pytest.fixture
def syl_list():
    syl1 = crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=32000, length=3200, label='0')
    syl2 = crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=64000, length=3200, label='0')
    syl3 = crowsetta.formats.seq.birdsongrec.BirdsongRecSyllable(position=96000, length=3200, label='0')
    return [syl1, syl2, syl3]


@pytest.fixture
def birdsongrec_wavfile(birdsong_rec_wav_path):
    return birdsong_rec_wav_path / '0.wav'


class TestBirdsongRecSequence:

    def test_init(self, syl_list, birdsongrec_wavfile):
        seq = crowsetta.formats.seq.birdsongrec.BirdsongRecSequence(
            wav_file=birdsongrec_wavfile, position=16000, length=120000, syl_list=syl_list
        )
        for attr in ['wav_file', 'position', 'length', 'num_syls', 'syls']:
            assert hasattr(seq, attr)

    def test_position_not_int_raises(self, syl_list, birdsongrec_wavfile):
        with pytest.raises(TypeError):
            # position should be an int
            crowsetta.formats.seq.birdsongrec.BirdsongRecSequence(
                wav_file=birdsongrec_wavfile, position=1.5, length=3200, syl_list=syl_list
            )

    def test_length_not_int_raises(self, syl_list, birdsongrec_wavfile):
        with pytest.raises(TypeError):
            # length should be an int
            crowsetta.formats.seq.birdsongrec.BirdsongRecSequence(
                wav_file=birdsongrec_wavfile, position=32500, length=2709.3, syl_list=syl_list
            )


def test_parsexml(birdsong_rec_xml_file):
    seq_list_no_concat = crowsetta.formats.seq.birdsongrec.parse_xml(
        birdsong_rec_xml_file, concat_seqs_into_songs=False, return_wav_abspath=False, wav_abspath=None
    )
    assert all([type(seq) == crowsetta.formats.seq.birdsongrec.BirdsongRecSequence
                for seq in seq_list_no_concat])


def test_parsexml_concat_seq_into_songs(birdsong_rec_xml_file):
    seq_list_no_concat = crowsetta.formats.seq.birdsongrec.parse_xml(
        birdsong_rec_xml_file, concat_seqs_into_songs=False, return_wav_abspath=False, wav_abspath=None
    )
    seq_list_concat = crowsetta.formats.seq.birdsongrec.parse_xml(
        birdsong_rec_xml_file, concat_seqs_into_songs=True, return_wav_abspath=False, wav_abspath=None
    )
    assert all([type(seq) == crowsetta.formats.seq.birdsongrec.BirdsongRecSequence for seq in seq_list_concat])
    assert seq_list_no_concat != seq_list_concat


def test_parsexml_wav_abspath_none(birdsong_rec_xml_file):
    # test return_wav_abspath works with wav_abpsath=None
    seq_list_abspath = crowsetta.formats.seq.birdsongrec.parse_xml(
        birdsong_rec_xml_file, concat_seqs_into_songs=True, return_wav_abspath=True, wav_abspath=None
    )
    for seq in seq_list_abspath:
        assert os.path.isfile(seq.wav_file)


def test_parsexml_wav_abspath(birdsong_rec_xml_file, birdsong_rec_wav_path):
    # test return_wav_abspath works with wav_abpsath specified
    seq_list_abspath = crowsetta.formats.seq.birdsongrec.parse_xml(
        birdsong_rec_xml_file, concat_seqs_into_songs=True, return_wav_abspath=True, wav_abspath=birdsong_rec_wav_path
    )
    for seq in seq_list_abspath:
        assert os.path.isfile(seq.wav_file)


@pytest.mark.parametrize(
    "concat_seqs_into_songs",
    [
        True,
        False,
    ],
)
def test_from_file(birdsong_rec_xml_file, birdsong_rec_wav_path, concat_seqs_into_songs):
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path, concat_seqs_into_songs=concat_seqs_into_songs
    )
    assert isinstance(birdsongrec, crowsetta.formats.seq.BirdsongRec)
    if concat_seqs_into_songs:
        n_wavs = len(sorted(birdsong_rec_wav_path.glob("*.wav")))
        assert len(birdsongrec.sequences) == n_wavs


# we use these for two tests so define them here
ARGNAMES = "concat_seqs_into_songs, samplerate, wav_path"
ARGVALUES = [
    (True, None, None),
    (False, None, None),
    (True, 32000, None),
    (False, 32000, None),
    (True, None, "birdsongrec/Bird0/Wave"),
    (False, None, "birdsongrec/Bird0/Wave"),
    (True, 32000, "birdsongrec/Bird0/Wave"),
    (False, 32000, "birdsongrec/Bird0/Wave"),
    (True, None, "birdsongrec/doesnt/exist"),
    (False, None, "birdsongrec/doesnt/exist"),
]


@pytest.mark.parametrize(ARGNAMES, ARGVALUES)
def test_to_seq(
    test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path, concat_seqs_into_songs, samplerate, wav_path
):
    if wav_path is None:
        wav_path = birdsong_rec_wav_path
    else:
        wav_path = test_data_root / wav_path
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=wav_path, concat_seqs_into_songs=concat_seqs_into_songs
    )
    if not wav_path.exists():
        with pytest.warns(UserWarning):
            seqs = birdsongrec.to_seq(samplerate)
    else:
        seqs = birdsongrec.to_seq(samplerate)

    assert isinstance(seqs, list)
    assert all([isinstance(seq, crowsetta.Sequence) for seq in seqs])
    if concat_seqs_into_songs:
        n_wavs = len(sorted(birdsong_rec_wav_path.glob("*.wav")))
        assert len(seqs) == n_wavs


@pytest.mark.parametrize(
    "decimals",
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
def test_to_seq_round_times_true(test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path, decimals):
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path, concat_seqs_into_songs=True
    )
    seqs = birdsongrec.to_seq(round_times=True, decimals=decimals)
    onsets_s = [onset_s for seq in seqs for onset_s in seq.onsets_s]
    offsets_s = [offset_s for seq in seqs for offset_s in seq.offsets_s]

    assert_rounded_correct_num_decimals(onsets_s, decimals)
    assert_rounded_correct_num_decimals(offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path):
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path, concat_seqs_into_songs=True
    )
    seqs = birdsongrec.to_seq(round_times=False)
    onsets_s_from_to_seq = [onset_s for seq in seqs for onset_s in seq.onsets_s]
    offsets_s_from_to_seq = [offset_s for seq in seqs for offset_s in seq.offsets_s]

    # get directly from annotations so we can compare with what ``to_seq`` returns
    onsets_s_from_birdsongrec = []
    offsets_s_from_birdsongrec = []
    for birdsongrec_seq in birdsongrec.sequences:
        onset_samples = np.array([syl.position for syl in birdsongrec_seq.syls])
        offset_samples = np.array([syl.position + syl.length for syl in birdsongrec_seq.syls])
        wav_filename = birdsongrec.wav_path / birdsongrec_seq.wav_file
        samplerate_this_wav = soundfile.info(wav_filename).samplerate
        onsets_s_from_birdsongrec.extend((onset_samples / samplerate_this_wav).tolist())
        offsets_s_from_birdsongrec.extend((offset_samples / samplerate_this_wav).tolist())

    assert np.all(np.allclose(onsets_s_from_to_seq, onsets_s_from_birdsongrec))
    assert np.all(np.allclose(offsets_s_from_to_seq, offsets_s_from_birdsongrec))


@pytest.mark.parametrize(ARGNAMES, ARGVALUES)
def test_to_annot(
    test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path, concat_seqs_into_songs, samplerate, wav_path
):
    if wav_path is None:
        wav_path = birdsong_rec_wav_path
    else:
        wav_path = test_data_root / wav_path
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=wav_path, concat_seqs_into_songs=concat_seqs_into_songs
    )
    if not wav_path.exists():
        with pytest.warns(UserWarning):
            annots = birdsongrec.to_annot(samplerate)
    else:
        annots = birdsongrec.to_annot(samplerate)

    assert isinstance(annots, list)
    assert all([isinstance(annot, crowsetta.Annotation) for annot in annots])
    if concat_seqs_into_songs:
        n_wavs = len(sorted(birdsong_rec_wav_path.glob("*.wav")))
        assert len(annots) == n_wavs


@pytest.mark.parametrize(
    "decimals",
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
def test_to_annot_round_times_true(test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path, decimals):
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path, concat_seqs_into_songs=True
    )
    annots = birdsongrec.to_annot(round_times=True, decimals=decimals)
    onsets_s = [onset_s for annot in annots for onset_s in annot.seq.onsets_s]
    offsets_s = [offset_s for annot in annots for offset_s in annot.seq.offsets_s]

    assert_rounded_correct_num_decimals(onsets_s, decimals)
    assert_rounded_correct_num_decimals(offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root, birdsong_rec_xml_file, birdsong_rec_wav_path):
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path, concat_seqs_into_songs=True
    )
    annots = birdsongrec.to_annot(round_times=False)
    onsets_s_from_to_annot = [onset_s for annot in annots for onset_s in annot.seq.onsets_s]
    offsets_s_from_to_annot = [offset_s for annot in annots for offset_s in annot.seq.offsets_s]

    # get directly from annotations so we can compare with what ``to_seq`` returns
    onsets_s_from_birdsongrec = []
    offsets_s_from_birdsongrec = []
    for birdsongrec_seq in birdsongrec.sequences:
        onset_samples = np.array([syl.position for syl in birdsongrec_seq.syls])
        offset_samples = np.array([syl.position + syl.length for syl in birdsongrec_seq.syls])
        wav_filename = birdsongrec.wav_path / birdsongrec_seq.wav_file
        samplerate_this_wav = soundfile.info(wav_filename).samplerate
        onsets_s_from_birdsongrec.extend((onset_samples / samplerate_this_wav).tolist())
        offsets_s_from_birdsongrec.extend((offset_samples / samplerate_this_wav).tolist())

    assert np.all(np.allclose(onsets_s_from_to_annot, onsets_s_from_birdsongrec))
    assert np.all(np.allclose(offsets_s_from_to_annot, offsets_s_from_birdsongrec))
