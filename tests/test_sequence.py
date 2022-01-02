import numpy as np
import pytest

from crowsetta.sequence import Sequence

from .helpers import keywords


def test_init(list_of_segments):
    (onset_inds,
     offset_inds,
     onsets_s,
     offsets_s,
     labels) = keywords.from_segments(list_of_segments)

    seq = Sequence(segments=list_of_segments,
                   onset_inds=onset_inds,
                   offset_inds=offset_inds,
                   onsets_s=onsets_s,
                   offsets_s=offsets_s,
                   labels=labels,
                   )

    assert type(seq) == Sequence
    assert hasattr(seq, 'segments')


def test_init_with_wrong_type_for_segments_raises(list_of_segments):
    dict_of_segments = dict(zip(range(len(list_of_segments)),
                                list_of_segments))
    with pytest.raises(TypeError):
        Sequence(segments=dict_of_segments)


def test_init_with_bad_type_in_segments_raises(list_of_segments):
    segment_dict = {
        'label': 'a',
        'onset_ind': 16000,
        'offset_ind': 32000,
    }
    list_of_segments.append(segment_dict)
    with pytest.raises(TypeError):
        Sequence(segments=list_of_segments)


def test_from_segments(list_of_segments):
    seq = Sequence.from_segments(list_of_segments)
    assert hasattr(seq, 'segments')
    assert type(seq.segments) == tuple


def test_from_keyword_bad_labels_type_raises():
    labels = 12345
    onset_inds = np.asarray([0, 2, 4, 6, 8])
    offset_inds = np.asarray([1, 3, 5, 7, 9])
    with pytest.raises(TypeError):
        Sequence.from_keyword(labels=labels, onset_inds=onset_inds,
                              offset_inds=offset_inds)


def test_from_keyword__onset_offset_in_seconds():
    labels = 'abcde'
    onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8])
    offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9])
    seq = Sequence.from_keyword(labels=labels,
                                onsets_s=onsets_s,
                                offsets_s=offsets_s)
    assert hasattr(seq, 'segments')
    assert type(seq.segments) == tuple


def test_from_keyword_onset_offset_in_Hertz():
    labels = 'abcde'
    onset_inds = np.asarray([0, 2, 4, 6, 8])
    offset_inds = np.asarray([1, 3, 5, 7, 9])
    seq = Sequence.from_keyword(labels=labels,
                                onset_inds=onset_inds,
                                offset_inds=offset_inds)
    assert hasattr(seq, 'segments')
    assert type(seq.segments) == tuple


def test_from_dict_onset_offset_in_seconds():
    seq_dict = {
        'labels': 'abcde',
        'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
    }
    seq = Sequence.from_dict(seq_dict=seq_dict)
    assert hasattr(seq, 'segments')
    assert type(seq.segments) == tuple


def test_from_dict_onset_offset_in_Hertz():
    seq_dict = {
        'labels': 'abcde',
        'onset_inds':  np.asarray([0, 2, 4, 6, 8]),
        'offset_inds': np.asarray([1, 3, 5, 7, 9]),
    }
    seq = Sequence.from_dict(seq_dict=seq_dict)
    assert hasattr(seq, 'segments')
    assert type(seq.segments) == tuple


def test_from_keyword_missing_onsets_and_offsets_raises():
    with pytest.raises(ValueError):
        Sequence.from_keyword(labels='abcde')


def test_missing_offset_seconds_raises():
    with pytest.raises(ValueError):
        Sequence.from_keyword(labels='abcde',
                              onsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]))


def test_missing_onset_seconds_raises():
    with pytest.raises(ValueError):
        Sequence.from_keyword(labels='abcde',
                              offsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]))


def test_missing_offset_Hertz_raises():
    with pytest.raises(ValueError):
        Sequence.from_keyword(labels='abcde',
                              onset_inds=np.asarray([0, 2, 4, 6, 8]))


