import importlib.util

import pytest

import crowsetta

BUILTIN_FORMATS = (
    crowsetta.formats.seq.BirdsongRec,
    crowsetta.formats.seq.GenericSeq,
    crowsetta.formats.seq.NotMat,
    crowsetta.formats.bbox.Raven,
    crowsetta.formats.seq.SimpleSeq,
    crowsetta.formats.seq.TextGrid,
    crowsetta.formats.seq.Timit,
    crowsetta.formats.seq.SongAnnotationGUI,
)

BUILTIN_FORMAT_NAMES = (format_class.name for format_class in BUILTIN_FORMATS)


def test_as_list():
    formats_list = crowsetta.formats.as_list()
    assert isinstance(formats_list, list)
    assert formats_list == sorted(crowsetta.formats.FORMATS.keys())
    assert all([isinstance(format_name, str) for format_name in formats_list])
    for builtin_format_name in BUILTIN_FORMAT_NAMES:
        assert builtin_format_name in formats_list


@pytest.mark.parametrize("format_class, format_name", list(zip(BUILTIN_FORMATS, BUILTIN_FORMAT_NAMES)))
def test_by_name(format_class, format_name):
    returned_class = crowsetta.formats.by_name(format_name)
    assert returned_class is format_class


def test_register_format(test_data_root):
    example_custom_format_dir = test_data_root / "example_custom_format"
    example_module = example_custom_format_dir / "example.py"
    # line below imports example, which uses `register_format` as decorator on Custom class
    spec = importlib.util.spec_from_file_location("example", example_module)
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    assert "example-custom-format" in crowsetta.formats.as_list()

    annot_path = example_custom_format_dir / "bird1_annotation.mat"
    Custom = crowsetta.formats.by_name("example-custom-format")
    custom = Custom.from_file(annot_path)
    assert isinstance(custom, example.Custom)
