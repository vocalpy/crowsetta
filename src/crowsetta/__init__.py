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

# --- need to import everything used by formats before importing formats
from . import (
    interface,
    typing,
    validation
)

from .transcriber import Transcriber
from .segment import Segment
from .sequence import Sequence
from .annotation import Annotation
from .meta import Meta
