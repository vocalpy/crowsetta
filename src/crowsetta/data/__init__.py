"""Module that handles example data built into ``crowsetta``"""
from . import audbbox, audseq, birdsongrec, generic, notmat, raven, simple, textgrid, timit
from .data import ExampleAnnotFile, available_formats, extract_data_files, get

__all__ = [
    "audbbox",
    "audseq",
    "available_formats",
    "birdsongrec",
    "ExampleAnnotFile",
    "extract_data_files",
    "generic",
    "get",
    "notmat",
    "raven",
    "simple",
    "textgrid",
    "timit",
]
