"""module with functions that handle .phn annotation files from the TIMIT dataset
"""
import pathlib
from typing import ClassVar, Optional
import warnings

import attr
import numpy as np
import pandas as pd
import pandera
from pandera.typing import Series
import soundfile

import crowsetta
from crowsetta.typing import PathLike


class TimitTranscriptSchema(pandera.SchemaModel):
    """A ``pandera.SchemaModel`` that validates ``pandas`` dataframes
    loaded from a .phn or .wrd file in the TIMIT transcription format.
    """
    begin_sample: Optional[Series[int]] = pandera.Field()
    end_sample: Optional[Series[int]] = pandera.Field()
    text: Series[pd.StringDtype] = pandera.Field(coerce=True)

    class Config:
        ordered = True
        strict = True


@crowsetta.interface.SeqLike.register
@attr.define
class Timit:
    """Class that represents annotations from transcription files in the
    DARPA TIMIT Acoustic-Phonetic Continuous Speech Corpus (TIMIT)

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'timit'``.
    ext: str
        Extension of files in annotation format:
        ``('.phn', '.PHN', '.wrd', '.WRD')``
    begin_samples : numpy.ndarray
        Vector of integer sample numbers corresponding
        to beginning of segments, i.e. onsets
    end_samples : numpy.ndarray
        Vector of integer sample numbers corresponding
        to ends of segments, i.e. offsets
    text : numpy.ndarray
        Vector of string labels for segments;
        each element is either a single word,
        or a single phonetic transcription code.
    annot_path : str, pathlib.Path
        Path to TIMIT transcription file from which annotations were loaded.
    audio_path : str. pathlib.Path
        Path to audio file that the TIMIT transcription file annotates.
    """
    name: ClassVar[str] = 'timit'
    ext: ClassVar[str] = ('.phn', '.PHN', '.wrd', '.WRD')

    begin_samples: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    end_samples: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    text: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path
    audio_path: Optional[pathlib.Path] = attr.field(default=None,
                                                    converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(cls,
                  annot_path: PathLike,
                  audio_path: Optional[PathLike] = None) -> 'Self':
        """Load annotations from a TIMIT transcription file

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to a TIMIT transcription file,
            with one of the extensions {'.phn', '.PHN', '.wrd', '.WRD'}.
        audio_path : str, pathlib.Path
            Optional, defaults to ``annot_path`` with the extension
            changed to '.wav' or '.WAV'. Both extensions are checked
            and if either file exists, that one is used. Otherwise,
            defaults to '.wav' in lowercase.

        Examples
        --------
        >>> example = crowsetta.data.get('timit')
        >>> timit = crowsetta.formats.seq.Timit.from_file(example.annot_path)

        Notes
        -----
        Versions of the dataset exist with the extensions
        in capital letters. Some platforms may not have case-sensitive paths.
        """
        annot_path = pathlib.Path(annot_path)
        # note multiple extensions, both all-uppercase and all-lowercase `.phn` exist,
        # depending on which version of TIMIT dataset you have
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        #  assume file is space-separated with no header
        df = pd.read_csv(annot_path,  sep=' ', header=None)
        df.columns = ['begin_sample', 'end_sample', 'text']
        df = TimitTranscriptSchema.validate(df)

        if audio_path is None:
            for ext in ('.wav', '.WAV'):
                audio_path = annot_path.parent / (annot_path.stem + ext)
                if audio_path.exists():
                    break
            if not audio_path.exists():
                # just default to lower-case .wav
                audio_path = annot_path.parent / (annot_path.stem + '.wav')

        return cls(
            annot_path=annot_path,
            begin_samples=df['begin_sample'].values,
            end_samples=df['end_sample'].values,
            text=df['text'].values,
            audio_path=audio_path,
        )

    def to_seq(self,
               round_times: bool = True,
               decimals: int = 3,
               samplerate: Optional[int] = None) -> crowsetta.Sequence:
        """Convert this TIMIT annotation to a ``crowsetta.Sequence``.

        Parameters
        ----------
        round_times : bool
            if True, round onsets_s and offsets_s.
            Default is True.
        decimals : int
            number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.
        samplerate : int
            Sampling rate for wave files. Used to convert
            ``begin_samples`` and ``end_samples``
            from sample number to seconds.
            Default is None, in which ths function
            tries to open ``audio_path`` and determine
            the actual sampling rate. If this does not work,
            then the ``onsets_s`` and ``offsets_s`` attributes
            of the ``crowsetta.Sequence`` are left as None.

        Examples
        --------
        >>> example = crowsetta.data.get('timit')
        >>> timit = crowsetta.formats.seq.Timit.from_file(example.annot_path)
        >>> seq = timit.to_seq()

        Returns
        -------
        phn_seq : crowsetta.Sequence

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        onset_samples = self.begin_samples
        offset_samples = self.end_samples
        labels = self.text

        if samplerate is None:
            try:
                samplerate = soundfile.info(self.audio_path).samplerate
            except RuntimeError:
                warnings.warn(
                    f'wav file not found: {self.audio_path}.'
                    f'Could not determine sampling rate to convert onsets and offsets to seconds. '
                    f'To use a fixed sampling rate for all files, pass in a value for the `samplerate` '
                    f'argument, but be aware that this may not be the correct sampling rate for some files.',
                    UserWarning
                )
                samplerate = None

        onsets_s = onset_samples / samplerate
        offsets_s = offset_samples / samplerate

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        phn_seq = crowsetta.Sequence.from_keyword(labels=labels,
                                                  onset_samples=onset_samples,
                                                  offset_samples=offset_samples,
                                                  onsets_s=onsets_s,
                                                  offsets_s=offsets_s)
        return phn_seq

    def to_annot(self,
                 round_times: bool = True,
                 decimals: int = 3,
                 samplerate: Optional[int] = None) -> crowsetta.Annotation:
        """Convert this TIMIT annotation to a ``crowsetta.Annotation``.

        Parameters
        ----------
        round_times : bool
            if True, round onsets_s and offsets_s.
            Default is True.
        decimals : int
            number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.
        samplerate : int
            Sampling rate for wave files. Used to convert
            ``begin_samples`` and ``end_samples``
            from sample number to seconds.
            Default is None, in which ths function
            tries to open ``audio_path`` and determine
            the actual sampling rate. If this does not work,
            then the ``onsets_s`` and ``offsets_s`` attributes
            of the ``crowsetta.Sequence`` are left as None.

        Examples
        --------
        >>> example = crowsetta.data.get('timit')
        >>> timit = crowsetta.formats.seq.Timit.from_file(example.annot_path)
        >>> annot = timit.to_annot()

        Returns
        -------
        annot : crowsetta.Annotation

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        phn_seq = self.to_seq(round_times, decimals, samplerate)
        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, seq=phn_seq)

    def to_file(self,
                annot_path: PathLike) -> None:
        """make a .phn file from an annotation

        Parameters
        ----------
        annot_path : str, pahtlib.Path
             path including filename where file should be saved.
             Must have a valid extension for TIMIT transcription files,
             one of {'.phn', '.PHN', '.wrd', '.WRD'}.
        """
        crowsetta.validation.validate_ext(annot_path, extension=self.ext)

        lines = []
        for begin_sample, end_sample, text in zip(self.begin_samples.tolist(),
                                                  self.end_samples.tolist(),
                                                  list(self.text)):
            lines.append(
                f'{begin_sample} {end_sample} {text}\n'
            )

        with annot_path.open('w') as fp:
            fp.writelines(lines)
