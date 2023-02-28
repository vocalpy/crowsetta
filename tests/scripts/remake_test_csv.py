"""
remakes the .csv files used for testing the `'generic-seq'` format
"""
import sys
from pathlib import Path

import pandas as pd

import crowsetta

HERE = Path(__file__).parent
TEST_DATA = HERE.joinpath("..", "data_for_tests")


def remake_notmat_as_generic_seq_csv():
    cbin_dir = TEST_DATA.joinpath("cbins/gy6or6/032312/")
    notmat_paths = sorted(cbin_dir.glob("*.not.mat"))
    annots = [crowsetta.formats.seq.NotMat.from_file(notmat_path).to_annot() for notmat_path in notmat_paths]
    notmat_generic_seq = crowsetta.formats.seq.GenericSeq(annots=annots)
    csv_path = TEST_DATA / "csv" / "notmat_gy6or6_032312.csv"
    print(f"saving csv: {csv_path}")
    notmat_generic_seq.to_file(csv_path=csv_path, basename=True)


def remake_birdsongrec_as_generic_seq_csv():
    birdsongrec_dir = TEST_DATA / "birdsongrec" / "Bird0"
    birdsongrec_xml_file = birdsongrec_dir / "Annotation.xml"
    birdsongrec_wavpath = birdsongrec_dir / "Wave"
    birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(
        xml_path=birdsongrec_xml_file, wav_path=birdsongrec_wavpath, concat_seqs_into_songs=True
    )
    annots = birdsongrec.to_annot()
    generic_seq = crowsetta.formats.seq.GenericSeq(annots=annots)
    csv_path = TEST_DATA / "csv" / "birdsongrec_Bird0_Annotation.csv"
    print(f"saving csv: {csv_path}")
    generic_seq.to_file(csv_path=csv_path, basename=True)


def remake_timit_phn_as_generic_seq_csv():
    timit_kaggle_dir = TEST_DATA / "timit_kaggle" / "dr1-fvmh0"
    phn_paths = sorted(timit_kaggle_dir.glob("*.phn"))
    annots = [crowsetta.formats.seq.Timit.from_file(phn_path).to_annot() for phn_path in phn_paths]
    timit_generic_seq = crowsetta.formats.seq.GenericSeq(annots=annots)
    csv_path = TEST_DATA / "csv" / "timit-dr1-fvmh0-phn.csv"
    print(f"saving csv: {csv_path}")
    timit_generic_seq.to_file(csv_path=csv_path, basename=True)


def remake_example_custom_format_as_generic_seq_csv():
    example_custom_format_dir = TEST_DATA / "example_custom_format"
    sys.path.append(example_custom_format_dir)
    import example  # registers custom format using `crowsetta.formats.register_format`

    annot_path = example_custom_format_dir / "bird1_annotation.mat"
    scribe = crowsetta.Transcriber(format="example-custom-format")
    example_ = scribe.from_file(annot_path)
    annots = example_.to_annot()
    custom_format_generic_seq = crowsetta.formats.seq.GenericSeq(annots=annots)
    csv_path = TEST_DATA / "csv" / "example_custom_format.csv"
    print(f"saving csv: {csv_path}")
    custom_format_generic_seq.to_file(csv_path=csv_path, basename=True)


def remake_invalid_fields_in_header_csv(source_csv_path):
    df = pd.read_csv(source_csv_path)
    df["invalid"] = df["label"].copy()

    csv_path = TEST_DATA / "csv" / "invalid_fields_in_header.csv"
    print(f"saving csv: {csv_path}")
    df.to_csv(csv_path, index=False)


def remake_missing_fields_in_header_csv(source_csv_path):
    df = pd.read_csv(source_csv_path)
    df = df.drop(columns=["label"])

    csv_path = TEST_DATA / "csv" / "missing_fields_in_header.csv"
    print(f"saving csv: {csv_path}")
    df.to_csv(csv_path, index=False)


def remake_onset_s_column_but_no_offset_s_column_csv(source_csv_path):
    df = pd.read_csv(source_csv_path)
    df = df.drop(columns=["offset_s"])

    csv_path = TEST_DATA / "csv" / "onset_s_column_but_no_offset_s_column.csv"
    print(f"saving csv: {csv_path}")
    df.to_csv(csv_path, index=False)


def remake_onset_sample_column_but_no_offset_sample_column_csv(source_csv_path):
    df = pd.read_csv(source_csv_path)
    df = df.drop(columns=["offset_sample"])

    csv_path = TEST_DATA / "csv" / "onset_sample_column_but_no_offset_sample_column.csv"
    print(f"saving csv: {csv_path}")
    df.to_csv(csv_path, index=False)


def remake_no_onset_or_offset_column_csv(source_csv_path):
    df = pd.read_csv(source_csv_path)
    df = df.drop(columns=["onset_s", "offset_s"])

    csv_path = TEST_DATA / "csv" / "no_onset_or_offset_column.csv"
    print(f"saving csv: {csv_path}")
    df.to_csv(csv_path, index=False)


def main():
    print("""Re-generating .csv files to use for testing `'generic-seq'` schema""")
    remake_notmat_as_generic_seq_csv()
    remake_birdsongrec_as_generic_seq_csv()
    remake_timit_phn_as_generic_seq_csv()

    source_csv_path = TEST_DATA / "csv" / "notmat_gy6or6_032312.csv"
    remake_invalid_fields_in_header_csv(source_csv_path)
    remake_missing_fields_in_header_csv(source_csv_path)
    remake_onset_s_column_but_no_offset_s_column_csv(source_csv_path)
    remake_no_onset_or_offset_column_csv(source_csv_path)

    source_csv_path = TEST_DATA / "csv" / "timit-dr1-fvmh0-phn.csv"
    remake_onset_sample_column_but_no_offset_sample_column_csv(source_csv_path)


if __name__ == "__main__":
    main()
