"""Module for type hinting that is specific to ``crowsetta``"""

import os
import pathlib
import typing

PathLike = typing.Union[str, bytes, os.PathLike, pathlib.Path]
