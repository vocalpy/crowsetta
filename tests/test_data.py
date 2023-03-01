import contextlib

try:
    from importlib.resources import as_file, files, open_text
except ImportError:
    from importlib_resources import as_file, files, open_text

import pathlib
import shutil

import pytest

import crowsetta

DEFAULT_USER_DATA_DIR = pathlib.Path(crowsetta.data.data.APP_DIRS.user_data_dir)


@pytest.fixture
def default_user_data_dir() -> pathlib.Path:
    return DEFAULT_USER_DATA_DIR


def delete_default_user_data_dir() -> None:
    if DEFAULT_USER_DATA_DIR.exists():
        shutil.rmtree(DEFAULT_USER_DATA_DIR)


def all_data_files_exist_in_dst_dir(dst_dir):
    exist = []

    for format_name, path_args in crowsetta.data.data.DATA.items():
        # don't use full name `importlib.resources` here
        # because we need to use backport package, not stdlib, on Python 3.8
        source = files(path_args.package).joinpath(path_args.resource)
        annot_path = as_file(source)
        dst_annot_dir = dst_dir / path_args.package.split(".")[-1]
        dst_annot_path = dst_annot_dir / path_args.resource
        dst_citation_txt_path = dst_annot_dir / "citation.txt"
        exist.append((dst_annot_path.exists() and dst_citation_txt_path.exists()))

    return all(exist)


def test_extract_data_files_default_dir(default_user_data_dir):
    delete_default_user_data_dir()
    crowsetta.data.extract_data_files(user_data_dir=default_user_data_dir)
    assert all_data_files_exist_in_dst_dir(dst_dir=default_user_data_dir)


def test_extract_data_files_user_specified(tmp_path):
    user_specified_data_dir = tmp_path / "crowsetta-data"
    crowsetta.data.extract_data_files(user_data_dir=user_specified_data_dir)
    assert all_data_files_exist_in_dst_dir(dst_dir=user_specified_data_dir)


FORMATS_PARAMETRIZE_ARGNAMES = "format, format_class"
FORMATS_PARAMETRIZE_ARGVALUES = [
    ("aud-seq", crowsetta.formats.seq.AudSeq),
    ("birdsong-recognition-dataset", crowsetta.formats.seq.BirdsongRec),
    ("generic-seq", crowsetta.formats.seq.GenericSeq),
    ("notmat", crowsetta.formats.seq.NotMat),
    ("raven", crowsetta.formats.bbox.Raven),
    ("simple-seq", crowsetta.formats.seq.SimpleSeq),
    ("textgrid", crowsetta.formats.seq.TextGrid),
    ("timit", crowsetta.formats.seq.Timit),
]


@pytest.mark.parametrize(FORMATS_PARAMETRIZE_ARGNAMES, FORMATS_PARAMETRIZE_ARGVALUES)
def test__get_example_as_context_manager(format, format_class):
    """test helper function ``_get_example_as_context_manager``"""
    example = crowsetta.data.data._get_example_as_context_manager(format)

    assert isinstance(example, crowsetta.data.ExampleAnnotFile)
    assert hasattr(example, "annot_path")
    assert isinstance(example.annot_path, contextlib._GeneratorContextManager)
    assert hasattr(example, "citation")
    assert isinstance(example.citation, str)

    if format_class is crowsetta.formats.bbox.Raven:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path, annot_col="Species")
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(
                annot_path,
                columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
                read_csv_kwargs={"index_col": 0},
            )
    else:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path)
    assert isinstance(annot_instance, format_class)


@pytest.mark.parametrize(FORMATS_PARAMETRIZE_ARGNAMES, FORMATS_PARAMETRIZE_ARGVALUES)
def test__get_example_from_user_data_dir(format, format_class, default_user_data_dir):
    delete_default_user_data_dir()
    crowsetta.data.extract_data_files(user_data_dir=default_user_data_dir)

    example = crowsetta.data.data._get_example_from_user_data_dir(format, default_user_data_dir)

    assert isinstance(example, crowsetta.data.ExampleAnnotFile)
    assert hasattr(example, "annot_path")
    assert isinstance(example.annot_path, pathlib.Path)
    assert hasattr(example, "citation")
    assert isinstance(example.citation, str)

    if format_class is crowsetta.formats.bbox.Raven:
        annot_instance = format_class.from_file(example.annot_path, annot_col="Species")
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        annot_instance = format_class.from_file(
            example.annot_path,
            columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
            read_csv_kwargs={"index_col": 0},
        )
    else:
        annot_instance = format_class.from_file(example.annot_path)
    assert isinstance(annot_instance, format_class)


