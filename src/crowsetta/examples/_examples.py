"""Functions that provide example data"""

import importlib.resources
import json
import pathlib

from attr import define


@define
class Example:
    """Dataclass that represents an example annotation file.

    Attributes
    ----------
    filename : str
        Name of annotation file.
    description_filename: str
        Name of text file that contains description of
        annotation file, including any relevant citations.
    format: str
        Annotation file format.
    name: str, optional
        A human-readable name for the annotation file.
        Can be specified if the filename is not convenient to type.
        If None, defaults to filename.
    from_file_kwargs : dict, optional
        Keyword arguments to pass into
        :meth:`crowsetta.Transcriber.from_file`
        when loading the annotation file.
        Optional, default is None.

    Notes
    -----
    This dataclass is used to load metadata from
    `vocalpy/examples/example-metadata.json`.
    """

    filename: str
    path: pathlib.Path
    description: str
    format: str
    name: str | None = None
    from_file_kwargs: dict | None = None

    @classmethod
    def from_metadata(
        cls, filename, description_filename, format: str, name: str | None = None, from_file_kwargs: dict | None = None
    ):
        """Create a :class:`Example` instance from metadata.

        Parameters
        ----------
        filename : str
            Name of annotation file.
        description_filename: str
            Name of text file that contains description of
            annotation file, including any relevant citations.
        format: str
            Annotation file format.
        name: str, optional
            A human-readable name for the annotation file.
            Can be specified if the filename is not convenient to type.
            If None, defaults to filename.
        from_file_kwargs : dict, optional
            Keyword arguments to pass into
            :meth:`crowsetta.Transcriber.from_file`
            when loading the annotation file.
            Optional, default is None.

        Returns
        -------
        example : Example
            Instance of :class:`Example` dataclass
        """
        path = importlib.resources.files("crowsetta.examples").joinpath(filename)

        description_path = importlib.resources.files("crowsetta.examples").joinpath(description_filename)
        description = description_path.read_text()

        if name is None:
            name = filename

        if from_file_kwargs is None:
            from_file_kwargs = {}

        return cls(filename, path, description, format, name, from_file_kwargs)

    def load(self):
        import crowsetta

        scribe = crowsetta.Transcriber(format=self.format)
        return scribe.from_file(self.path, **self.from_file_kwargs)


EXAMPLE_METADATA_JSON_PATH = pathlib.Path(
    importlib.resources.files("crowsetta.examples").joinpath("example-metadata.json")
)
with EXAMPLE_METADATA_JSON_PATH.open("r") as fp:
    ALL_EXAMPLE_METADATA = json.load(fp)

EXAMPLES = [Example.from_metadata(**example_metadata) for example_metadata in ALL_EXAMPLE_METADATA]

REGISTRY = {example_.name: example_ for example_ in EXAMPLES}


