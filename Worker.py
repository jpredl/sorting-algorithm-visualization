import time
import threading

import Data
import Diagram
import SortingSteps


class Worker:

    def __init__(self, diagram: Diagram.Diagram, callback_on_no_next_step_available,
                 callback_on_update_comparison_count, callback_on_update_swap_count,
                 callback_on_update_replace_count, delay: float):
        # diagram used for visualization
        self._diagram: Diagram.Diagram = diagram

        # callback executed when no next step is available
        self._callback_on_no_next_step_available = callback_on_no_next_step_available

        # callback executed when a comparison is visualized
        self._callback_on_update_comparison_count = callback_on_update_comparison_count

        # callback executed when a swap is visualized
        self._callback_on_update_swap_count = callback_on_update_swap_count

        # callback executed when a replace is visualized
        self._callback_on_update_replace_count = callback_on_update_replace_count

        # delay for visualization
        self._delay: float = delay

        # thread for visualization
        self._thread: threading.Thread = None

        # data to be visualized
        self._data: Data.Data = None

        # comparisons visualized count
        self._comparison_count: int = 0

        # swaps visualized count
        self._swap_count: int = 0

        # replacements visualized count
        self._replace_count: int = 0

        # interrupt to stop thread
        self._stop_thread: bool = False

    def initiate_visualization(self, data: Data.Data):
        # setup data
        self._data = data
        self._comparison_count = 0
        self._swap_count = 0
        self._replace_count = 0

        # execute callback for comparison count
        self._callback_on_update_comparison_count(self._comparison_count)

        # execute callback for swap count
        self._callback_on_update_swap_count(self._swap_count)

        # execute callback for replace count
        self._callback_on_update_replace_count(self._replace_count)

        # setup bars in diagram
        self._diagram.create_slots(self._data.get_initial_data())

    def start_visualization(self):
        # if there are steps to visualize
        if self._data.next_step_available():
            # visualize steps in separate thread
            self._thread = threading.Thread(target=self._visualize_steps, daemon=True)
            self._stop_thread = False
            self._thread.start()

    def pause_visualization(self):
        # set interrupt of thread
        self._stop_thread = True

    def visualize_next_step(self):
        # visualize next step if it is available
        if self._data.next_step_available():
            # visualize next step in separate thread
            self._thread = threading.Thread(target=self._visualize_step,
                                            args=(self._data.get_next_step(),), daemon=True)
            self._thread.start()

            # if after this visualization there is no further next step
            if not self._data.next_step_available():
                self._finish_visualization()

    def set_delay(self, delay: float) -> None:
        self._delay = delay

    def _visualize_steps(self):
        # visualize steps while there are steps to visualize
        while self._data.next_step_available():
            # this flag stops the thread in which this method is running
            if self._stop_thread:
                break

            # visualize next step and wait
            if self._visualize_step(self._data.get_next_step()):
                time.sleep(self._delay)

        # if after this visualization there is no further next step
        if not self._data.next_step_available():
            self._finish_visualization()

    def _visualize_step(self, step: SortingSteps.Step) -> bool:
        # handle step
        match type(step):

            case SortingSteps.Comparison:
                # visualize comparison
                self._diagram.compare_slots(step)

                # increment comparison count
                self._comparison_count += 1

                # execute callback for comparison count
                self._callback_on_update_comparison_count(self._comparison_count)

            case SortingSteps.Swap:
                # visualize swap
                self._diagram.swap_slots(step)

                # increment swap count
                self._swap_count += 1

                # execute callback for swap count
                self._callback_on_update_swap_count(self._swap_count)

            case SortingSteps.Mark:
                # visualize mark
                self._diagram.mark_slot(step)

            case SortingSteps.Unmark:
                # visualize unmark
                self._diagram.unmark_slots()

            case SortingSteps.Focus:
                # visualize focus
                self._diagram.focus_slots(step)

            case SortingSteps.Unfocus:
                # visualize unfocus
                self._diagram.unfocus_slots()

            case SortingSteps.Replace:
                # visualize insert
                self._diagram.replace_slot(step)

                # increment replace count
                self._replace_count += 1

                # execute callback for replace count
                self._callback_on_update_replace_count(self._replace_count)

            case SortingSteps.Unreplace:
                # visualize uninsert
                self._diagram.unreplace_slots()

        return step.delay

    def _finish_visualization(self):
        # clean up visualization
        self._diagram.clean_slots()

        # execute callback for no next step available
        self._callback_on_no_next_step_available()
