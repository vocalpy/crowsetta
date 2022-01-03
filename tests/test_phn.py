import os
from glob import glob
import shutil
import csv
from pathlib import Path

import numpy as np

import crowsetta


def test_phn2annot_single_str(a_phn):
    annot = crowsetta.phn.phn2annot(a_phn)
    assert type(annot) == crowsetta.Annotation
    assert hasattr(annot, 'seq')


def test_phn2annot_list_of_str(phns):
    phns = [str(phn) for phn in phns]
    annots = crowsetta.phn.phn2annot(phns)
    assert isinstance(annots, list)
    assert len(annots) == len(phns)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_phn2annot_list_of_Path(phns):
    annots = crowsetta.phn.phn2annot(phns)
    assert isinstance(annots, list)
    assert len(annots) == len(phns)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_phn2csv(phns,
                 tmp_path):
    csv_filename = tmp_path / 'test.csv'
    crowsetta.phn.phn2csv(phns, csv_filename)
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
    for phn_name in phns:
        assert os.path.basename(phn_name) in filenames_from_csv


def test_annot2phn(tmp_path, phns):
    for phn in phns:
        annot = crowsetta.phn.phn2annot(phn, round_times=False)
        annot_path = Path(tmp_path).joinpath(Path(phn).name)
        # copy wav file to tmp_path so we can open the annot
        # need sampling rate from wave file
        shutil.copyfile(src=annot.audio_path, dst=Path(tmp_path).joinpath(Path(annot.audio_path.name)))
        crowsetta.phn.annot2phn(annot, annot_path)
        annot_made = crowsetta.phn.phn2annot(annot_path)
        assert np.all(np.equal(annot.seq.onset_inds, annot_made.seq.onset_inds))
        assert np.all(np.equal(annot.seq.offset_inds, annot_made.seq.offset_inds))
        assert np.all(np.char.equal(annot.seq.labels, annot_made.seq.labels))


def test_PHN2annot_single_str(a_PHN):
    """same unit-test as above, but here
    test function still works when .phn extension is capitalized
    and audio files are alternate .WAV format"""
    annot = crowsetta.phn.phn2annot(a_PHN)
    assert type(annot) == crowsetta.Annotation
    assert hasattr(annot, 'seq')


def test_PHN2annot_list_of_str(PHNs):
    """same unit-test as above, but here
    test function still works when .phn extension is capitalized
    and audio files are alternate .WAV format"""
    PHNs = [str(PHN) for PHN in PHNs]
    annots = crowsetta.phn.phn2annot(PHNs)
    assert isinstance(annots, list)
    assert len(annots) == len(PHNs)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_PHN2annot_list_of_Path(PHNs):
    """same unit-test as above, but here
    test function still works when .phn extension is capitalized
    and audio files are alternate .WAV format"""
    annots = crowsetta.phn.phn2annot(PHNs)
    assert isinstance(annots, list)
    assert len(annots) == len(PHNs)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_PHN2csv(tmp_path, PHNs):
    """same unit-test as above, but here
    test function still works when .phn extension is capitalized
    and audio files are alternate .WAV format"""
    # since notmat_list_to_csv is basically a wrapper around
    # notmat2annot and seq2csv,
    # and those are tested above and in other test modules,
    # here just need to make sure this function doesn't fail
    csv_filename = tmp_path / 'test.csv'
    crowsetta.phn.phn2csv(PHNs, csv_filename)
    # make sure file was created
    assert csv_filename.exists()

    # to be extra sure, make sure all filenames from
    # .not.mat list are in csv
    filenames_from_csv = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile,
                                fieldnames=crowsetta.csv.CSV_FIELDNAMES)
        header = next(reader)
        for row in reader:
            filenames_from_csv.append(
                os.path.basename(row['annot_path'])
            )
    for phn_name in PHNs:
        assert os.path.basename(phn_name) in filenames_from_csv


def test_annot2PHN(tmp_path, PHNs):
    for phn in PHNs:
        annot = crowsetta.phn.phn2annot(phn, round_times=False)
        annot_path = Path(tmp_path).joinpath(Path(phn).name)
        # copy wav file to tmp_path so we can open the annot
        # need sampling rate from wave file
        shutil.copyfile(src=annot.audio_path, dst=Path(tmp_path).joinpath(Path(annot.audio_path.name)))
        crowsetta.phn.annot2phn(annot, annot_path)
        annot_made = crowsetta.phn.phn2annot(annot_path)
        assert np.all(np.equal(annot.seq.onset_inds, annot_made.seq.onset_inds))
        assert np.all(np.equal(annot.seq.offset_inds, annot_made.seq.offset_inds))
        assert np.all(np.char.equal(annot.seq.labels, annot_made.seq.labels))
