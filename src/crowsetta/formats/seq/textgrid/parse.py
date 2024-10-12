"""Functions for parsing TextGrid files.

Code for parsing TextGrids is adapted from several sources,
all under MIT license.
The main logic in
:func:`~crowsetta.formats.seq.textgrid.parse.parse_fp`
is from <https://github.com/dopefishh/pympi>
which is perhaps the most concise
Python code I have found for parsing TextGrids.
However there are also good ideas in
https://github.com/kylebgorman/textgrid/blob/master/textgrid/textgrid.py
(__getitem__ method) and
https://github.com/timmahrt/praatIO
(data classes, handling encoding).
For some documentation of the binary format see
https://github.com/Legisign/Praat-textgrids
and for a citable library with docs see
https://github.com/hbuschme/TextGridTools
but note that both of these have a GPL license.
"""

from __future__ import annotations

import pathlib
import re
from typing import Final, TextIO

from .classes import Interval, IntervalTier, Point, PointTier

FLOAT_PAT: Final = re.compile(r"([\d.]+)\s*$", flags=re.UNICODE)
INT_PAT: Final = re.compile(r"([\d]+)\s*$", flags=re.UNICODE)
STR_PAT: Final = re.compile(r'"(.*)"\s*$', flags=re.UNICODE)


def search_next_line(fp: TextIO, pat: re.Pattern) -> str:
    """Get next line from a text stream
    and search it for a regex pattern.

    This is a helper function used by
    :func:`~crowsetta.textgrid.parse.get_float_from_line`,
    :func:`~crowsetta.textgrid.parse.get_int_from_line`,
    and :func:`~crowsetta.textgrid.parse.get_str_from_line`.

    Parameters
    ----------
    fp : TextIO
        Python text stream from an open TextGrid file.
    pat : re.Pattern
        A complied regex pattern.

    Returns
    -------
    match : str
        The match string
    """
    line = fp.readline()
    return pat.search(line).group(1)


def get_float_from_next_line(fp: TextIO) -> float:
    """Get next line from a text stream,
    search for a string that matches a float value,
    and return as a float.

    Helper function used by
    :func:`~crowsetta.textgrid.parse.parse_fp`,
    e.g., to parse ``xmin`` and ``xmax`` times of
    ``IntervalTier``s.

    Parameters
    ----------
    fp : TextIO
        Python text stream from an open TextGrid file.

    Returns
    -------
    val : float
    """
    return float(search_next_line(fp, pat=FLOAT_PAT))


def get_int_from_next_line(fp: TextIO) -> int:
    """Get next line from a text stream,
    search for a string that matches an int value,
    and return as an int.

    Helper function used by
    :func:`~crowsetta.textgrid.parse.parse_fp`,
    e.g., to parse the number of intervals in
    an interval tier.

    Parameters
    ----------
    fp : TextIO
        Python text stream from an open TextGrid file.

    Returns
    -------
    val : int
    """
    return int(search_next_line(fp, pat=INT_PAT))


def get_str_from_next_line(fp: TextIO) -> str:
    """Get next line from a text stream,
    search for a string as Praat writes them
    (with double quoting),
    and then return just that string.

    Helper function used by
    :func:`~crowsetta.textgrid.parse.parse_fp`,
    e.g., to parse ``text``s for ``Interval``s
    in ``IntervalTier``s or to parse ``text``
    for ``PointTier``s.

    Parameters
    ----------
    fp : TextIO
        Python text stream from an open TextGrid file.

    Returns
    -------
    val : str
    """
    # don't need to cast here
    return search_next_line(fp, pat=STR_PAT)


INTERVAL_TIER: Final = "IntervalTier"
POINT_TIER: Final = "TextTier"


def parse_fp(fp: TextIO, keep_empty: bool = False) -> dict:
    """Parse a TextGrid file passed in as an open
    text stream, converting it to a :class:`dict`.

    Helper function called by
    :func:`~crowsetta.formats.seq.textgrid.parse.parse`.

    Parameters
    ----------
    fp : TextIO
        Python text stream from an open TextGrid file.
    keep_empty : bool
        If True, keep intervals in
        interval tiers that have empty labels
        (i.e., the empty string "").
        Default is False.

    Returns
    -------
    tg : dict
        A parsed TextGrid as a :class:`dict:.
    """
    # Skip the Headers and empty line
    for _ in range(3):
        fp.readline()

    xmin_tg, xmax_tg = get_float_from_next_line(fp), get_float_from_next_line(fp)
    # We don't use next line except to determine format:
    # if it's just '<exists>' then format is "short", anything else is "full"
    line = fp.readline()
    is_short = line.strip() == "<exists>"

    n_tier = get_int_from_next_line(fp)
    if not is_short:
        # skip item[]:
        fp.readline()

    # make textgrid dict we will return below
    tg = {
        "xmin": xmin_tg,
        "xmax": xmax_tg,
    }

    tiers = []
    for _ in range(n_tier):
        if not is_short:
            fp.readline()  # skip item[\d]: (where \d is some number)
        tier_type = get_str_from_next_line(fp)
        tier_name = get_str_from_next_line(fp)
        xmin_tier = get_float_from_next_line(fp)
        xmax_tier = get_float_from_next_line(fp)

        entries = []  # intervals or points depending on tier type
        for _ in range(get_int_from_next_line(fp)):
            if not is_short:
                fp.readline()  # skip intervals [\d]
            if tier_type == INTERVAL_TIER:
                xmin = get_float_from_next_line(fp)
                xmax = get_float_from_next_line(fp)
                text = get_str_from_next_line(fp)
                if not keep_empty:
                    if text == "":
                        continue
                entry = Interval(xmin=xmin, xmax=xmax, text=text)
            elif tier_type == POINT_TIER:
                number = get_float_from_next_line(fp)
                mark = get_str_from_next_line(fp)
                entry = Point(
                    number=number,
                    mark=mark,
                )
            entries.append(entry)

        if tier_type == INTERVAL_TIER:
            tier = IntervalTier(name=tier_name, xmin=xmin_tier, xmax=xmax_tier, intervals=entries)
        elif tier_type == POINT_TIER:
            tier = PointTier(
                name=tier_name,
                xmin=xmin_tier,
                xmax=xmax_tier,
                points=entries,
            )

        tiers.append(tier)

    tg["tiers"] = tiers

    return tg


def parse(textgrid_path: str | pathlib.Path, keep_empty: bool = False) -> dict:
    """Parse a TextGrid file, loading it into a :class:`dict`.

    This function is used by
    :meth:`crowsetta.formats.seq.TextGrid.from_file`
    to load and parse the TextGrid file passed in
    as the ``annot_path`` argument.

    Parameters
    ----------
    textgrid_path : str, pathlib.Path
        The path to a TextGrid file.
    keep_empty : bool
        If True, keep intervals in
        interval tiers that have empty labels
        (i.e., the empty string "").
        Default is False.

    Returns
    -------
    textgrid_raw : dict
        A dict with keys 'xmin', 'xmax', and 'tiers'.
    """
    textgrid_path = pathlib.Path(textgrid_path)
    try:
        with textgrid_path.open("r", encoding="utf-16") as fp:
            textgrid_raw = parse_fp(fp, keep_empty)
    except UnicodeError:
        with textgrid_path.open("r", encoding="utf-8") as fp:
            textgrid_raw = parse_fp(fp, keep_empty)
    return textgrid_raw
