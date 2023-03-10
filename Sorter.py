import numpy as np

import SortingSteps


class Sorter:
    """
    Base class for a sorting algorithm.

    Methods
    -------
    sort(data)
        Wrapper for sorting data. Returns list of steps of sorting processes.
    execute(data)
        This method should be overridden by the concrete sorting algorithm.
    """

    _steps = []

    def sort(self, data: np.ndarray) -> list[SortingSteps.Step]:
        # prepare new round of sorting
        Sorter._steps.clear()

        # sort data
        self.execute(data)

        # data is sorted now
        return Sorter._steps

    def execute(self, data: np.ndarray) -> None:
        pass

    @staticmethod
    def compare(data: np.ndarray, pos_1: int, pos_2: int, delay: bool = True) -> int:
        # append comparison step to steps
        Sorter._steps.append(SortingSteps.Comparison(pos_1=pos_1, pos_2=pos_2, delay=delay))

        # compare and return True if data[pos_1] is smaller than or equal to data[pos_2]
        return True if data[pos_1] <= data[pos_2] else False

    @staticmethod
    def swap(data: np.ndarray, pos_1: int, pos_2: int, delay: bool = True) -> None:
        # swap entries in data
        temp = data[pos_1]
        data[pos_1] = data[pos_2]
        data[pos_2] = temp

        # append swap step to steps
        Sorter._steps.append(SortingSteps.Swap(pos_1=pos_1, pos_2=pos_2, delay=delay))

    @staticmethod
    def mark(pos: int, multiple: bool = False, delay: bool = True) -> None:
        # append mark step to steps
        Sorter._steps.append(SortingSteps.Mark(pos=pos, multiple=multiple, delay=delay))

    @staticmethod
    def unmark(delay: bool = True) -> None:
        # append unmark step to steps
        Sorter._steps.append(SortingSteps.Unmark(delay=delay))

    @staticmethod
    def replace(data: np.ndarray, pos:int, height: int, delay: bool = True) -> None:
        # replace entry in data
        data[pos] = height

        # append replace step to steps
        Sorter._steps.append(SortingSteps.Replace(pos=pos, height=height, delay=delay))

    @staticmethod
    def unreplace(delay: bool = True) -> None:
        # append unreplace step to steps
        Sorter._steps.append(SortingSteps.Unreplace(delay=delay))


    @staticmethod
    def focus(from_pos: int, to_pos: int, delay: bool = True) -> None:
        # append focus step to steps
        Sorter._steps.append(SortingSteps.Focus(from_pos=from_pos, to_pos=to_pos, delay=delay))

    @staticmethod
    def unfocus(delay: bool = True) -> None:
        # append unfocus step to steps
        Sorter._steps.append(SortingSteps.Unfocus(delay=delay))

