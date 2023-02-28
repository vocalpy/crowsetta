import importlib

import pytest

import crowsetta


def test_audtxt_from_file(an_audseq_path):
    scribe = crowsetta.Transcriber(format="aud-seq")
    audtxt = scribe.from_file(annot_path=an_audseq_path)
    assert isinstance(audtxt, crowsetta.formats.seq.AudSeq)
    annot = audtxt.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


def test_birdsongrec_from_file(birdsong_rec_xml_file, birdsong_rec_wav_path):
    scribe = crowsetta.Transcriber(format="birdsong-recognition-dataset")
    birdsongrec = scribe.from_file(annot_path=birdsong_rec_xml_file, wav_path=birdsong_rec_wav_path)
    assert isinstance(birdsongrec, crowsetta.formats.seq.BirdsongRec)
    annots = birdsongrec.to_annot()
    assert isinstance(annots, list)
    assert all([isinstance(annot, crowsetta.Annotation) for annot in annots])


def test_generic_seq_from_file(birdsongrec_as_generic_seq_csv):
    scribe = crowsetta.Transcriber(format="generic-seq")
    generic = scribe.from_file(birdsongrec_as_generic_seq_csv)
    assert isinstance(generic, crowsetta.formats.seq.GenericSeq)
    annots = generic.to_annot()
    assert isinstance(annots, list)
    assert all([isinstance(annot, crowsetta.Annotation) for annot in annots])


def test_notmat_from_file(a_notmat_path):
    scribe = crowsetta.Transcriber(format="notmat")
    notmat = scribe.from_file(annot_path=a_notmat_path)
    assert isinstance(notmat, crowsetta.formats.seq.NotMat)
    annot = notmat.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


def test_simple_seq_from_file(a_simple_csv_path):
    scribe = crowsetta.Transcriber(format="simple-seq")
    simple = scribe.from_file(a_simple_csv_path)
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)
    annot = simple.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


def test_yarden_from_file(yarden_annot_mat):
    scribe = crowsetta.Transcriber(format="yarden")
    yarden = scribe.from_file(annot_path=yarden_annot_mat)
    assert isinstance(yarden, crowsetta.formats.seq.SongAnnotationGUI)
    annots = yarden.to_annot()
    assert isinstance(annots, list)
    assert all([isinstance(annot, crowsetta.Annotation) for annot in annots])


def test_example_custom_format(test_data_root):
    example_custom_format_dir = test_data_root / "example_custom_format"
    example_module = example_custom_format_dir / "example.py"
    # line below imports example, which uses `register_format` as decorator on Custom class
    spec = importlib.util.spec_from_file_location("example", example_module)
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)

    annot_path = example_custom_format_dir / "bird1_annotation.mat"
    scribe = crowsetta.Transcriber(format="example-custom-format")
    example_ = scribe.from_file(annot_path)
    assert isinstance(example_, example.Custom)


@pytest.mark.parametrize(
    "format",
    ["birdsong-recognition-dataset", "generic-seq", "notmat", "raven", "simple-seq", "textgrid", "timit", "yarden"],
)
def test_repr(format):
    scribe = crowsetta.Transcriber(format=format)
    repr_ = repr(scribe)
    assert repr_ == f"crowsetta.Transcriber(format='{format}')"
