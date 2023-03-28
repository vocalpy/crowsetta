"""Module with functions that handle the following dataset:
Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.
https://doi.org/10.6084/m9.figshare.3470165.v1
https://figshare.com/articles/BirdsongRecognition/3470165

as used in this paper:
Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""
import pathlib
import warnings
from typing import ClassVar, List, Optional

import attr
import birdsongrec
import numpy as np
import soundfile

import crowsetta
from crowsetta.typing import PathLike


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
        List of :class:`birdsongrec.Sequence` instances.
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

    sequences: List[birdsongrec.Sequence]
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
        >>> example = crowsetta.data.get('birdsong-recognition-dataset')
        >>> birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(example.annot_path)

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
        birdsongrec_seqs = birdsongrec.parse_xml(annot_path, concat_seqs_into_songs=concat_seqs_into_songs)
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
            ``birdsongrec.Syllable`` from sample number
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
        >>> example = crowsetta.data.get('birdsong-recognition-dataset')
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
            ``birdsongrec.Syllable`` from sample number
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
        >>> example = crowsetta.data.get('birdsong-recognition-dataset')
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
