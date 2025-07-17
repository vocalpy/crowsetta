import pathlib

import pytest

import crowsetta


@pytest.mark.parametrize(
    "annot_path, notated_path, seq_or_bbox",
    [
        ("./an/bird1-22.csv", None, "seq"),
        ("./an/bird1-22.csv", "./an/bird1-22.wav", "seq"),
        ("./an/bird1-22.csv", None, "bbox"),
        ("./an/bird1-22.csv", "./an/bird1-22.wav", "bbox"),
    ],
)
def test_init_seq(annot_path, notated_path, seq_or_bbox, a_seq, a_bboxes_list):
    """smoke test, make sure we can instantiate"""
    if seq_or_bbox == "seq":
        annot = crowsetta.Annotation(annot_path=annot_path, notated_path=notated_path, seq=a_seq)
    elif seq_or_bbox == "bbox":
        annot = crowsetta.Annotation(
            annot_path=annot_path,
            notated_path=notated_path,
            bboxes=a_bboxes_list,
        )

    assert isinstance(annot, crowsetta.Annotation)
    assert annot.annot_path == pathlib.Path(annot_path)
    if notated_path:
        assert annot.notated_path == pathlib.Path(notated_path)
    else:
        assert annot.notated_path is None
    if seq_or_bbox == "seq":
        assert hasattr(annot, "seq")
        assert annot.seq == a_seq
    elif seq_or_bbox == "bbox":
        assert hasattr(annot, "bboxes")
        assert annot.bboxes == a_bboxes_list


def test_no_seq_or_bboxes_raises():
    with pytest.raises(ValueError):
        crowsetta.Annotation(
            annot_path="./an/annnot.csv",
            notated_path=None,
        )


def test_seq_and_bboxes_raises(a_seq, a_bboxes_list):
    with pytest.raises(ValueError):
        crowsetta.Annotation(
            annot_path="./an/annnot.csv",
            notated_path=None,
            seq=a_seq,
            bboxes=a_bboxes_list,
        )


def seq_not_Sequence_raises():
    with pytest.raises(ValueError):
        crowsetta.Annotation(annot_path="./an/annnot.csv", notated_path=None, seq=5)


def bbox_not_list_raises():
    with pytest.raises(ValueError):
        crowsetta.Annotation(annot_path="./an/annnot.csv", notated_path=None, bboxes=5)


def bbox_not_list_of_bboxes_raises():
    with pytest.raises(ValueError):
        crowsetta.Annotation(annot_path="./an/annnot.csv", notated_path=None, bboxes=[_ for _ in range(10)])


def test_seq_with_no_segments():
    """Test that an :class:`crowsetta.Annotation`
    instantiated with a :class:`crowsetta.Sequence` 
    that has no segments / a length of zero 
    has a `seq` attribute that points to that Sequence.
    """
    # see https://github.com/vocalpy/crowsetta/issues/290
    seq = crowsetta.Sequence.from_keyword(labels=[], onsets_s=[], offsets_s=[])
    annot = crowsetta.Annotation(seq=seq, annot_path="./path.csv")
    assert hasattr(annot, "seq")
    assert annot.seq == seq
