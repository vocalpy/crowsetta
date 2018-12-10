import os
import csv

import numpy as np


# fields that must be present for each syllable that is annotated.
# these field names are used below by annot_list_to_csv and csv_to_annot_list
# but defined at top-level of the module, since these fields determine
# what annotations the library can and cannot interpret.
# The idea is to use the bare minimum of fields required.
SYL_ANNOT_COLUMN_NAMES = ['filename',
                          'onset_Hz',
                          'offset_Hz',
                          'onset_s',
                          'offset_s',
                          'label']
set_SYL_ANNOT_COLUMN_NAMES = set(SYL_ANNOT_COLUMN_NAMES)

# below maps each column in csv to a key in an annot_dict
# used when appending to lists that correspond to each key
SYL_ANNOT_TO_SONG_ANNOT_MAPPING = {'onset_Hz':'onsets_Hz',
                                   'offset_Hz': 'offsets_Hz',
                                   'onset_s': 'onsets_s',
                                   'offset_s': 'offsets_s',
                                   'label': 'labels'}

# used when mapping inputs **from** csv **to** annotation
SONG_ANNOT_TYPE_MAPPING = {'onsets_Hz': int,
                           'offsets_Hz': int,
                           'onsets_s': float,
                           'offsets_s': float,
                           'labels': str}


def func2seq(func, files):
    """converts files into Sequences using a user-specified function

    Parameters
    ----------
    func : function
    files : iterable or str

    Returns
    -------
    seq : Sequence
    """
    seq_list = []
    for file in files:
        seq_list.append(func(file))
    if len(seq_list) == 1:
        seq_list = seq_list[0]
    return seq_list


def _fix_annot_dict_types(annot_dict):
    """helper function that converts items in lists of annot dict
    from str to correct type, and then converts lists to numpy arrays"""
    for key, type_to_convert in SONG_ANNOT_TYPE_MAPPING.items():
        list_from_key = annot_dict[key]
        if type_to_convert == int:
            list_from_key = [int(el) for el in list_from_key]
        elif type_to_convert == float:
            list_from_key = [float(el) for el in list_from_key]
        elif type_to_convert == str:
            pass
        else:
            raise TypeError('Unexpected type {} specified in '
                            'conbirt'
                            .format(type_to_convert))
        annot_dict[key] = list_from_key
    # convert all lists to ndarray
    for col_name in (set_SYL_ANNOT_COLUMN_NAMES - {'filename'}):
        annot_dict[SYL_ANNOT_TO_SONG_ANNOT_MAPPING[col_name]] = \
            np.asarray(annot_dict[SYL_ANNOT_TO_SONG_ANNOT_MAPPING[col_name]])
    return annot_dict


