"""Data classes used to represent components of TextGrids."""

from __future__ import annotations

import numpy as np
from attrs import define, field


def valid_time(instance, attribute, value):
    if not value >= 0.0:
        raise ValueError(f"{attribute} is a time and must be a non-negative number but was: {value}")


@define
class Interval:
    """Class representing an interval in an interval tier
    from a Praat TextGrid.

    Attributes
    ----------
    xmin: float
        Start time of interval, in seconds.
    xmax: float
        End time of interval, in seconds.
    text: str
        Label for interval.

    See Also
    --------
    :class:`~crowsetta.formats.seq.textgrid.classes.IntervalTier`.
    """

    xmin: float = field(validator=valid_time)
    xmax: float = field(validator=valid_time)
    text: str

    def __attrs_post_init__(self):
        if self.xmax < self.xmin:
            raise ValueError(f"xmax must be greater than xmin but xmax was {self.xmax} and xmin was {self.xmin}")


@define
class IntervalTier:
    """Class representing an *interval tier* in a Praat TextGrid.

    As described in the Praat documentation[1]_:

       An interval tier is a connected sequence of labelled intervals,
       with boundaries in between.

    Attributes
    ----------
    name: str
        A name given to the interval tier, e.g. "phonemes".
    xmin: float
        Start time of interval tier, in seconds.
    xmax: float
        End time of interval tier, in seconds.
    intervals: list
        A list of
        :class:`~crowsetta.formats.seq.textgrid.classes.Interval`
        instances.

    See Also
    --------
    :class:`~crowsetta.formats.seq.textgrid.classes.Interval`

    References
    ----------
    .. [^1]: https://www.fon.hum.uva.nl/praat/manual/TextGrid.html
    """

    name: str
    xmin: float = field(validator=valid_time)
    xmax: float = field(validator=valid_time)
    intervals: list[Interval]

    def __attrs_post_init__(self):
        if self.xmax < self.xmin:
            raise ValueError(f"xmax must be greater than xmin but xmax was {self.xmax} and xmin was {self.xmin}")

        # sort because (1) we want them in ascending order of xmin and
        # (2) we use this to check for overlap
        self.intervals = sorted(self.intervals, key=lambda interval: interval.xmin)

        xmax_lt_all_xmin = []
        for ind in range(len(self.intervals) - 1):
            xmax_lt_all_xmin.append(
                all([self.intervals[ind].xmax <= interval.xmin for interval in self.intervals[ind + 1 :]])  # noqa: E203
            )

        if not all(xmax_lt_all_xmin):
            have_overlap = [(ind, self.intervals[ind]) for ind in np.nonzero(xmax_lt_all_xmin)[0]]
            err_str = ""
            for has_overlap_ind, interval in have_overlap:
                overlaps_with = [
                    (overlaps_with_ind, self.intervals[overlaps_with_ind])
                    for overlaps_with_ind in range(has_overlap_ind + 1, len(self.intervals) - 1)
                    if not (self.intervals[has_overlap_ind].xmax <= self.intervals[overlaps_with_ind].xmin)
                ]
                err_str += (
                    f"Interval {has_overlap_ind} with xmin {interval.xmin} and xmax {interval.xmax} overlaps with "
                )
                for overlaps_with_ind, interval in overlaps_with:
                    err_str += f"interval {overlaps_with_ind} with xmin {interval.xmin} and xmax {interval.xmax}, "
                err_str = err_str[:-2] + ".\n"

            raise ValueError(
                "TextGrids with overlapping intervals are not valid.\n"
                "Found the following overlapping intervals:\n"
                f"{err_str}"
            )

    def __iter__(self):
        return iter(self.intervals)


@define
class Point:
    """Class representing a point in a point tier
    from a Praat TextGrid.

    Attributes
    ----------
    number: float
        Time of point, in seconds.
    mark: str
        Label for point.

    See Also
    --------
    :class:`~crowsetta.formats.seq.textgrid.classes.PointTier`.
    """

    number: float = field(validator=valid_time)
    mark: str


@define
class PointTier:
    """Class representing a *point tier* in a Praat TextGrid.

    As described in the Praat documentation[1]_:

       A point tier is a sequence of labelled points.

    Attributes
    ----------
    name: str
        A name given to the point tier, e.g. "stimulus onset".
    xmin: float
        Start time of IntervalTier, in seconds.
    xmax: float
        End time of IntervalTier, in seconds.
    points: list
        A list of
        :class:`~crowsetta.formats.seq.textgrid.classes.Point`
        instances.

    See Also
    --------
    :class:`~crowsetta.formats.seq.textgrid.classes.Point`

    References
    ----------
    .. [^1]: https://www.fon.hum.uva.nl/praat/manual/TextGrid.html
    """

    name: str
    xmin: float = field(validator=valid_time)
    xmax: float = field(validator=valid_time)
    points: list[Point]

    def __attrs_post_init__(self):
        if self.xmax < self.xmin:
            raise ValueError(f"xmax must be greater than xmin but xmax was {self.xmax} and xmin was {self.xmin}")

    def __iter__(self):
        return iter(self.points)
