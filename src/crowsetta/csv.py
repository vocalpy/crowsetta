"""module of functions for handling csv files"""
import os
import csv

from .annotation import Annotation
from .meta import Meta
from .segment import Segment
from .sequence import Sequence
from .stack import Stack


CSV_FIELDNAMES = [
    'label',
    'onset_s',
    'offset_s',
    'onset_ind',
    'offset_ind',
    'audio_path',
    'annot_path',
    'sequence',
    'annotation'
]


FIELD_TYPES = {
    'label': str,
    'onset_s': float,
    'offset_s': float,
    'onset_ind': int,
    'offset_ind': int,
    'audio_path': str,
    'annot_path': str,
    'sequence': int,
    'annotation': int,
}


def annot2csv(annot,
              csv_filename,
              abspath=False,
              basename=False):
    """write annotations from files to a comma-separated value (csv) file.

    Parameters
    ----------
    annot : Annotation or list of Annotations
    csv_filename : str
        name of csv file to write to, will be created
        (or overwritten if it exists already)

    Other Parameters
    ----------------
    abspath : bool
        if True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        if True, discard any information about path and just use file name.
        Default is False.

    Returns
    -------
    None

    Notes
    -----
    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful when working with multiple copies of files, and for
    reproducibility (so you know which copy of a file you were working with).
    Default for both is False, in which case the filename is saved just as it is passed to
    this function in a Sequence object.
    """
    if type(annot) == Annotation:
        # put in a list so we can iterate over it
        annot = [annot]
    elif type(annot) == list:
        if not all([type(annot_) == Annotation for annot_ in annot]):
            raise TypeError('not all objects in annot are of type Annotation')
    else:
        raise TypeError('annot must be Annotation or list of Annotations, '
                        f'not type {type(annot)})')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)

        writer.writeheader()

        for annot_num, annot_ in enumerate(annot):
            if hasattr(annot_, 'stack'):
                seq_list = annot_.stack.seqs
            else:
                seq_list = [annot_.seq]
            for seq_num, seq in enumerate(seq_list):
                for segment in seq.segments:
                    row = segment.asdict()
                    row = {
                        key: ('None' if val is None else val)
                        for key, val in row.items()
                    }
                    annot_path = annot_.annot_path
                    audio_path = annot_.audio_path
                    if abspath:
                        annot_path = os.path.abspath(annot_path)
                        if audio_path is not None:
                            audio_path = os.path.abspath(audio_path)
                    elif basename:
                        annot_path = os.path.basename(annot_path)
                        if audio_path is not None:
                            audio_path = os.path.basename(audio_path)
                    row['annot_path'] = annot_path
                    if audio_path is not None:
                        row['audio_path'] = audio_path
                    else:
                        row['audio_path'] = 'None'
                    # we use 'sequence' and 'annotation' fields when we are
                    # loading back into Annotations
                    row['sequence'] = seq_num
                    row['annotation'] = annot_num

                    writer.writerow(row)


def toannot_func_to_csv(toannot_func):
    """accepts a function for turning files of a certain format into Annotations,
    and returns a function, `annot2seq2csv` that will convert that format into
    csv files. Essentially creates a wrapper around some `format2seq` function
    and the `annot2csv` function.

    Parameters
    ----------
    toseq_func : callable
        function that accepts a file argument (and keyword arguments, if needed),
        and returns a Sequence or list of Sequence

    Returns
    -------
    format2seq2csv : callable
        function that accepts a file argument, a dictionary of keywords and arguments
        to use to call the toseq_func, and a dictionary of keywords and arguments to
        pass to the seq2csv function.

    Examples
    --------
    >>> from my_format_module import myformat2annot
    >>> myformat2csv = toannot_func_to_csv(myformat2annot)
    >>> to_csv_kwargs = {csv_filename: 'my_format_bird1.csv', 'abspath': True}
    >>> myformat2csv('my_annotation.txt', to_csv_kwargs=to_csv_kwargs)
    """
    def format2annot2csv(file, csv_filename, abspath=False, basename=False, **to_annot_kwargs):
        """wrapper around a to_seq function and the seq2csv function.
        Returned by format2seq2csv

        Parameters
        ----------
        file : str or list
            annotation file or files to load into Sequences
        csv_filename : str
            name of .csv file that will be saved
        **to_annot_kwargs
            arbitrary keyword arguments to pass to the to_annot function, if needed. Default is None.

        Other Parameters
        ----------------
        abspath : bool
            if True, converts filename for each audio file into absolute path.
            Default is False.
        basename : bool
            if True, discard any information about path and just use file name.
            Default is False.

        Returns
        -------
        None
        """
        annot = toannot_func(file, **to_annot_kwargs)
        annot2csv(annot, csv_filename, abspath=abspath, basename=basename)

    return format2annot2csv


