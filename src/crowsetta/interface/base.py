import abc


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
    def from_file(cls) -> 'Self':
        """Loads an annotation from a file
        in a given format.
        """
        ...

    def to_annot(self) -> 'Union[crowsetta.Annotation,List[crowsetta.Annotation]]':
        """Converts the instance representing annotations
        loaded from a file into a `crowsetta.Annotation`
        or a list of `crowsetta.Annotation`s,
        that can be used to convert to other formats
        """
        ...
