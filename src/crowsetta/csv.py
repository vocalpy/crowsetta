"""module of functions for handling with csv files"""
import os
import csv

from .segment import Segment
from .sequence import Sequence
from .annotation import Annotation


CSV_FIELDNAMES = [
    'label',
    'onset_s',
    'offset_s',
    'onset_Hz',
    'offset_Hz',
    'file',
    'sequence',
]


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

        for annot_ in annot:
            for seq_num, seq in enumerate(annot_.seq):
                for segment in seq.segments:
                    seg_dict = segment.asdict()
                    seg_dict = {
                        key: ('None' if val is None else val)
                        for key, val in seg_dict.items()
                    }
                    if abspath:
                        seg_dict['file'] = os.path.abspath(seg_dict['file'])
                    elif basename:
                        seg_dict['file'] = os.path.basename(seg_dict['file'])
                    seg_dict['sequence'] = seq_num

                    writer.writerow(seg_dict)


def toannot_func_to_csv(toseq_func):
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


def csv2seq(csv_filename):
    """loads a comma-separated values (csv) file containing annotations
    for song files, returns contents as a list of Sequence objects

    Parameters
    ----------
    csv_filename : str
        filename for comma-separated values file

    Returns
    -------
    seq_list : list
        list of crowsetta.tuples.Sequence objects
    """
    seq_list = []

    with open(csv_filename, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)

        header = next(reader)
        set_header = set(header)
        if set_header != set(Segment._FIELDS):
            not_in_FIELDS = set_header.difference(set(Segment._FIELDS))
            if not_in_FIELDS:
                raise ValueError('The following column names in {} are not recognized: {}'
                                 .format(csv_filename, not_in_FIELDS))
        not_in_header = set(Segment._FIELDS).difference(set_header)
        if not_in_header:
            raise ValueError(
                'The following column names in {} are required but missing: {}'
                .format(csv_filename, not_in_header))

        row = next(reader)
        row = [None if item == 'None' else item for item in row]
        segment = Segment.from_row(row=row, header=header)
        curr_file = segment.file
        segments = [segment]

        for row in reader:
            row = [None if item == 'None' else item for item in row]
            segment = Segment.from_row(row=row, header=header)
            row_file = segment.file
            if row_file == curr_file:
                segments.append(segment)
            else:
                seq = Sequence.from_segments(segments)
                seq_list.append(seq)
                # start a new segments list that starts with this segment
                curr_file = row_file
                segments = [segment]
        # lines below appends annot_dict corresponding to last file
        # since there won't be another file after it to trigger the 'else' logic above
        seq = Sequence.from_segments(segments)
        seq_list.append(seq)

    return seq_list
