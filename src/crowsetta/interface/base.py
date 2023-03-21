import abc
from typing import List, Union


class BaseFormat(abc.ABC):
    """An abstract base class
    that declares the interface
    for any sub-class that
    represents annotations
    loaded from a file
    in a specific format
    for annotating vocalizations.
    """

    @classmethod
    @abc.abstractmethod
    def from_file(cls) -> "Self":  # noqa: F821
        """Loads an annotation from a file
        in a given format.
        """
        ...

    # type hints here would cause circular imports if not strings
    # TODO: fix type hinting here (use stubs?)
    @abc.abstractmethod
    def to_annot(self) -> "Union[crowsetta.Annotation,List[crowsetta.Annotation]]":  # noqa: F821
        """Converts the instance representing annotations
        loaded from a file into a :class:`crowsetta.Annotation`
        or a :class:`list` of :class:`~crowsetta.Annotation` instances,
        that can be used to convert to other formats.
        """
        ...
