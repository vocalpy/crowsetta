import math
import re
from unittest.mock import mock_open, patch

import pytest

from crowsetta.formats.seq.textgrid.classes import IntervalTier, PointTier
import crowsetta.formats.seq.textgrid.parse


@pytest.fixture
def fp_factory():
    """Factory that returns a mocked open file ``fp``
    that will return a specified string when ``readline`` when
    ``fp.readline`` is called"""

    def _fp(readline):
        with patch('builtins.open', mock_open(read_data=readline)) as mock_file:
            with open('fake.TextGrid') as fp:
                return fp

    return _fp


@pytest.mark.parametrize(
    'readline, pat, expected_result',
    [
        # float
        ('xmin = 0 \n', re.compile('([\\d.]+)\\s*$'), '0'),
        ('xmax = 2.4360509767904546 \n', re.compile('([\\d.]+)\\s*$'), '2.4360509767904546'),
        # int
        ('size = 3 \n', re.compile('([\\d]+)\\s*$'), '3'),
        ('        points: size = 5 \n', re.compile('([\\d]+)\\s*$'), '5'),
        # string
        ('        class = "TextTier" \n', re.compile('"(.*)"\\s*$'), 'TextTier'),
        ('        name = "Tones" \n', re.compile('"(.*)"\\s*$'), 'Tones')
    ]
)
def test_search_next_line(readline, pat, expected_result, fp_factory):
    fp = fp_factory(readline)
    out = crowsetta.formats.seq.textgrid.parse.search_next_line(fp, pat)
    assert out == expected_result


@pytest.mark.parametrize(
    'readline, expected_result',
    [
        # float
        ('xmin = 0 \n', 0.0),
        ('xmax = 2.4360509767904546 \n', 2.4360509767904546),
    ]
)
def test_get_float_from_next_line(readline, expected_result, fp_factory):
    fp = fp_factory(readline)
    out = crowsetta.formats.seq.textgrid.parse.get_float_from_next_line(fp)
    assert isinstance(out, float)
    assert math.isclose(out, expected_result)


@pytest.mark.parametrize(
    'readline, expected_result',
    [
        # int
        ('size = 3 \n', 3),
        ('        points: size = 5 \n', 5),
    ]
)
def test_get_int_from_next_line(readline, expected_result, fp_factory):
    fp = fp_factory(readline)
    out = crowsetta.formats.seq.textgrid.parse.get_int_from_next_line(fp)
    assert isinstance(out, int)
    assert out == expected_result


@pytest.mark.parametrize(
    'readline, expected_result',
    [
        ('        class = "TextTier" \n', 'TextTier'),
        ('        name = "Tones" \n', 'Tones')
    ]
)
def test_get_str_from_next_line(readline, expected_result, fp_factory):
    fp = fp_factory(readline)
    out = crowsetta.formats.seq.textgrid.parse.get_str_from_next_line(fp)
    assert isinstance(out, str)
    assert out == expected_result


def test_parse_fp(a_parse_textgrid_path):
    try:
        with a_parse_textgrid_path.open("r", encoding="utf-16") as fp:
            out = crowsetta.formats.seq.textgrid.parse.parse_fp(fp)
    except (UnicodeError, UnicodeDecodeError):
        with a_parse_textgrid_path.open("r", encoding="utf-8") as fp:
            out = crowsetta.formats.seq.textgrid.parse.parse_fp(fp)

    assert isinstance(out, dict)
    for expected_key, expected_type in zip(
            ('xmin', 'xmax', 'tiers'), (float, float, list)
    ):
        assert expected_key in out
        assert isinstance(out[expected_key], expected_type)

    assert all(
        [isinstance(tier, (IntervalTier, PointTier)) for tier in out['tiers']]
    )


def test_parse_fp_keep_empty(a_textgrid_with_empty_intervals_path, keep_empty):
    try:
        with a_textgrid_with_empty_intervals_path.open("r", encoding="utf-16") as fp:
            out = crowsetta.formats.seq.textgrid.parse.parse_fp(fp, keep_empty)
    except (UnicodeError, UnicodeDecodeError):
        with a_textgrid_with_empty_intervals_path.open("r", encoding="utf-8") as fp:
            out = crowsetta.formats.seq.textgrid.parse.parse_fp(fp, keep_empty)

    tiers = [tier for tier in out['tiers'] if isinstance(tier, IntervalTier)]

    if keep_empty:
        assert any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )
    else:
        assert not any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )


def test_parse(a_parse_textgrid_path):
    out = crowsetta.formats.seq.textgrid.parse.parse(a_parse_textgrid_path)

    assert isinstance(out, dict)
    for expected_key, expected_type in zip(
            ('xmin', 'xmax', 'tiers'), (float, float, list)
    ):
        assert expected_key in out
        assert isinstance(out[expected_key], expected_type)

    assert all(
        [isinstance(tier, (IntervalTier, PointTier)) for tier in out['tiers']]
    )


def test_parse_keep_empty(a_textgrid_with_empty_intervals_path, keep_empty):
    out = crowsetta.formats.seq.textgrid.parse.parse(a_textgrid_with_empty_intervals_path, keep_empty)
    tiers = [tier for tier in out['tiers'] if isinstance(tier, IntervalTier)]

    if keep_empty:
        assert any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )
    else:
        assert not any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )
