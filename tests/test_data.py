import pytest

import crowsetta


@pytest.mark.parametrize(
    'format, format_class',
    [
        ('birdsong-recognition-dataset', crowsetta.formats.seq.BirdsongRec),
        ('generic-seq', crowsetta.formats.seq.GenericSeq),
        ('notmat', crowsetta.formats.seq.NotMat),
        ('raven', crowsetta.formats.bbox.Raven),
        ('simple-seq', crowsetta.formats.seq.SimpleSeq),
        ('textgrid', crowsetta.formats.seq.TextGrid),
        ('timit', crowsetta.formats.seq.Timit),
    ]
)
def test_get(format,
             format_class):
    example = crowsetta.data.get(format)
    if format_class is crowsetta.formats.bbox.Raven:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path,
                                                    annot_col='Species')
    elif format_class is crowsetta.formats.seq.SimpleSeq:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path,
                                                    columns_map={'start_seconds': 'onset_s', 
                                                                 'stop_seconds': 'offset_s', 
                                                                 'name': 'label'},
                                                    read_csv_kwargs={'index_col': 0})
    else:
        with example.annot_path as annot_path:
            annot_instance = format_class.from_file(annot_path)
    assert isinstance(annot_instance, format_class)


def test_available_formats():
    formats_with_example_data_list = crowsetta.data.available_formats()
    assert isinstance(formats_with_example_data_list, list)
    for format in formats_with_example_data_list:
        assert format in crowsetta.formats.as_list()
