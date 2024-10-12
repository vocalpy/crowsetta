"""Module with functions that handle the following dataset:
Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.
https://doi.org/10.6084/m9.figshare.3470165.v1
https://figshare.com/articles/BirdsongRecognition/3470165

as used in this paper:
Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""

from __future__ import annotations

import os
import pathlib
import warnings
import xml.etree.ElementTree as ET
from typing import ClassVar, List, Optional

import attr
import numpy as np
import soundfile

import crowsetta
from crowsetta.typing import PathLike


class BirdsongRecSyllable:
    """Object that represents a syllable.

    Attributes
    ----------
    position : int
        starting sample number ("frame") within .wav file
        *** relative to start of sequence! ***
    length : int
        duration given as number of samples
    label : str
        text representation of syllable as classified by a human
        or a machine learning algorithm
    """

    def __init__(self, position: int, length: int, label: str) -> None:
        if not isinstance(position, int):
            raise TypeError(f"position must be an int, not type {type(position)}")
        if not isinstance(length, int):
            raise TypeError(f"length must be an int, not type {type(length)}")
        if not isinstance(label, str):
            raise TypeError(f"label must be a string, not type {type(label)}")
        self.position = position
        self.length = length
        self.label = label

    def __repr__(self):
        return f"BirdsongRecSyllable(position={self.position}, length={self.length}, label={self.label})"


class BirdsongRecSequence:
    """Class from birdsong-recognition
    that represents a sequence of syllables.

    Attributes
    ----------
    wav_file : string
        file name of .wav file in which sequence occurs
    position : int
        starting sample number within .wav file
    length : int
        duration given as number of samples
    syls : list
        list of syllable objects that make up sequence
    seq_spect : spectrogram object
    """

    def __init__(self, wav_file: PathLike, position: int, length: int, syl_list: list[BirdsongRecSyllable]):
        if not isinstance(wav_file, (str, pathlib.Path)):
            raise TypeError(f"wav_file must be a string or pathlib.Path, not type {type(wav_file)}")
        wav_file = str(wav_file)
        if not isinstance(position, int):
            raise TypeError(f"position must be an int, not type {type(position)}")
        if not isinstance(length, int):
            raise TypeError(f"length must be an int, not type {type(length)}")
        if not isinstance(syl_list, list):
            raise TypeError(f"syl_list must be a list, not type {type(syl_list)}")
        if not all([isinstance(syl, BirdsongRecSyllable) for syl in syl_list]):
            raise TypeError("not all elements in syl list are of type BirdsongRecSyllable: " f"{syl_list}")
        self.wav_file = wav_file
        self.position = position
        self.length = length
        self.num_syls = len(syl_list)
        self.syls = syl_list

    def __repr__(self):
        return f"Sequence(wav_file={self.wav_file}, position={self.position}, length={self.length}, syls={self.syls})"


def parse_xml(
    xml_file: PathLike,
    concat_seqs_into_songs: bool = False,
    return_wav_abspath: bool = False,
    wav_abspath: PathLike = None,
) -> list[BirdsongRecSequence]:
    """parses Annotation.xml files from the BirdsongRecognition dataset:
    Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.
    https://doi.org/10.6084/m9.figshare.3470165.v1
    https://figshare.com/articles/BirdsongRecognition/3470165

    Parameters
    ----------
    xml_file : str
        filename of .xml file, e.g. 'Annotation.xml'
    concat_seqs_into_songs : bool
        if True, concatenate sequences into songs, where each .wav file is a
        song. Default is False.
    return_wav_abspath : bool
        if True, change value for the wav_file field of sequences to absolute path,
        instead of just the .wav file name (without a path). This option is
        useful if you need to specify the path to data on your system.
        Default is False, in which the .wav file name is returned as written in the
        Annotation.xml file.
    wav_abspath : str
        Path to directory in which .wav files are found. Specify this if you have changed
        the structure of the repository so that the .wav files are no longer in a
        directory named Wave that's in the same parent directory as the Annotation.xml
        file. Default is None, in which case the structure just described is assumed.

    Returns
    -------
    seq_list : list of BirdsongrecSequence objects
        if concat_seqs_into_songs is True, then each sequence will correspond to one song,
        i.e., the annotation for one .wav file

    Examples
    --------
    >>> seq_list = parse_xml(xml_file='./Bird0/Annotation.xml', concat_seqs_into_songs=False)
    >>> seq_list[0]
    Sequence from 0.wav with position 32000 and length 43168

    Notes
    -----
    Parses files that adhere to this XML Schema document:
    https://github.com/NickleDave/birdsong-recognition-dataset/blob/main/doc/xsd/AnnotationSchema.xsd
    """
    if return_wav_abspath:
        if wav_abspath:
            if not os.path.isdir(wav_abspath):
                raise NotADirectoryError(f"return_wav_abspath is True but {wav_abspath} " "is not a valid directory.")
    tree = ET.ElementTree(file=xml_file)
    seq_list = []
    for seq in tree.iter(tag="Sequence"):
        wav_file = seq.find("WaveFileName").text
        if return_wav_abspath:
            if wav_abspath:
                wav_file = os.path.join(wav_abspath, wav_file)
            else:
                # assume .wav file is in Wave directory that's a child to wherever
                # Annotation.xml file is kept (since this is how the repository is
                # structured)
                xml_dirname = os.path.dirname(xml_file)
                wav_file = os.path.join(xml_dirname, "Wave", wav_file)
            if not os.path.isfile(wav_file):
                raise FileNotFoundError("File {wav_file} is not found")

        position = int(seq.find("Position").text)
        length = int(seq.find("Length").text)
        syl_list = []
        for syl in seq.iter(tag="Note"):
            syl_position = int(syl.find("Position").text)
            syl_length = int(syl.find("Length").text)
            label = syl.find("Label").text

            syl_obj = BirdsongRecSyllable(position=syl_position, length=syl_length, label=label)
            syl_list.append(syl_obj)
        seq_obj = BirdsongRecSequence(wav_file=wav_file, position=position, length=length, syl_list=syl_list)
        seq_list.append(seq_obj)

    if concat_seqs_into_songs:
        song_list = []
        curr_wav_file = seq_list[0].wav_file
        new_seq_obj = seq_list[0]
        for syl in new_seq_obj.syls:
            syl.position += new_seq_obj.position

        for seq in seq_list[1:]:
            if seq.wav_file == curr_wav_file:
                new_seq_obj.length += seq.length
                new_seq_obj.num_syls += seq.num_syls
                for syl in seq.syls:
                    syl.position += seq.position
                new_seq_obj.syls += seq.syls

            else:
                song_list.append(new_seq_obj)
                curr_wav_file = seq.wav_file
                new_seq_obj = seq
                for syl in new_seq_obj.syls:
                    syl.position += new_seq_obj.position

        song_list.append(new_seq_obj)  # to append last song

        return song_list

    else:
        return seq_list


@crowsetta.interface.SeqLike.register
@attr.define
class BirdsongRec:
    """Class that represents annotations from the
    BirdsongRecognition dataset [1]_.
    This dataset was first used in Koumura and Okanoya 2016 [2]_.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'birdsong-recognition-dataset'``.
    ext: str
        Extension of files in annotation format: ``'.xml'``.
    sequences: list
        List of :class:`BirdsongRecSequence` instances.
    annot_path: pathlib.Path
        Path to file from which annotations were loaded.
        Typically with filename 'Annotation.xml'.
    wav_path: pathlib.Path
        Path to directory containing .wav files annotated by the .xml file.
        If not specified, defaults to directory "Wave", relative to the parent
        of ``xml_path``. E.g., if ``xml_path`` is 'Bird0/Annotation.xml'
        as shown below, then ``wav_path`` defaults to 'Bird0/Wave'.

            .. code-block:: console

                ├── Bird0
                │   ├── Annotation.xml
                │   └── Wave
                │       ├── 0.wav
                │       ├── 100.wav
                │       ├── 101.wav
                ...

        Used to obtain sampling rates,
        to convert onset and offset times from sample number to seconds,
        when converting annotations to ``crowsetta.Sequence``.


    Examples
    --------
    >>> birdsongrec = crowsetta.example('Annotation.xml')

    Notes
    -----
    This class uses the Python package ``birdsong-recognition-dataset``
    to load the annotations.
    https://github.com/NickleDave/birdsong-recognition-dataset
    That package creates Python objects from .xml files that obey
    this XML schema document:
    https://github.com/NickleDave/birdsong-recognition-dataset/blob/main/doc/xsd/AnnotationSchema.xsd

    References
    ----------

    .. [1] Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.
       https://doi.org/10.6084/m9.figshare.3470165.v1
       https://figshare.com/articles/BirdsongRecognition/3470165


    .. [2] Koumura T., Okanoya K. (2016) Automatic Recognition of Element Classes and
       Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
       https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0159188
       doi:10.1371/journal.pone.0159188
    """

    name: ClassVar[str] = "birdsong-recognition-dataset"
    ext: ClassVar[str] = ".xml"

    sequences: List[BirdsongRecSequence]
    annot_path: pathlib.Path = attr.field(converter=pathlib.Path)
    wav_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls, annot_path: PathLike, wav_path: Optional[PathLike] = None, concat_seqs_into_songs: bool = True
    ) -> "Self":  # noqa: F821
        """Load BirdsongRecognition annotations from an .xml file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to xml file from BirdsongRecognition dataset
            that contains annotations.
        wav_path : str, pathlib.Path
            Path in which wav files listed in Annotation.xml file are found.
            Defaults to a directory ``Wave`` that is located in the parent directory of
            the Annotation.xml file, which matches the structure of the dataset from [1]_.

            .. code-block:: console

                ├── Bird0
                │   ├── Annotation.xml
                │   └── Wave
                │       ├── 0.wav
                │       ├── 100.wav
                │       ├── 101.wav
                ...

        concat_seqs_into_songs : bool
            If True, concatenate sequences from ``annot_path``, so that
            one sequence = one song / .wav file. Default is True.

        Examples
        --------
        >>> path = crowsetta.example('Annotation.xml', return_path=True)
        >>> birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(path)

        .. [1] Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.
           https://doi.org/10.6084/m9.figshare.3470165.v1
           https://figshare.com/articles/BirdsongRecognition/3470165
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)
        if not annot_path.exists():
            raise FileNotFoundError(f"annot_path not found: {annot_path}")

        if wav_path is None:
            wav_path = annot_path.parent.joinpath("Wave")
        else:
            wav_path = pathlib.Path(wav_path)

        # `birdsong-recongition-dataset` has a 'Sequence' class
        # but it is different from a `crowsetta.Sequence`
        birdsongrec_seqs = parse_xml(annot_path, concat_seqs_into_songs=concat_seqs_into_songs)
        return cls(sequences=birdsongrec_seqs, annot_path=annot_path, wav_path=wav_path)

    def to_seq(
        self, round_times: bool = True, decimals: int = 3, samplerate: Optional[int] = None
    ) -> List[crowsetta.Sequence]:
        """Convert this set of ``'birdsong-recognition-dataset'``
        annotations to a list of :class:`crowsetta.Sequence` instances.

        Parameters
        ----------
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.
        samplerate : int
            Sampling rate for wave files. Used to convert
            ``position`` and ``length`` attributes of
            ``BirdsongrecSyllable`` from sample number
            to seconds. Default is None, in which ths function
            tries to open each .wav file and determine
            the actual sampling rate. If this does not work,
            then the ``onsets_s`` and ``offsets_s`` attributes
            of the :class:`crowsetta.Sequence` are left as None.

        Returns
        -------
        seqs : list
            A :class:`list` of :class:`crowsetta.Sequence` instances.

        Examples
        --------
        >>> example = crowsetta.example('birdsong-recognition-dataset')
        >>> birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(example.annot_path)
        >>> seqs = birdsongrec.to_seq()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g., when loading
        annotation files and then sending them to a csv file,
        the result should be the same on Windows and Linux.

        The ``samplerate`` argument is provided to make it possible
        to convert onset and offset times from sample number to seconds,
        even without the original audio files.
        By default it is ``None``, and the default
        location for the .wav files is used.
        If you need to specify some other location for the ``.wav`` files,
        pass in the ``wavpath`` argument when you first load the annotations:

        >>> birdsongrec = crowsetta.formats.BirdsongRec.from_file(annot_path, wav_path='./actually/wavs/are/here')  # doctest: +SKIP # noqa:  E501
        """
        seqs = []
        for birdsongrec_seq in self.sequences:
            onset_samples = np.array([syl.position for syl in birdsongrec_seq.syls])
            offset_samples = np.array([syl.position + syl.length for syl in birdsongrec_seq.syls])
            labels = np.array(
                # NOTE we convert syl.label to string so dtype is consistent across formats
                # and to adhere to schema for `'generic-seq'`
                [str(syl.label) for syl in birdsongrec_seq.syls]
            )
            wav_filename = self.wav_path / birdsongrec_seq.wav_file

            if samplerate is None:
                try:
                    samplerate_this_wav = soundfile.info(wav_filename).samplerate
                except RuntimeError:
                    warnings.warn(
                        f"wav file not found: {wav_filename}."
                        f"Could not determine sampling rate to convert onsets and offsets to seconds. "
                        f"To use a fixed sampling rate for all files, pass in a value for the `samplerate` "
                        f"argument. Be aware that this may not be the correct sampling rate for all files.",
                        UserWarning,
                        stacklevel=2,
                    )
                    samplerate_this_wav = None
            else:
                samplerate_this_wav = samplerate

            if samplerate_this_wav:
                onsets_s = onset_samples / samplerate_this_wav
                offsets_s = offset_samples / samplerate_this_wav
                if round_times:
                    onsets_s = np.round(onsets_s, decimals=decimals)
                    offsets_s = np.round(offsets_s, decimals=decimals)
            else:
                onsets_s = None
                offsets_s = None

            seq = crowsetta.Sequence.from_keyword(
                onset_samples=onset_samples,
                offset_samples=offset_samples,
                onsets_s=onsets_s,
                offsets_s=offsets_s,
                labels=labels,
            )
            seqs.append(seq)
        return seqs

    def to_annot(
        self, round_times: bool = True, decimals: int = 3, samplerate: Optional[int] = None
    ) -> List[crowsetta.Annotation]:
        """Convert this set of ``'birdsong-recognition-dataset'``
        annotations to a :class:`list` of :class:`crowsetta.Annotation` instances.

        Parameters
        ----------
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.
        samplerate
            Sampling rate for wave files. Used to convert
            ``position`` and ``length`` attributes of
            ``BirdsongRecSyllable`` from sample number
            to seconds. Default is None, in which ths function
            tries to open each .wav file and determine
            the actual sampling rate. If this does not work,
            then the ``onsets_s`` and ``offsets_s`` attributes
            of the :class:`crowsetta.Sequence` are left as None.

        Returns
        -------
        annots : list
            A list of :class:`crowsetta.Annotation` instances.

        Examples
        --------
        >>> example = crowsetta.example('birdsong-recognition-dataset')
        >>> birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(example.annot_path)
        >>> annots = birdsongrec.to_annot()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g., when loading
        annotation files and then sending them to a csv file,
        the result should be the same on Windows and Linux.

        The ``samplerate`` argument is provided to make it possible
        to convert onset and offset times from sample number to seconds,
        even without the original audio files.
        By default it is ``None``, and the default
        location for the .wav files is used.
        If you need to specify some other location for the ``.wav`` files,
        pass in the ``wavpath`` argument when you first load the annotations:

        >>> birdsongrec = crowsetta.formats.BirdsongRec.from_file(annot_path, wav_path='./actually/wavs/are/here')  # doctest: +SKIP # noqa: E501
        """
        seqs = self.to_seq(round_times=round_times, decimals=decimals, samplerate=samplerate)
        wav_filenames = [self.wav_path / birdsongrec_seq.wav_file for birdsongrec_seq in self.sequences]
        annot_list = []
        for seq, wav_filename in zip(seqs, wav_filenames):
            annot_list.append(crowsetta.Annotation(seq=seq, annot_path=self.annot_path, notated_path=wav_filename))
        return annot_list
