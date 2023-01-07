import numpy as np

import Initiator
import Sorter
import SortingSteps



class Data:

    def __init__(self, initiator: Initiator.Initiator, sorter: Sorter.Sorter, n):
        # initial data
        self._initial_data: np.ndarray = initiator.initiate(n)

        # swaps
        self._steps: list[SortingSteps.Step] = sorter.sort(self._initial_data.copy())

        # index for iterating swaps
        self._index: int = -1

    def get_initial_data(self) -> np.ndarray:
        return self._initial_data

    def get_next_step(self) -> SortingSteps.Step:
        if self.next_step_available():
            self._index += 1
            return self._steps[self._index]

    def get_previous_steps(self) -> SortingSteps.Step:
        if self.previous_step_available():
            # return current step and then decrement index
            current_step = self._steps[self._index]
            self._index -= 1
            return current_step

    def next_step_available(self) -> bool:
        return True if self._index < len(self._steps) - 1 else False

    def previous_step_available(self) -> bool:
        return True if self._index >= 0 else False

    def checkout_previous_step(self) -> SortingSteps.Step:
        if self.previous_step_available():
            return self._steps[self._index - 1]
