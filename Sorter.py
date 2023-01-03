import numpy as np

import SortingSteps


class Sorter:
    steps = []

    @staticmethod
    def sort(data: np.ndarray) -> list[SortingSteps.Step]:
        return Sorter.steps

    @staticmethod
    def compare(data: np.ndarray, pos_1: int, pos_2: int, delay: bool = True) -> int:
        # append comparison step to steps
        Sorter.steps.append(SortingSteps.Comparison(pos_1=pos_1, pos_2=pos_2, delay=delay))

        # compare and return True if data[pos_1] is smaller than or equal to data[pos_2]
        return True if data[pos_1] <= data[pos_2] else False

    @staticmethod
    def swap(data: np.ndarray, pos_1: int, pos_2: int, delay: bool = True) -> None:
        # swap entries in data
        temp = data[pos_1]
        data[pos_1] = data[pos_2]
        data[pos_2] = temp

        # append swap step to steps
        Sorter.steps.append(SortingSteps.Swap(pos_1=pos_1, pos_2=pos_2, delay=delay))

    @staticmethod
    def mark(pos: int, multiple: bool = False, delay: bool = True) -> None:
        # append mark step to steps
        Sorter.steps.append(SortingSteps.Mark(pos=pos, multiple=multiple, delay=delay))

    @staticmethod
    def unmark(delay: bool = True) -> None:
        # append unmark step to steps
        Sorter.steps.append(SortingSteps.Unmark(delay=delay))

    @staticmethod
    def focus(from_pos: int, to_pos: int, delay: bool = True) -> None:
        # append focus step to steps
        Sorter.steps.append(SortingSteps.Focus(from_pos=from_pos, to_pos=to_pos, delay=delay))

    @staticmethod
    def unfocus(delay: bool = True) -> None:
        # append unmark step to steps
        Sorter.steps.append(SortingSteps.Unfocus(delay=delay))