@pytest.mark.parametrize(FORMATS_PARAMETRIZE_ARGNAMES, FORMATS_PARAMETRIZE_ARGVALUES)
def test_get_with_extract(format, format_class, monkeypatch):
    """test that ``crowsetta.data.get`` works
    when we **do** extract annotation files
    to the local file system

    Added as a regression test,
    to make sure #186 stays fixed:
    https://github.com/vocalpy/crowsetta/issues/186
    """
    # set up
    delete_default_user_data_dir()

    # this will cause the call to ``input`` in ``crowsetta.data.get``
    # to return ``Yes``, so that data is extracted
    monkeypatch.setattr("builtins.input", lambda _: "Yes")

    example = crowsetta.data.get(format)

    assert isinstance(example, crowsetta.data.ExampleAnnotFile)
    assert hasattr(example, "annot_path")
    assert isinstance(example.annot_path, pathlib.Path)
    assert hasattr(example, "citation")
    assert isinstance(example.citation, str)

    if format_class is crowsetta.formats.bbox.Raven:
        annot_instance = format_class.from_file(example.annot_path, annot_col="Species")
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        annot_instance = format_class.from_file(
            example.annot_path,
            columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
            read_csv_kwargs={"index_col": 0},
        )
    else:
        annot_instance = format_class.from_file(example.annot_path)
    assert isinstance(annot_instance, format_class)


@pytest.mark.parametrize(FORMATS_PARAMETRIZE_ARGNAMES, FORMATS_PARAMETRIZE_ARGVALUES)
def test_get_with_extracted_already(format, format_class):
    """test that ``crowsetta.data.get`` works
    when annotation files are **already** extracted
    to the local file system"""
    # set up
    delete_default_user_data_dir()
    # this assumes a function we test here will work
    # but I can't think of a better way to test it.
    # re-write the function as a test in this file?
    # Seems redundant and error-prone.
    # So the trade-off is that here if ``extract_data_files`` fails
    # then this unit test will probably fail too.
    crowsetta.data.extract_data_files()  # to default user data dir

    example = crowsetta.data.get(format)

    assert isinstance(example, crowsetta.data.ExampleAnnotFile)
    assert hasattr(example, "annot_path")
    assert isinstance(example.annot_path, pathlib.Path)
    assert hasattr(example, "citation")
    assert isinstance(example.citation, str)

    if format_class is crowsetta.formats.bbox.Raven:
        annot_instance = format_class.from_file(example.annot_path, annot_col="Species")
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        annot_instance = format_class.from_file(
            example.annot_path,
            columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
            read_csv_kwargs={"index_col": 0},
        )
    else:
        annot_instance = format_class.from_file(example.annot_path)
    assert isinstance(annot_instance, format_class)


@pytest.mark.parametrize(FORMATS_PARAMETRIZE_ARGNAMES, FORMATS_PARAMETRIZE_ARGVALUES)
def test_get_with_no_extract(format, format_class, monkeypatch):
    """test that ``crowsetta.data.get`` works
    even if we do not extract annotation files
    from package to local file system
    """
    # set up
    delete_default_user_data_dir()
    # this will cause the call to ``input`` in ``crowsetta.data.get``
    # to return ``No``, so that data is not extracted
    monkeypatch.setattr("builtins.input", lambda _: "No")

    example = crowsetta.data.get(format)

    assert isinstance(example, crowsetta.data.ExampleAnnotFile)
    assert hasattr(example, "annot_path")
    assert isinstance(example.annot_path, contextlib._GeneratorContextManager)
    assert hasattr(example, "citation")
    assert isinstance(example.citation, str)

    if format_class is crowsetta.formats.bbox.Raven:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path, annot_col="Species")
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(
                annot_path,
                columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
                read_csv_kwargs={"index_col": 0},
            )
    else:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path)
    assert isinstance(annot_instance, format_class)


def test_available_formats():
    formats_with_example_data_list = crowsetta.data.available_formats()
    assert isinstance(formats_with_example_data_list, list)
    for format in formats_with_example_data_list:
        assert format in crowsetta.formats.as_list()
