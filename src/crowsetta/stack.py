import attr
from attr.validators import optional, instance_of

from .sequence import Sequence


@attr.s
class Stack:
    """class to represent multiple overlapping sequences that annotate the same file

    Attributes
    ----------
    seq_dict : dict
        that maps names to Sequences

    Notes
    -----
    Sequences are also added as attributes when you create an instance of a Stack.
    """
    seq_dict = attr.ib(validator=optional(instance_of(dict)), default=None)

    def __attrs_post_init__(self):
        for name, value in self.seq_dict.items():
            setattr(self, name, value)

    @classmethod
    def from_seqs(cls,
                  seq_list=None,
                  seq_dict=None):
        if seq_list is None and seq_dict is None:
            raise ValueError(
                "must provide either a list or a dictionary of Sequences"
            )

        if seq_list and seq_dict is None:
            if not all([type(seq) == Sequence for seq in seq_list]):
                raise TypeError("all elements in 'seq_list' must be of type Sequence")
            seq_key_val_pairs = [
                (f'seq{num + 1}', seq)
                for num, seq in enumerate(seq_list)
            ]
            seq_dict = dict(seq_key_val_pairs)

        elif seq_dict and seq_list is None:
            if not all([type(key) == str for key in seq_dict.keys()]):
                raise TypeError("all keys in seq_dict must be strings; these will be the "
                                "names of the sequences belonging to the stack")
            if not all([type(val) == Sequence for val in seq_dict.values()]):
                raise TypeError("all elements in 'seq_dict' must be of type Sequence")

        return cls(seq_dict=seq_dict)
