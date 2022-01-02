from pathlib import Path

import crowsetta

HERE = Path(__file__).parent
TEST_DATA = HERE.joinpath('..', 'data_for_tests')


def main():
    cbin_dir = TEST_DATA.joinpath('cbins/gy6or6/032312/')
    notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
    # below, sorted() so it's the same order on different platforms
    notmat_list = sorted(notmat_list)
    annot_list = crowsetta.notmat.notmat2annot(notmat_list)
    csv_filename = TEST_DATA.joinpath('csv/gy6or6_032312.csv')
    crowsetta.csv.annot2csv(csv_filename=csv_filename, annot=annot_list,
                            basename=True)

    module = str(HERE.joinpath('example.py'))
    config = {'module': module, 'from_file': 'example2annot'}
    scribe = crowsetta.Transcriber(format='example', config=config)
    mat_file = str(
        TEST_DATA.joinpath('example_user_format', 'bird1_annotation.mat')
    )
    csv_filename = str(
        TEST_DATA.joinpath('csv', 'example_annotation_with_onset_inds_offset_inds_None.csv')
    )
    scribe.to_csv(mat_file, csv_filename=csv_filename)


if __name__ == '__main__':
    main()