def seq2csv(seq_list,
            csv_fname,
            abspath=False,
            basename=False):
    """writes annotations from files to a comma-separated value (csv) file.

    Parameters
    ----------
    seq_list : list
        list of Sequence objects, each of which has the following fields:
            file : str
                name of audio file with which annotation is associated.
                See parameter abspath and basename below that allow for specifying how
                filename is saved.
            onsets_Hz : numpy.ndarray
                of type int, onset of each annotated syllable in samples/second
            offsets_Hz : numpy.ndarray
                of type int, offset of each annotated syllable in samples/second
            onsets_s : numpy.ndarray
                of type float, onset of each annotated syllable in seconds
            offsets_s : numpy.ndarray
                of type float, offset of each annotated syllable in seconds
            labels : numpy.ndarray
                of type str, label for each annotated syllable
    csv_fname : str
        name of csv file to write to, will be created
        (or overwritten if it exists already)

    The following two parameters specify how file names for audio files are saved. These
    options are useful for working with multiple copies of files and for reproducibility.
    Default for both is False, in which case the filename is saved just as it is passed to
    this function.
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
    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    with open(csv_fname, 'w', newline='') as csvfile:
        # SYL_ANNOT_COLUMN_NAMES is defined above, at the level of the module,
        # to ensure consistency across all functions in this module
        # that make use of it
        writer = csv.DictWriter(csvfile, fieldnames=SYL_ANNOT_COLUMN_NAMES)

        writer.writeheader()
        for seq in seq_list:
            song_filename = seq.file
            if abspath:
                song_filename = os.path.abspath(song_filename)
            elif basename:
                song_filename = os.path.basename(song_filename)

            annot_dict_zipped = zip(seq.onsets_Hz,
                                    seq.offsets_Hz,
                                    seq.onsets_s,
                                    seq.offsets_s,
                                    seq.labels,
                                    )
            for onset_Hz, offset_Hz, onset_s, offset_s, label in annot_dict_zipped:
                syl_annot_dict = {'filename': song_filename,
                                  'onset_Hz': onset_Hz,
                                  'offset_Hz': offset_Hz,
                                  'onset_s': onset_s,
                                  'offset_s': offset_s,
                                  'label': label}
                writer.writerow(syl_annot_dict)


def csv2seqlist(csv_fname):
    """loads a comma-separated values (csv) file containing
    annotations for song files and returns an annot_list

    Parameters
    ----------
    csv_fname : str
        filename for comma-separated values file

    Returns
    -------
    annot_list : list
        list of dicts
    """
    annot_list = []

    with open(csv_fname, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)

        header = next(reader)
        set_header = set(header)
        if set_header != set_SYL_ANNOT_COLUMN_NAMES:
            not_in_FIELDNAMES = set_header.difference(set_SYL_ANNOT_COLUMN_NAMES)
            if not_in_FIELDNAMES:
                raise ValueError('The following column names in {} are not recognized: {}'
                                 .format(csv_fname, not_in_FIELDNAMES))
            not_in_header = set_FIELDNAMES.difference(set_header)
            if not_in_header:
                raise ValueError(
                    'The following column names in {} are required but missing: {}'
                    .format(csv_fname, not_in_header))

        column_name_index_mapping = {column_name: header.index(column_name)
                                     for column_name in SYL_ANNOT_COLUMN_NAMES}

        row = next(reader)
        curr_filename = row[column_name_index_mapping['filename']]
        annot_dict = {'filename': curr_filename,
                      'onsets_Hz': [],
                      'offsets_Hz': [],
                      'onsets_s': [],
                      'offsets_s': [],
                      'labels': []}
        for col_name in (set_SYL_ANNOT_COLUMN_NAMES - {'filename'}):
            annot_dict[SYL_ANNOT_TO_SONG_ANNOT_MAPPING[col_name]].append(
                row[column_name_index_mapping[col_name]])

        for row in reader:
            row_filename = row[column_name_index_mapping['filename']]
            if row_filename == curr_filename:
                for col_name in (set_SYL_ANNOT_COLUMN_NAMES - {'filename'}):
                    annot_dict[SYL_ANNOT_TO_SONG_ANNOT_MAPPING[col_name]].append(
                        row[column_name_index_mapping[col_name]])
            else:
                annot_dict = _fix_annot_dict_types(annot_dict)
                annot_list.append(annot_dict)
                # and start a new annot_dict
                curr_filename = row_filename
                annot_dict = {'filename': curr_filename,
                              'onsets_Hz': [],
                              'offsets_Hz': [],
                              'onsets_s': [],
                              'offsets_s': [],
                              'labels': []}
                for col_name in (set_SYL_ANNOT_COLUMN_NAMES - {'filename'}):
                    annot_dict[SYL_ANNOT_TO_SONG_ANNOT_MAPPING[col_name]].append(
                        row[column_name_index_mapping[col_name]])
        # lines below appends annot_dict corresponding to last file
        # since there won't be another file after it to trigger the 'else' logic above
        annot_dict = _fix_annot_dict_types(annot_dict)
        annot_list.append(annot_dict)

    return annot_list
