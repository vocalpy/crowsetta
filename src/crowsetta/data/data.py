try:
    from importlib.resources import as_file, files, open_text 
except ImportError:
    from importlib_resources import as_file, files, open_text 

import pathlib

import attr


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
    """class representing
    an example annotation file

    Attributes
    ----------
    annot_path : pathlib.Path
        to annotation file,
        can be used to load
    about : str
        brief description of dataset
        from which example is taken
    doi : str
        DOI for dataset
        from which example is taken
    citation : str
        citation for dataset
        from which example is taken
    """
    annot_path: str
    citation: str


DATA = {
    'aud-txt': FormatPathArgs(package='crowsetta.data.audtxt',
                              resource='405_marron1_June_14_2016_69640887.audacity.txt'),
    'birdsong-recognition-dataset': FormatPathArgs(package='crowsetta.data.birdsongrec',
                                                   resource='Annotation.xml'),
    'generic-seq': FormatPathArgs(package='crowsetta.data.generic',
                                  resource='example_custom_format.csv'),
    'notmat': FormatPathArgs(package='crowsetta.data.notmat',
                             resource='gy6or6_baseline_230312_0808.138.cbin.not.mat'),
    'raven': FormatPathArgs(package='crowsetta.data.raven',
                            resource='Recording_1_Segment_02.Table.1.selections.txt'),
    'simple-seq': FormatPathArgs(package='crowsetta.data.simple',
                                 resource='bl26lb16_190412_0721.20144_annotations.csv'),
    'textgrid': FormatPathArgs(package='crowsetta.data.textgrid',
                               resource='1179.TextGrid'),
    'timit': FormatPathArgs(package='crowsetta.data.timit',
                            resource='sa1.phn'),
}


def get(format: str) -> pathlib.Path:
    """get example annotation files

    Parameters
    ----------
    format : str
        name of annotation format.
        Should be the shorthand string name,
        as listed by ``crowsetta.formats.as_list``.

    Returns
    -------
    example_annot_file : ExampleAnnotFile
        class instance with attributes ``annot_path`` 
        and ``citation``. The ``annot_path`` 
        attribute should be used as part of a ``with`` 
        statement to open the file; see Examples below
        or examples in the docstrings.

    Examples
    --------
    >>> example = crowsetta.data.get('textgrid')
    >>> with example.annot_path as annot_path:
    ...     textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path)
    """
    try:
        path_args = DATA[format]
    except KeyError as e:
        raise ValueError(
            f'format not recognized: {format}'
        ) from e

    # don't use full name `importlib.resources` here
    # because we need to use backport package, not stdlib, on Python 3.8
    source = files(path_args.package).joinpath(path_args.resource)
    annot_path = as_file(source)

    with open_text(
        package=path_args.package,
        resource='citation.txt'
    ) as fp:
        citation = fp.read().replace("\n", "")

    return ExampleAnnotFile(annot_path=annot_path,
                            citation=citation)


def available_formats() -> list:
    """return list of string names
    of annotation formats.
    Any of the names can be passed into
    ``crowsetta.data.get`` to get a path
    to an annotation file
    in that format.

    Returns
    -------
    data_list : list
        of the names of formats
        that have built-in sample data available.
    """
    return list(
        DATA.keys()
    )
