import threading
import time

import Algorithms
import VisualizationData
import VisualizationDiagram


class VisualizationWorker:

    def __init__(self, diagram: VisualizationDiagram.VisualizationDiagram, callback_on_no_next_step_available,
                 callback_on_update_comparison_count, callback_on_update_swap_count, delay=0.25):
        # diagram used for visualization
        self._diagram: VisualizationDiagram.VisualizationDiagram = diagram

        # callback executed when no next step is available
        self._callback_on_no_next_step_available = callback_on_no_next_step_available

        # callback executed when a comparison is visualized
        self._callback_on_update_comparison_count = callback_on_update_comparison_count

        # callback executed when a swap is visualized
        self._callback_on_update_swap_count = callback_on_update_swap_count

        # delay for visualization
        self._delay = delay

        # thread for visualization
        self._thread = None

        # data to be visualized
        self._data: VisualizationData.VisualizationData = None

        # comparisons visualized count
        self._comparison_count = 0

        # swaps visualized count
        self._swap_count = 0

        # interrupt to stop thread
        self._stop_thread = False

    def initiate_visualization(self, data: VisualizationData.VisualizationData):
        # setup data
        self._data = data
        self._comparison_count = 0
        self._swap_count = 0

        # execute callback for comparison count
        self._callback_on_update_comparison_count(self._comparison_count)

        # execute callback for swap count
        self._callback_on_update_swap_count(self._swap_count)

        # setup bars in diagram
        self._diagram.setup_bars(self._data.initial_data)

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

    def visualize_next_step(self, stepwise):
        # visualize next step if it is available
        if self._data.next_step_available():
            # if stepwise is true visualize next step in separate thread
            step = self._data.get_next_step()
            if stepwise:
                self._thread = threading.Thread(target=self._visualize_step,
                                                args=(step,), daemon=True)
                self._thread.start()
            else:
                self._visualize_step(step)

            # increment comparison or swap count
            self.update_comparison_and_swap_count(step, 1)

            # if after this visualization there is no further next step
            if not self._data.next_step_available():
                self._finish_visualization()

    def _visualize_steps(self):
        # visualize steps while there are steps to visualize
        while self._data.next_step_available():
            # this flag stops the thread in which this method is running
            if self._stop_thread:
                break

            # visualize next step
            self.visualize_next_step(stepwise=False)

            # delay between steps
            time.sleep(self._delay)

    def _visualize_step(self, step):
        # handle step
        match type(step):
            case Algorithms.Comparison:
                self._diagram.highlight_slots(step.pos_1, step.pos_2)
            case Algorithms.Swap:
                self._diagram.swap_slots(step.pos_1, step.pos_2)
            case Algorithms.Mark:
                self._diagram.mark_slot(step.pos)
            case Algorithms.Focus:
                self._diagram.focus_slots(step.pos_1, step.pos_2)

    def _finish_visualization(self):
        # clean up visualization
        self.clean_up_visualization()

        # execute callback for no next step available
        self._callback_on_no_next_step_available()

    def clean_up_visualization(self):
        self._diagram.unhighlight_slots()
        self._diagram.unmark_slot()
        self._diagram.unfocus_slots()

    def update_comparison_and_swap_count(self, step, increment: int):
        # handle step
        match type(step):
            case Algorithms.Comparison:
                # decrement comparison count
                self._comparison_count += increment

                # execute callback for comparison count
                self._callback_on_update_comparison_count(self._comparison_count)

            case Algorithms.Swap:
                # update swap count
                self._swap_count += increment

                # execute callback for swap count
                self._callback_on_update_swap_count(self._swap_count)

    def set_delay(self, delay):
        self._delay = delay
