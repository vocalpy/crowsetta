import os
from glob import glob
import csv
from pathlib import Path, PureWindowsPath

import numpy as np
import evfuncs

import crowsetta


def test_notmat2annot_single_str(a_notmat):
    annot = crowsetta.notmat.notmat2annot(str(a_notmat))
    assert isinstance(annot, crowsetta.Annotation)
    assert hasattr(annot, 'seq')


def test_notmat2annot_list_of_str(notmats):
    notmats = [str(notmat) for notmat in notmats]
    annots = crowsetta.notmat.notmat2annot(notmats)
    assert isinstance(annots, list)
    assert len(annots) == len(notmats)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_notmat2annot_list_of_Path(notmats):
    annots = crowsetta.notmat.notmat2annot(notmats)
    assert isinstance(annots, list)
    assert len(annots) == len(notmats)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_notmat2csv(notmats,
                    tmp_path):
    # since notmat_list_to_csv is basically a wrapper around
    # notmat2annot and seq2csv,
    # and those are tested above and in other test modules,
    # here just need to make sure this function doesn't fail
    csv_filename = tmp_path / 'test.csv'
    crowsetta.notmat.notmat2csv(notmats, csv_filename)
    # make sure file was created
    assert csv_filename.exists()

    # to be extra sure, make sure all filenames from
    # .not.mat list are in csv
    filenames_from_csv = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filenames_from_csv.append(
                os.path.basename(row['annot_path'])
            )
    for notmat in notmats:
        assert os.path.basename(notmat) in filenames_from_csv


def test_make_notmat(tmp_path,
                     notmats):
    for notmat in notmats:
        notmat_dict = evfuncs.load_notmat(notmat)
        annot = crowsetta.notmat.notmat2annot(notmat, round_times=False)
        seq_dict = annot.seq.as_dict()
        filename = notmat.replace('.not.mat', '')
        crowsetta.notmat.make_notmat(filename=filename,
                                     labels=np.asarray(list(notmat_dict['labels'])),
                                     onsets_s=seq_dict['onsets_s'],
                                     offsets_s=seq_dict['offsets_s'],
                                     samp_freq=notmat_dict['Fs'],
                                     threshold=notmat_dict['threshold'],
                                     min_syl_dur=notmat_dict['min_dur']/1000,
                                     min_silent_dur=notmat_dict['min_int']/1000,
                                     alternate_path=tmp_path,
                                     other_vars=None
                                     )
        notmat_made = evfuncs.load_notmat(os.path.join(tmp_path,
                                                       os.path.basename(notmat)))
        # can't do assert(new_dict == old_dict)
        # because headers will be different (and we want them to be different)
        for key in ['Fs', 'fname', 'labels', 'onsets', 'offsets',
                    'min_int', 'min_dur', 'threshold', 'sm_win']:
            if key == 'fname':
                # have to deal with Windows path saved in .not.mat files
                # and then compare file names without path to them
                notmat_dict_path = PureWindowsPath(notmat_dict[key])
                notmat_made_path = Path(notmat_made[key])
                assert notmat_dict_path.name == notmat_made_path.name
            elif type(notmat_dict[key]) == np.ndarray:
                assert np.allclose(notmat_dict[key],
                                   notmat_made[key],
                                   atol=1e-3, rtol=1e-3)
            else:
                assert notmat_dict[key] == notmat_made[key]
