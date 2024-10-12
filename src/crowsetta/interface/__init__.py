"""This module declares the interface for any class that
represents annotations for animal communication sounds
loaded from a file in a specific format."""

from .base import BaseFormat
from .bbox import BBoxLike
from .seq import SeqLike

__all__ = ["BaseFormat", "BBoxLike", "SeqLike"]
