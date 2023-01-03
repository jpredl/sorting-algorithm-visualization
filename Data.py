import numpy as np

import SortingSteps


class Data:

    def __init__(self, initialization_algorithm, sorting_algorithm, n):
        # initial data
        self.initial_data: np.ndarray = initialization_algorithm(n)

        # swaps
        self._steps: list[SortingSteps.Step] = sorting_algorithm(self.initial_data.copy())

        # index for iterating swaps
        self._index: int = -1

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