def example(name: str, return_path: bool = False):
    """Get an example annotation file.

    Parameter
    ---------
    name : str
        Human-readable name that refers to annotation file.
        For a list pf names, call :func:`crowsetta.examples.show`.
    return_path : bool
        If ``True``, return the path to the annotation file.
        Default is ``False``.
        When ``False``, an instance of the class that represents
        a set of annotations in the format used by the example
        is returned.

    Examples
    --------

    >>> marron1 = crowsetta.example("marron1")
    >>> print(marron1)
    AudSeq(start_times=array([ 0.        ,  0.76981817,  1.13127401,  2.21840074,  2.55502374,
            3.09030949,  3.69457537,  3.81322118,  4.05603121,  4.86171904,
            4.87551507,  5.52392822,  6.55587085,  6.59449972,  7.0883974 ,
            7.18772877,  7.23463526,  7.94375092,  9.01984083,  9.06950652,
            9.18263392, 10.06282028, 10.07661631, 10.9705987 , 10.98715393,
        11.80663778, 11.86458109, 12.19016727, 13.24142433, 13.277294  ,
        14.49686257, 14.60723076, 15.22805186, 15.31082801, 16.22136563,
        17.25606747, 18.16660509, 18.20247475, 19.65381653, 19.75590711,
        20.71059201, 20.78509054, 20.96719806, 21.02514137, 21.35624596,
        21.45005892, 21.66527691, 21.67355452, 22.73860761, 22.82966137,
        23.63534921, 24.59831172, 24.60383013, 24.67281025, 24.77214163,
        25.68267925, 25.70751209, 26.65943778, 27.7410461 , 27.76036054,
        28.34531198]), end_times=array([ 0.76981817,  1.13127401,  2.21840074,  2.55502374,  3.09030949,
            3.69457537,  3.81322118,  4.05603121,  4.86171904,  4.87551507,
            5.53496504,  6.55587085,  6.59449972,  7.0883974 ,  7.18772877,
            7.23463526,  7.94375092,  9.01984083,  9.06950652,  9.18263392,
        10.06282028, 10.07661631, 10.9705987 , 10.98715393, 11.80663778,
        11.86458109, 12.20396329, 13.24142433, 13.277294  , 14.49686257,
        14.60723076, 15.22805186, 15.31082801, 16.22136563, 17.25606747,
        18.16660509, 18.20247475, 19.65381653, 19.75590711, 20.71059201,
        20.78509054, 20.96719806, 21.02514137, 21.35624596, 21.45005892,
        21.66527691, 21.67355452, 22.73860761, 22.82966137, 23.63534921,
        24.59831172, 24.60383013, 24.67281025, 24.77214163, 25.68267925,
        25.70751209, 26.65943778, 27.7410461 , 27.76036054, 28.359108  ,
        29.10133412]), labels=<StringArray>
    [ 'SIL', 'call',  'SIL', 'call',  'SIL',    'Z',  'SIL',   'Ci',    'C',
    'SIL',    'H',    'E',  'SIL',    'R',  'SIL',   'J1',   'J1',   'J2',
    'J2',  'SIL',   'B1',  'SIL',   'B2',  'SIL',    'Q',  'SIL',    'H',
        'E',  'SIL',    'R',  'SIL',    'O',  'SIL',   'J1',   'J2',    'L',
    'SIL',    'N',  'SIL',    'A',  'SIL',    'O',  'SIL',    'P',  'SIL',
        'K',  'SIL',    'V',  'SIL',   'J1',   'J2',  'SIL',   'J2',  'SIL',
    'B1',  'SIL',   'B2',    'Q',  'SIL',    'H',    'E']
    Length: 61, dtype: string, annot_path=PosixPath('/Users/davidnicholson/Documents/repos/vocalpy/crowsetta/src/crowsetta/examples/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None)  # noqa: E501

    You can specify ``return_path=True`` to get a ``pathlib.Path``
    instance that points to the file.
    This can be used with the ``from_file`` method of the
    format classes.

    >>> patg = crowsetta.example("marron1", return_path=True)
    >>> marron1 = crowsetta.AudSeq.from_file(path)
    >>> print(marron1)
    AudSeq(start_times=array([ 0.        ,  0.76981817,  1.13127401,  2.21840074,  2.55502374,
            3.09030949,  3.69457537,  3.81322118,  4.05603121,  4.86171904,
            4.87551507,  5.52392822,  6.55587085,  6.59449972,  7.0883974 ,
            7.18772877,  7.23463526,  7.94375092,  9.01984083,  9.06950652,
            9.18263392, 10.06282028, 10.07661631, 10.9705987 , 10.98715393,
        11.80663778, 11.86458109, 12.19016727, 13.24142433, 13.277294  ,
        14.49686257, 14.60723076, 15.22805186, 15.31082801, 16.22136563,
        17.25606747, 18.16660509, 18.20247475, 19.65381653, 19.75590711,
        20.71059201, 20.78509054, 20.96719806, 21.02514137, 21.35624596,
        21.45005892, 21.66527691, 21.67355452, 22.73860761, 22.82966137,
        23.63534921, 24.59831172, 24.60383013, 24.67281025, 24.77214163,
        25.68267925, 25.70751209, 26.65943778, 27.7410461 , 27.76036054,
        28.34531198]), end_times=array([ 0.76981817,  1.13127401,  2.21840074,  2.55502374,  3.09030949,
            3.69457537,  3.81322118,  4.05603121,  4.86171904,  4.87551507,
            5.53496504,  6.55587085,  6.59449972,  7.0883974 ,  7.18772877,
            7.23463526,  7.94375092,  9.01984083,  9.06950652,  9.18263392,
        10.06282028, 10.07661631, 10.9705987 , 10.98715393, 11.80663778,
        11.86458109, 12.20396329, 13.24142433, 13.277294  , 14.49686257,
        14.60723076, 15.22805186, 15.31082801, 16.22136563, 17.25606747,
        18.16660509, 18.20247475, 19.65381653, 19.75590711, 20.71059201,
        20.78509054, 20.96719806, 21.02514137, 21.35624596, 21.45005892,
        21.66527691, 21.67355452, 22.73860761, 22.82966137, 23.63534921,
        24.59831172, 24.60383013, 24.67281025, 24.77214163, 25.68267925,
        25.70751209, 26.65943778, 27.7410461 , 27.76036054, 28.359108  ,
        29.10133412]), labels=<StringArray>
    [ 'SIL', 'call',  'SIL', 'call',  'SIL',    'Z',  'SIL',   'Ci',    'C',
    'SIL',    'H',    'E',  'SIL',    'R',  'SIL',   'J1',   'J1',   'J2',
    'J2',  'SIL',   'B1',  'SIL',   'B2',  'SIL',    'Q',  'SIL',    'H',
        'E',  'SIL',    'R',  'SIL',    'O',  'SIL',   'J1',   'J2',    'L',
    'SIL',    'N',  'SIL',    'A',  'SIL',    'O',  'SIL',    'P',  'SIL',
        'K',  'SIL',    'V',  'SIL',   'J1',   'J2',  'SIL',   'J2',  'SIL',
    'B1',  'SIL',   'B2',    'Q',  'SIL',    'H',    'E']
    Length: 61, dtype: string, annot_path=PosixPath('/Users/davidnicholson/Documents/repos/vocalpy/crowsetta/src/crowsetta/examples/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None)  # noqa: E501
    """
    try:
        example_ = REGISTRY[name]
    except KeyError as e:
        raise ValueError(
            f"The `name` is not recongized as an example annotation file: {name}.\n"
            "Please call `crowsetta.examples.show()` to see the list of example annotation files."
        ) from e

    if return_path:
        return example_.path
    else:
        return example_.load()


def show():
    """Print the names and descriptions of all
    example annotation files built into :mod:`crowsetta`"""
    print("Example annotation files built into crowsetta")
    print("=" * 72)
    for example_ in EXAMPLES:
        print(
            f"Name: {example_.name}\n"
            f"Format name in `crowsetta`: {example_.format}\n"
            "Description:\n"
            f"{example_.description}\n"
        )
