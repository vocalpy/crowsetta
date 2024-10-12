"""A class that represents a bounding box on a spectrogram,
drawn around animal communication or other sounds.
"""

import attrs
from attrs import field


def is_positive(self, attribute, value):
    if value < 0.0:
        raise ValueError("All input values must be positive")


@attrs.define
class BBox:
    """A class that represents a bounding box
    on a spectrogram,
    drawn around animal communication
    or other sounds.

    Attributes
    ----------
    onset : float
        Time of sound onset, typically in seconds.
    offset : float
        Time of sound offset, typically in seconds.
    low_freq : float
        Lowest frequency bounding sound, typically in Hz.
    high_freq : float
        Highest frequency bounding sound, typically in Hz.
    label : str
        string label that annotates bounding box

    Examples
    --------

    A toy example of a bounding box-like annotation.

    >>> bbox1 = crowsetta.BBox(label='Pinacosaurus grangeri', onset=1.0, offset=2.0, low_freq=3e3, high_freq=1e4)
    >>> bbox2 = crowsetta.BBox(label='Pinacosaurus grangeri', onset=3.0, offset=4.0, low_freq=3.25e3, high_freq=1.25e4)
    >>> bboxes = [bbox1, bbox2]
    >>> annot = crowsetta.Annotation(notated_path='prebird1.wav', annot_path='prebird1.csv', bboxes=bboxes)
    >>> print(annot)
    Annotation(annot_path=PosixPath('prebird1.csv'), notated_path=PosixPath('prebird1.wav'), bboxes=[BBox(onset=1.0, offset=2.0, low_freq=3000.0, high_freq=10000.0, label='Pinacosaurus grangeri'), BBox(onset=3.0, offset=4.0, low_freq=3250.0, high_freq=12500.0, label='Pinacosaurus grangeri')])  # noqa
    """

    onset: float = field(validator=is_positive)

    @onset.validator
    def lt_offset(self, attribute, value):
        if not value < self.offset:
            raise ValueError(
                "Bounding box onset must be less than offset." f"Onset was {value}, offset was {self.offset}"
            )

    offset: float = field(validator=is_positive)
    low_freq: float = field(validator=is_positive)

    @low_freq.validator
    def lt_high_freq(self, attribute, value):
        if not value < self.high_freq:
            raise ValueError(
                "Low frequency of bounding box must be less than high frequency."
                f"Low frequency was {value}, high frequency was {self.high_freq}"
            )

    high_freq: float = field(validator=is_positive)
    label: str
