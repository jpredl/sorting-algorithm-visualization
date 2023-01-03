from dataclasses import dataclass


@dataclass
class Step:
    delay: bool


@dataclass
class Comparison(Step):
    pos_1: int
    pos_2: int


@dataclass
class Swap(Step):
    pos_1: int
    pos_2: int


@dataclass
class Mark(Step):
    pos: int
    multiple: bool


@dataclass
class Unmark(Step):
    pass


@dataclass
class Focus(Step):
    from_pos: int
    to_pos: int


@dataclass
class Unfocus(Step):
    pass