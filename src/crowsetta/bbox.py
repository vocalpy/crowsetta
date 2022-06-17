"""A class that represents a bounding box on a spectrogram,
drawn around animal communication or other sounds.
"""
import attrs
from attrs import field


def is_positive(self, attribute, value):
    if value < 0.:
        raise ValueError(
            'All input values must be positive'
        )


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
    """
    onset: float = field(validator=is_positive)
    @onset.validator
    def lt_offset(self, attribute, value):
        if not value < self.offset:
            raise ValueError(
                'Bounding box onset must be less than offset.'
                f'Onset was {value}, offset was {self.offset}'
            )

    offset: float = field(validator=is_positive)
    low_freq: float = field(validator=is_positive)
    @low_freq.validator
    def lt_high_freq(self, attribute, value):
        if not value < self.high_freq:
            raise ValueError(
                'Low frequency of bounding box must be less than high frequency.'
                f'Low frequency was {value}, high frequency was {self.high_freq}'
            )
    high_freq: float = field(validator=is_positive)
    label: str
