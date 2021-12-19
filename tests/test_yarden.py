"""test functions in yarden module"""
import crowsetta


def test_yarden2annot(yarden_annot_mat):
    annots = crowsetta.yarden.yarden2annot(annot_path=yarden_annot_mat)
    assert isinstance(annots, list)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])
