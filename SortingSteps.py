from dataclasses import dataclass


@dataclass
class Step:
    """
    Base class for a step in the sorting process.

    Attributes
    ----------
    delay: bool
        If True then there will be delay until the next step is visualized.
    """
    delay: bool


@dataclass
class Comparison(Step):
    """
    Data for a comparison step.

    Attributes
    ----------
    pos_1, pos_2: int
        Position of the slots that are compared.
    """
    pos_1: int
    pos_2: int


@dataclass
class Swap(Step):
    """
    Data for a swapping step.

    Attributes
    ----------
    pos_1, pos_2: int
        Position of the slots that are swapped.
    """
    pos_1: int
    pos_2: int


@dataclass
class Mark(Step):
    """
    Data for marking a slot.

    Attributes
    ----------
    pos: int
        Position of the slot that is marked.
    multiple: bool
        If True then multiple slots can be marked at the same time.
    """
    pos: int
    multiple: bool


@dataclass
class Unmark(Step):
    pass


@dataclass
class Focus(Step):
    """
    Data for focus step.

    Attributes
    ----------
    from_pos, to_pos: int
        The slots from from_pos up to to_pos will be focused.
    """
    from_pos: int
    to_pos: int


@dataclass
class Unfocus(Step):
    pass

@dataclass
class Replace(Step):
    """
    Data for replace step.

    Attributes
    ----------
    pos, height: int
        Slot at pos will be replaced by a slot with height height.

    """
    pos: int
    height: int

@dataclass
class Unreplace(Step):
    pass