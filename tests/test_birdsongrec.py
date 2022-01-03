"""test functions in birdsongrec module"""
import csv

import crowsetta


def test_birdsongrec2annot(birdsong_rec_xml_file,
                           birdsong_rec_wavpath):
    annots = crowsetta.birdsongrec.birdsongrec2annot(annot_path=birdsong_rec_xml_file,
                                                     concat_seqs_into_songs=True,
                                                     wavpath=birdsong_rec_wavpath)
    assert isinstance(annots, list)
    assert all([type(annot) == crowsetta.Annotation for annot in annots])


def test_birdsongrec2csv(tmp_path,
                         birdsong_rec_xml_file,
                         birdsong_rec_wavpath):
    # since birdsongrec2csv is basically a wrapper around
    # birdsongrec2seq and seq2csv,
    # and those are tested above and in other test modules,
    # here just need to make sure this function doesn't fail
    csv_filename = tmp_path / 'test.csv'
    crowsetta.birdsongrec.birdsongrec2csv(annot_path=birdsong_rec_xml_file,
                                          wavpath=birdsong_rec_wavpath,
                                          csv_filename=csv_filename,
                                          basename=True)
    # make sure file was created
    assert csv_filename.exists()

    # to be extra sure, make sure all .wav files filenames from are in csv
    filenames_from_csv = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filenames_from_csv.append(row['audio_path'])

    wav_list = sorted(birdsong_rec_wavpath.glob('*.wav'))
    wav_list = [wav_file.name for wav_file in wav_list]
    for wav_file in wav_list:
        assert(wav_file in filenames_from_csv)