def csv2annot(csv_filename):
    """loads a comma-separated values (csv) file containing annotations
    for song files, returns contents as a list of Annotation objects

    Parameters
    ----------
    csv_filename : str
        filename for comma-separated values file

    Returns
    -------
    annot_list : list
        list of Annotations
    """
    annot_list = []

    with open(csv_filename, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)

        # DictReader automatically uses first row (AKA 'header') as fieldnames
        # when no argument supplied for fieldnames parameter
        # so we use that default to check validity of csv fieldnames
        set_header = set(reader.fieldnames)
        if set_header != set(CSV_FIELDNAMES):
            not_in_FIELDS = set_header.difference(set(CSV_FIELDNAMES))
            if not_in_FIELDS:
                raise ValueError('The following column names in {} are not recognized: {}'
                                 .format(csv_filename, not_in_FIELDS))
        not_in_header = set(CSV_FIELDNAMES).difference(set_header)
        if not_in_header:
            raise ValueError(
                'The following column names in {} are required but missing: {}'
                .format(csv_filename, not_in_header))

        row = next(reader)
        row.update((key, converter(row[key]))
                   if row[key] != 'None'
                   else (key, None)
                   for key, converter in FIELD_TYPES.items())
        segment = Segment.from_row(row=row)
        curr_seq = row['sequence']
        curr_annot = row['annotation']
        curr_annot_path_list = [row['annot_path']]
        curr_audio_path_list = [row['audio_path']]

        segments = [segment]
        seq_list = []
        annot_list = []
        for row_num, row in enumerate(reader):
            row.update((key, converter(row[key]))
                       if row[key] != 'None'
                       else (key, None)
                       for key, converter in FIELD_TYPES.items())
            segment = Segment.from_row(row=row)
            # if this is still the same sequence and/or annotation
            if row['sequence'] == curr_seq and row['annotation'] == curr_annot:
                # append to growing list of segments
                segments.append(segment)
                curr_annot_path_list.append(row['annot_path'])
                curr_audio_path_list.append(row['audio_path'])
            else:
                # either sequence **or** annotation changed
                # so make sequence from the one we just finished
                seq = Sequence.from_segments(segments)
                seq_list.append(seq)
                curr_seq = row['sequence']
                # start a new segments list that starts with the segment we just made
                segments = [segment]  # that will go into this next seq we just started
                # if we're still on the same annotation
                if row['annotation'] == curr_annot:
                    curr_annot_path_list.append(row['annot_path'])
                    curr_audio_path_list.append(row['audio_path'])
                else:  # annot file changed too
                    if len(seq_list) == 1:
                        annot_path = set(curr_annot_path_list)
                        if len(annot_path) != 1:
                            raise ValueError(
                                'A single annotation should be associated with a '
                                'single annotation file but the found the following set: '
                                f'{annot_path}'
                            )
                        else:
                            annot_path = annot_path.pop()

                        audio_path = set(curr_audio_path_list)
                        if len(audio_path) != 1:
                            raise ValueError(
                                'A single annotation should be associated with a single'
                                'audio file but the found the following set: '
                                f'{audio_path}'
                            )
                        else:
                            audio_path = audio_path.pop()

                        annot = Annotation(seq=seq_list[0], annot_path=annot_path,
                                           audio_path=audio_path)
                    elif len(seq_list) > 1:
                        stack = Stack(seqs=seq_list)
                        annot = Annotation(stack=stack, annot_path=annot_path,
                                           audio_path=audio_path)
                    else:
                        raise ValueError(
                            f'invalid sequence length: {len(seq_list)}\n'
                            f'in row from csv: {csv_filename}\n'
                            f'row: {row}')

                    annot_list.append(annot)
                    seq_list = []
                    curr_annot_path_list = [row['annot_path']]
                    curr_audio_path_list = [row['audio_path']]
                    curr_annot = row['annotation']

        # lines below appends annot_dict corresponding to last file
        # since there won't be another file after it to trigger the 'else' logic above
        seq = Sequence.from_segments(segments)
        seq_list.append(seq)

        if len(seq_list) == 1:
            annot_path = set(curr_annot_path_list)
            if len(annot_path) != 1:
                raise ValueError(
                    'A single annotation should be associated with a '
                    'single annotation file but the found the following set: '
                    f'{annot_path}'
                )
            else:
                annot_path = annot_path.pop()

            audio_path = set(curr_audio_path_list)
            if len(audio_path) != 1:
                raise ValueError(
                    'A single annotation should be associated with a single'
                    'audio file but the found the following set: '
                    f'{audio_path}'
                )
            else:
                audio_path = audio_path.pop()

            annot = Annotation(seq=seq_list[0], annot_path=annot_path,
                               audio_path=audio_path)
        elif len(seq_list) > 1:
            stack = Stack(seqs=seq_list)
            annot = Annotation(stack=stack, annot_path=annot_path)

        annot_list.append(annot)

    return annot_list


meta = Meta(
    name='csv',
    ext='csv',
    from_file=csv2annot,
    to_csv=annot2csv,
)
