"""test functions in birdsongrec module"""
import numpy as np
import pytest
import soundfile

import crowsetta

from .asserts import assert_rounded_correct_num_decimals


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
