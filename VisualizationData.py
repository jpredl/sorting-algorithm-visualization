

class VisualizationData:

    def __init__(self, initialization_algorithm, sorting_algorithm, n):
        # initial data
        self.initial_data = initialization_algorithm(n)

        # swaps
        self._steps = sorting_algorithm(self.initial_data.copy())

        # index for iterating swaps
        self._index = -1

    def get_next_step(self):
        if self.next_step_available():
            self._index += 1
            return self._steps[self._index]
        else:
            raise StopIteration

    def get_previous_steps(self):
        if self.previous_step_available():
            # return current step and then decrement index
            current_step = self._steps[self._index]
            self._index -= 1
            return current_step
        else:
            raise StopIteration

    def next_step_available(self):
        return True if self._index < len(self._steps) - 1 else False

    def previous_step_available(self):
        return True if self._index >= 0 else False

    def checkout_previous_step(self):
        if self.previous_step_available():
            return self._steps[self._index - 1]