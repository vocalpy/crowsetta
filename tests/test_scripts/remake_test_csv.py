from pathlib import Path

import crowsetta

HERE = Path(__file__)
TEST_DATA = HERE.parents[1].joinpath('test_data')


def main():
    cbin_dir = TEST_DATA.joinpath('cbins/gy6or6/032312/')
    notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
    # below, sorted() so it's the same order on different platforms
    notmat_list = sorted(notmat_list)
    annot_list = crowsetta.notmat.notmat2annot(notmat_list)
    csv_filename = TEST_DATA.joinpath('csv/gy6or6_032312.csv')
    crowsetta.csv.annot2csv(csv_filename=csv_filename, annot=annot_list,
                            basename=True)


if __name__ == '__main__':
    main()