def test_missing_onset_Hertz_raises():
    with pytest.raises(ValueError):
        Sequence.from_keyword(labels='abcde',
                              offset_inds=np.asarray([0, 2, 4, 6, 8]))


def test_as_dict_onset_offset_in_Hertz():
    labels = 'abcde'
    onset_inds = np.asarray([0, 2, 4, 6, 8])
    offset_inds = np.asarray([1, 3, 5, 7, 9])
    seq = Sequence.from_keyword(labels=labels,
                                onset_inds=onset_inds,
                                offset_inds=offset_inds)
    seq_dict = seq.as_dict()

    assert np.all(seq_dict['labels'] == np.asarray(list(labels)))
    assert np.all(seq_dict['onset_inds'] == onset_inds)
    assert np.all(seq_dict['offset_inds'] == offset_inds)
    assert seq_dict['onsets_s'] is None
    assert seq_dict['offsets_s'] is None


def test_as_dict_onset_offset_in_seconds():
    labels = 'abcde'
    onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
    offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
    seq = Sequence.from_keyword(labels=labels,
                                onsets_s=onsets_s,
                                offsets_s=offsets_s)
    seq_dict = seq.as_dict()

    assert np.all(seq_dict['labels'] == np.asarray(list(labels)))
    assert np.all(seq_dict['onsets_s'] == onsets_s)
    assert np.all(seq_dict['offsets_s'] == offsets_s)
    assert seq_dict['onset_inds'] is None
    assert seq_dict['offset_inds'] is None


def test_to_dict_onset_offset_both_units():
    labels = 'abcde'
    onset_inds = np.asarray([0, 2, 4, 6, 8])
    offset_inds = np.asarray([1, 3, 5, 7, 9])
    onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
    offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
    seq = Sequence.from_keyword(labels=labels,
                                onset_inds=onset_inds,
                                offset_inds=offset_inds,
                                onsets_s=onsets_s,
                                offsets_s=offsets_s)
    seq_dict = seq.as_dict()

    assert np.all(seq_dict['labels'] == np.asarray(list(labels)))
    assert np.all(seq_dict['onsets_s'] == onsets_s)
    assert np.all(seq_dict['offsets_s'] == offsets_s)
    assert np.all(seq_dict['onset_inds'] == onset_inds)
    assert np.all(seq_dict['offset_inds'] == offset_inds)


def test_eq(a_seq, same_seq):
    assert a_seq == same_seq


def test_ne(a_seq, different_seq):
    assert a_seq != different_seq


def test_lt_raises(a_seq, different_seq):
    with pytest.raises(NotImplementedError):
        a_seq < different_seq


def test_le_raises(a_seq, different_seq):
    with pytest.raises(NotImplementedError):
        a_seq <= different_seq


def test_gt_raises(a_seq, different_seq):
    with pytest.raises(NotImplementedError):
        a_seq > different_seq


def test_ge_raises(a_seq, different_seq):
    with pytest.raises(NotImplementedError):
        a_seq >= different_seq


def test_hash():
    seq_dict1 = {
        'labels': 'abcde',
        'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
    }
    seq1 = Sequence.from_dict(seq_dict=seq_dict1)

    # same as seq1, so Sequence should have same hash
    seq_dict2 = {
        'labels': 'abcde',
        'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
    }
    seq2 = Sequence.from_dict(seq_dict=seq_dict2)

    # different from seq1, so Sequence should have different hash
    seq_dict3 = {'labels': 'fghijk',
                 'onsets_s': np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
                 'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
                 }
    seq3 = Sequence.from_dict(seq_dict=seq_dict3)

    hash1 = hash(seq1)
    hash2 = hash(seq2)
    hash3 = hash(seq3)

    assert hash1 == hash2
    assert hash1 != hash3


def test_seq_is_immutable(a_seq):
    with pytest.raises(TypeError):
        a_seq.labels = np.asarray(['a', 'b', 'c', 'd', 'd'])
