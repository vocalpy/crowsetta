import csv

import crowsetta


def test_textgrid2annot_single_str(a_textgrid):
    annot = crowsetta.textgrid.textgrid2annot(a_textgrid)
    assert type(annot) == crowsetta.Annotation


def test_textgrid2annot_list_of_str(textgrids):
    textgrids = [str(textgrid) for textgrid in textgrids]
    annots = crowsetta.textgrid.textgrid2annot(textgrids)
    assert type(annots) == list
    assert len(annots) == len(textgrids)
    assert all([type(annot) == crowsetta.Annotation
                for annot in annots])


def test_textgrid2annot_list_of_Path(textgrids):
    annots = crowsetta.textgrid.textgrid2annot(textgrids)
    assert type(annots) == list
    assert len(annots) == len(list(textgrids))
    assert all([type(annot) == crowsetta.Annotation
                for annot in annots])


def test_textgrid2csv(textgrids, tmp_path):
    # since textgrid2csv is basically a wrapper around
    # textgrid2annot and seq2csv,
    # and those are tested above and in other test modules,
    # here just need to make sure this function doesn't fail
    csv_filename = tmp_path / 'test.csv'
    crowsetta.textgrid.textgrid2csv(textgrids, csv_filename)
    # make sure file was created
    assert csv_filename.exists()

    # to be extra sure, make sure all filenames from
    # .TextGrid list are in csv
    audio_paths_from_csv = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            audio_paths_from_csv.append(row['audio_path'])
    for textgrid_path in textgrids:
        wav_path = str(
            textgrid_path.parent / textgrid_path.name.replace('.TextGrid', '.wav')
        )
        assert wav_path in audio_paths_from_csv
