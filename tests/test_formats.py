import crowsetta


def test_show(capsys):
    # make sure calling formats.show() gives us back some string
    crowsetta.formats.show()
    captured = capsys.readouterr()
    for format in crowsetta.formats._INSTALLED:
        # and that string should have the different formats in it somewhere
        assert format in captured.out
