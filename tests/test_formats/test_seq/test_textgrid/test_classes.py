import pytest


import crowsetta.formats.seq.textgrid.classes


@pytest.mark.parametrize(
    'xmin, xmax, text',
    [
        (0., 0.3349812397, 'm'),
    ]
)
def test_Interval(xmin, xmax, text):
    interval = crowsetta.formats.seq.textgrid.classes.Interval(xmin, xmax, text)
    assert isinstance(interval, crowsetta.formats.seq.textgrid.classes.Interval)
    for attr_name, expected_attr_val in zip(
        ('xmin', 'xmax', 'text'),
        (xmin, xmax, text)
    ):
        assert hasattr(interval, attr_name)
        assert getattr(interval, attr_name) == expected_attr_val


@pytest.mark.parametrize(
    'xmin, xmax, text, expected_error',
    [
        # xmin > xmax
        (0.3349812397, 0, 'm', ValueError),
        # xmin is negative
        (-0.3, 0, 'm', ValueError),
        # xmax is negative
        (0., -0.3, 'm', ValueError),
    ]
)
def test_Interval_raises(xmin, xmax, text, expected_error):
    with pytest.raises(expected_error):
        crowsetta.formats.seq.textgrid.classes.Interval(xmin, xmax, text)


@pytest.mark.parametrize(
    'xmin, xmax, name, intervals',
    [
        (
            0.,
            2.3,
            'phones',
            [
                crowsetta.formats.seq.textgrid.classes.Interval(0., 0.35, 'fo'),
                crowsetta.formats.seq.textgrid.classes.Interval(0.35, 1.25, 'n'),
                crowsetta.formats.seq.textgrid.classes.Interval(1.25, 2.02, 's')
            ]
        )
    ]
)
def test_IntervalTier(xmin, xmax, name, intervals):
    interval_tier = crowsetta.formats.seq.textgrid.classes.IntervalTier(
        xmin=xmin, xmax=xmax, name=name, intervals=intervals)
    for attr_name, expected_attr_val in zip(
        ('xmin', 'xmax', 'name', 'intervals'),
        (xmin, xmax, name, intervals)
    ):
        assert hasattr(interval_tier, attr_name)
        assert getattr(interval_tier, attr_name) == expected_attr_val


@pytest.mark.parametrize(
    'xmin, xmax, name, intervals, expected_error',
    [
        (
            0.,
            2.3,
            'phones',
            # intervals overlap, should raise error
            [
                crowsetta.formats.seq.textgrid.classes.Interval(0., 0.35, 'fo'),
                crowsetta.formats.seq.textgrid.classes.Interval(0.1, 1.25, 'n'),
                crowsetta.formats.seq.textgrid.classes.Interval(1.23, 2.02, 's')
            ],
            ValueError
        )
    ]
)
def test_IntervalTier_raises(xmin, xmax, name, intervals, expected_error):
    with pytest.raises(expected_error):
        crowsetta.formats.seq.textgrid.classes.IntervalTier(
            xmin=xmin, xmax=xmax, name=name, intervals=intervals)


@pytest.mark.parametrize(
    'number, mark',
    [
        (0., 'fo'),
        (0.35, 'n'),
        (1.25, 's')
    ]
)
def test_Point(number, mark):
    point = crowsetta.formats.seq.textgrid.classes.Point(number, mark)
    for attr_name, expected_attr_val in zip(
        ('number', 'mark'),
        (number, mark)
    ):
        assert hasattr(point, attr_name)
        assert getattr(point, attr_name) == expected_attr_val




@pytest.mark.parametrize(
    'xmin, xmax, name, points',
    [
        (
            0.,
            2.3,
            'phones',
            [
                crowsetta.formats.seq.textgrid.classes.Point(0., 'fo'),
                crowsetta.formats.seq.textgrid.classes.Point(0.35, 'n'),
                crowsetta.formats.seq.textgrid.classes.Point(1.25, 's')
            ]
        )
    ]
)
def test_PointTier(xmin, xmax, name, points):
    point_tier = crowsetta.formats.seq.textgrid.classes.PointTier(
        xmin=xmin, xmax=xmax, name=name, points=points)
    for attr_name, expected_attr_val in zip(
        ('xmin', 'xmax', 'name', 'points'),
        (xmin, xmax, name, points)
    ):
        assert hasattr(point_tier, attr_name)
        assert getattr(point_tier, attr_name) == expected_attr_val
