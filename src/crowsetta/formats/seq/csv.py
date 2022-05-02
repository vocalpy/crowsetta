import copy
from typing import ClassVar

from .generic import GenericSeq


class Csv(GenericSeq):
    """alias for GenericSeq, will be removed in next version"""
    name: ClassVar[str] = 'csv'
