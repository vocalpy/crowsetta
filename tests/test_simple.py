import os
from glob import glob
import csv
from pathlib import Path, PureWindowsPath

import numpy as np

import crowsetta


def test_simple2annot_single_str(simple_csvs):
    for a_simple_csv in simple_csvs:
        annot = crowsetta.simple.simple2annot(str(a_simple_csv))
        assert isinstance(annot, crowsetta.Annotation)
        assert hasattr(annot, 'seq')


def test_simple2annot_list_of_str(simple_csvs):
    simple_csvs = [str(simple_csv) for simple_csv in simple_csvs]
    annots = crowsetta.simple.simple2annot(simple_csvs)
    assert isinstance(annots, list)
    assert len(annots) == len(simple_csvs)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_simple2annot_list_of_Path(simple_csvs):
    annots = crowsetta.simple.simple2annot(simple_csvs)
    assert isinstance(annots, list)
    assert len(annots) == len(simple_csvs)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_simple2csv(simple_csvs,
                    tmp_path):
    # since simple_to_csv is basically a wrapper around
    # simple2annot and seq2csv,
    # and those are tested above and in other test modules,
    # here just need to make sure this function doesn't fail
    csv_filename = tmp_path / 'test.csv'
    crowsetta.simple.simple2csv(simple_csvs, csv_filename)
    # make sure file was created
    assert csv_filename.exists()

    # to be extra sure, make sure all filenames from
    # .not.mat list are in csv
    filenames_from_csv = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # header = next(reader)
        for row in reader:
            filenames_from_csv.append(
                os.path.basename(row['annot_path'])
            )
    for simple_csv in simple_csvs:
        try:
            assert os.path.basename(simple_csv) in filenames_from_csv
        except AssertionError:
            breakpoint()
