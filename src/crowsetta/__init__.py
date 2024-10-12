from . import examples, interface, typing, validation
from .__about__ import (
    __author__,
    __commit__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __uri__,
    __version__,
)
from .annotation import Annotation
from .bbox import BBox
from .examples._examples import example
from .segment import Segment
from .sequence import Sequence
from .transcriber import Transcriber

# Need to import formats last to avoid circular import errors
# isort: off
from . import formats
from .formats import register_format
from .formats.seq import AudSeq, BirdsongRec, GenericSeq, NotMat, SimpleSeq, Timit, SongAnnotationGUI
from .formats.bbox import AudBBox, Raven

# isort: on

__all__ = [
    "__author__",
    "__commit__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__uri__",
    "__version__",
    "Annotation",
    "AudBBox",
    "AudSeq",
    "BBox",
    "BirdsongRec",
    "GenericSeq",
    "NotMat",
    "Raven",
    "SimpleSeq",
    "Timit",
    "SongAnnotationGUI",
    "example",
    "examples",
    "formats",
    "interface",
    "register_format",
    "Segment",
    "Sequence",
    "Transcriber",
    "typing",
    "validation",
]
