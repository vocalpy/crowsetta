from __future__ import annotations

import contextlib

try:
    from importlib.resources import as_file, files, open_text
except ImportError:
    from importlib_resources import as_file, files, open_text

import pathlib
import shutil
from typing import Union

import appdirs
import attr

from ..__about__ import __version__ as version
from ..typing import PathLike

APP_DIRS = appdirs.AppDirs(appname="crowsetta", appauthor="vocalpy", version=version)


@attr.define
class FormatPathArgs:
    """arguments that should be
    passed into
    ``importlib.resources.path``
    when loading resources
    for each annotation format
    """

    package: str
    resource: str


@attr.define
class ExampleAnnotFile:
    """Class representing
    an example annotation file.
    Returned by ``crowsetta.data.get``.

    Attributes
    ----------
    annot_path : pathlib.Path, contextlib._GeneratorContextManager
        Path to annotation file,
        can be used to load.
        If annotation files are not been extracted to
        the local file system using the function
        ``crowsetta.data.extract_data_files``,
        then ``crowsetta.data.get`` will return
        ``annot_path`` as a context manager
        that will provide a path to a temporary file.
    citation : str
        Citation for dataset
        from which example is taken
    """

    annot_path: Union[PathLike, contextlib._GeneratorContextManager]
    citation: str


DATA = {
    "aud-bbox": FormatPathArgs(package="crowsetta.data.audbbox", resource="spinetail.txt"),
    "aud-seq": FormatPathArgs(
        package="crowsetta.data.audseq", resource="405_marron1_June_14_2016_69640887.audacity.txt"
    ),
    "birdsong-recognition-dataset": FormatPathArgs(package="crowsetta.data.birdsongrec", resource="Annotation.xml"),
    "generic-seq": FormatPathArgs(package="crowsetta.data.generic", resource="example_custom_format.csv"),
    "notmat": FormatPathArgs(package="crowsetta.data.notmat", resource="gy6or6_baseline_230312_0808.138.cbin.not.mat"),
    "raven": FormatPathArgs(package="crowsetta.data.raven", resource="Recording_1_Segment_02.Table.1.selections.txt"),
    "simple-seq": FormatPathArgs(
        package="crowsetta.data.simple", resource="bl26lb16_190412_0721.20144_annotations.csv"
    ),
    "textgrid": FormatPathArgs(package="crowsetta.data.textgrid", resource="AVO-maea-basic.TextGrid"),
    "timit": FormatPathArgs(package="crowsetta.data.timit", resource="sa1.phn"),
}


def extract_data_files(user_data_dir: PathLike | None = None):
    """Extract example annotation files from ``crowsetta.data``
    to a local directory on the file system.

    Parameters
    ----------
    user_data_dir : str, pathlib.Path
        Location where example annotation files should be extracted to.
        If none is given, defaults to the value of
        ``crowsetta.data.data.APP_DIRS.user_data_dir``
    """
    if user_data_dir is None:
        user_data_dir = APP_DIRS.user_data_dir
    user_data_dir = pathlib.Path(user_data_dir)
    user_data_dir.mkdir(parents=True, exist_ok=True)
    for _, path_args in DATA.items():
        # don't use full name `importlib.resources` here
        # because we need to use backport package, not stdlib, on Python 3.8
        source = files(path_args.package).joinpath(path_args.resource)
        annot_path = as_file(source)
        dst_annot_dir = user_data_dir / path_args.package.split(".")[-1]
        dst_annot_dir.mkdir(exist_ok=True)
        dst_annot_path = dst_annot_dir / path_args.resource
        # don't bother copying if we already did this
        if not dst_annot_path.exists():
            with annot_path as annot_path:
                shutil.copy(annot_path, dst_annot_path)
        dst_citation_txt_path = dst_annot_dir / "citation.txt"
        if not dst_citation_txt_path.exists():
            with as_file(files(path_args.package).joinpath("citation.txt")) as citation_txt_path:
                shutil.copy(citation_txt_path, dst_citation_txt_path)


def _get_example_from_user_data_dir(format: str, user_data_dir: PathLike | None = None) -> ExampleAnnotFile:
    """Returns example from ``user_data_dir``.

    Assumes that example data has already been copied to
    ``user_data_dir`` by calling ``_extract_data_files``.
    Helper function used by ``crowsetta.data.get``.

    Parameters
    ----------
    format : str
        Name of annotation format.
        Should be the shorthand string name,
        as listed by ``crowsetta.formats.as_list``.
    user_data_dir : str, pathlib.Path
        Location where example annotation files have been extracted to,
        by calling ``crowsetta.data.extract_data_files``.
        If none is given, defaults to the value of
        ``crowsetta.data.data.APP_DIRS.user_data_dir``

    Returns
    -------
    example : ExampleAnnotFile
        with ``annot_path`` and ``citation`` attributes.
    """
    try:
        path_args = DATA[format]
    except KeyError as e:
        raise ValueError(f"format not recognized: {format}") from e

    if user_data_dir is None:
        user_data_dir = APP_DIRS.user_data_dir

    format_pkg = path_args.package.split(".")[-1]
    annot_path = user_data_dir / format_pkg / path_args.resource
    citation_txt = user_data_dir / format_pkg / "citation.txt"
    with citation_txt.open("r") as fp:
        citation = fp.read().replace("\n", "")

    return ExampleAnnotFile(annot_path=annot_path, citation=citation)


def _get_example_as_context_manager(format: str) -> ExampleAnnotFile:
    """Gets an example annotation file
    as a context manager, that can be used
    as shown in the example below.

    Helper function used by ``crowsetta.data.get``.

    Parameters
    ----------
    format : str
        Name of annotation format.
        Should be the shorthand string name,
        as listed by ``crowsetta.formats.as_list``.

    Returns
    -------
    example_annot_file : crowsetta.data.ExampleAnnotFile
        class instance with attributes ``annot_path``
        and ``citation``. The ``annot_path``
        attribute should be used as part of a ``with``
        statement to open the file; see Examples below
        or examples in the docstrings.
    """
    try:
        path_args = DATA[format]
    except KeyError as e:
        raise ValueError(f"format not recognized: {format}") from e

    # don't use full name `importlib.resources` here
    # because we need to use backport package, not stdlib, on Python 3.8
    source = files(path_args.package).joinpath(path_args.resource)
    annot_path = as_file(source)

    with open_text(package=path_args.package, resource="citation.txt") as fp:
        citation = fp.read().replace("\n", "")

    return ExampleAnnotFile(annot_path=annot_path, citation=citation)


def get(format: str, user_data_dir: PathLike | None = None) -> ExampleAnnotFile:
    """Get an example annotation files.

    Parameters
    ----------
    format : str
        Name of annotation format.
        Should be the shorthand string name,
        as listed by ``crowsetta.formats.as_list``.
    user_data_dir : str, pathlib.Path
        Location where example annotation files
        are stored.
        If none is given, defaults to the value of
        ``crowsetta.data.data.APP_DIRS.user_data_dir``
        This default can be changed, but will require
        passing the same path in every time
        this function is called to avoid
        being prompted about extracting the example files
        to the default location.

    Returns
    -------
    example_annot_file : ExampleAnnotFile
        class instance with attributes ``annot_path``
        and ``citation``.
        If the annotation files have been
        extracted to the local file system,
        then ``annot_path`` will be a path
        to a file.
        Otherwise, ``annot_path`` will be
        a context manager that should be
        used as part of a ``with``
        statement to open the file; see Examples below
        or examples in the docstrings.

    Examples
    --------
    >>> # example of a context manager
    >>> example = crowsetta.data.get('textgrid')
    >>> with example.annot_path as annot_path:
    ...     textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path)
    """
    if format not in DATA:
        raise ValueError(f"format not recognized: {format}")

    if user_data_dir is None:
        user_data_dir = APP_DIRS.user_data_dir

    user_data_dir = pathlib.Path(user_data_dir)
    if not user_data_dir.exists():
        y_or_n = input(
            f"``user_data_dir`` does not exist at default location:\n{user_data_dir}\n"
            "(To choose a location besides the default, call this function with that location "
            "as the argument for ``user_data_dir``.)\n\n"
            "Do you want to create this ``user_data_dir`` and extract example annotation files into it?\n"
            "[yes]/no >>>"
        )
        if y_or_n.lower().startswith("y") or y_or_n == "":
            extract_data_files(user_data_dir)
            return _get_example_from_user_data_dir(format, user_data_dir)
        else:
            print(
                """Not extracting data. Will return a context manager.\n
                Use the context manager to get a path to a temporary path
                like in the following example:\n

                >>> example = crowsetta.data.get('timit')
                >>> with example.annot_path as annot_path:
                ...     timit = crowsetta.formats.seq.Timit.from_file(annot_path=annot_path)
                >>> annot = timit.to_annot()
            """
            )
            return _get_example_as_context_manager(format)
    else:
        return _get_example_from_user_data_dir(format, user_data_dir)


def available_formats() -> list:
    """Return list of string names
    of annotation formats
    that have built-in sample data
    available.

    Any of the names in the returned list
    can be passed into ``crowsetta.data.get``
    to get a path to an annotation file
    in that format.

    Returns
    -------
    data_list : list
        List of names of formats
        that have built-in sample data available.

    Examples
    --------
    >>> crowsetta.data.available_formats()
    ['aud-bbox', 'aud-seq', 'birdsong-recognition-dataset', 'generic-seq', 'notmat', 'raven', 'simple-seq', 'textgrid', 'timit']  # noqa
    """
    return list(DATA.keys())
