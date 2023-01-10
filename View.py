from dataclasses import dataclass
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk

import Data
import Diagram
import Initiator
import SortingAlgorithms
import Worker

@dataclass
class Settings:
    '''
    Settings for View.

    ...

    Attributes
    ----------
    InitializationAlgorithms: dict[str, Initiator.Initiator]
        Name and a class instance of an initiator used for initializing the array that should be sorted.

    SortingAlgorithms: dict[str, Sorter.Sorter]
        Name and a class instance of a sorting algorithm.

    data_size: int
        Size of the array that should be sorted.

    speed
        Settings for the speed of the visualization and the associated scale widget.

    '''

    InitializationAlgorithms = {'Permutation': Initiator.PermutationInitiator(),
                                'Local': Initiator.LocalInitiator(),
                                'Transposition': Initiator.TranspositionInitiater(),
                                'Reverse': Initiator.ReverseInitiator(),
                                'Sorted': Initiator.SortedInitiator()}

    SortingAlgorithms = {'Selectionsort': SortingAlgorithms.SelectionSorter(),
                         'Heapsort': SortingAlgorithms.HeapSorter(),
                         'Insertionsort': SortingAlgorithms.InsertionSorter(),
                         'Shellsort': SortingAlgorithms.ShellSorter(),
                         'Bubblesort': SortingAlgorithms.BubbleSorter(),
                         'Shakersort': SortingAlgorithms.ShakerSorter(),
                         'Combsort': SortingAlgorithms.CombSorter(),
                         'Quicksort': SortingAlgorithms.QuickSorter(),
                         'Quicksort (Median)': SortingAlgorithms.MedianQuickSorter(),
                         'Quicksort (Random)': SortingAlgorithms.RandomQuickSorter(),
                         'Mergesort': SortingAlgorithms.MergeSorter(),
                         'Mergesort (Straight)': SortingAlgorithms.StraightMergeSorter(),
                         'Mergesort (Natural)': SortingAlgorithms.NaturalMergeSorter(),
                         'Radixsort': SortingAlgorithms.DecimalRadixSorter(),
                         'Radixsort (Binary)': SortingAlgorithms.BinaryRadixSorter()}

    data_size: int = 50

    @dataclass
    class Speed:
        scale_speed_from: int = 0
        scale_speed_to: int = 100
        scale_speed_default_value: int = 40
        speed_function = lambda x: np.exp(-0.07 * x)


class View(tk.Tk):
    '''
    Main window that holds all widgets and manages the control flow.
    '''

    def __init__(self, *args, **kwargs):
        # initiate Tk window
        tk.Tk.__init__(self, *args, **kwargs)

        # set window title
        self.title('Sorting Algorithm Visualization')

        # prevent window from being resized
        self.resizable(width=False, height=False)

        # frame for controls
        self.frame_controls = ttk.Frame(master=self)
        self.frame_controls.grid(row=0, column=0, sticky='N')

        # sorting bar diagram widget
        self.diagram: Diagram.Diagram = Diagram.Diagram(self, Settings.data_size)
        self.diagram.grid(row=0, column=1)

        # frame for initialization controls
        self.frame_initialization = ttk.LabelFrame(self.frame_controls, text='Initialization')
        self.frame_initialization.grid(row=0, column=0, sticky='WE', padx=(3, 0), pady=(3, 15))

        # frame for visualization controls
        self.frame_visualization = ttk.LabelFrame(self.frame_controls, text='Visualization')
        self.frame_visualization.grid(row=1, column=0, sticky='WE', padx=(3, 0), pady=(3, 15))

        # frame for analysis
        self.frame_analysis = ttk.LabelFrame(master=self.frame_controls, text='Anaylsis')
        self.frame_analysis.grid(row=2, column=0, sticky='WE', padx=(3, 0), pady=(3, 3))

        # label for choosing initialization algorithm
        self.label_initialization_algorithm = ttk.Label(master=self.frame_initialization, text='Data Initialization:')
        self.label_initialization_algorithm.grid(row=0, column=0, sticky='W')

        # option menu current value for choosing initialization algorithm
        self.option_menu_initialization_algorithms_current_value = tk.StringVar(master=self.frame_initialization,
                                                                                value=Settings.InitializationAlgorithms.keys().__iter__().__next__())

        # option menu for choosing initialization algorithm
        self.option_menu_initialization_algorithms = ttk.OptionMenu(self.frame_initialization,
                                                                    self.option_menu_initialization_algorithms_current_value,
                                                                    self.option_menu_initialization_algorithms_current_value.get(),
                                                                    *list(Settings.InitializationAlgorithms.keys()),
                                                                    command=self._on_click_button_initiate)
        self.option_menu_initialization_algorithms.grid(row=0, column=1, sticky='WE')

        # label for choosing sorting algorithm
        self.label_sorting_algorithm = ttk.Label(master=self.frame_initialization, text='Sorting Algorithm:')
        self.label_sorting_algorithm.grid(row=1, column=0, sticky=tk.W)

        # option menu current value for choosing sorting algorithm
        self.option_menu_sorting_algorithms_current_value = tk.StringVar(master=self.frame_initialization,
                                                                         value=Settings.SortingAlgorithms.keys().__iter__().__next__())

        # option menu for choosing sorting algorithm
        self.option_menu_sorting_algorithms = ttk.OptionMenu(self.frame_initialization,
                                                             self.option_menu_sorting_algorithms_current_value,
                                                             self.option_menu_sorting_algorithms_current_value.get(),
                                                             *list(Settings.SortingAlgorithms.keys()),
                                                             command=self._on_click_button_initiate)
        self.option_menu_sorting_algorithms.grid(row=1, column=1, sticky='WE')

        # initiate button
        self.button_initiate = ttk.Button(master=self.frame_initialization, text='Initiate',
                                          command=self._on_click_button_initiate)
        self.button_initiate.grid(row=2, column=1, sticky='WE')

        # label for speed scale
        self.label_speed = ttk.Label(self.frame_visualization, text='Visualization Speed:')
        self.label_speed.grid(row=0, column=0)

        # speed scale current value
        self.scale_speed_current_value = tk.DoubleVar(master=self.frame_visualization,
                                                      value=Settings.Speed.scale_speed_default_value)
        self.scale_speed_current_value.trace(mode='w', callback=self._on_change_scale_speed)

        # speed scale
        self.scale_speed = ttk.Scale(master=self.frame_visualization,
                                     from_=Settings.Speed.scale_speed_from,
                                     to=Settings.Speed.scale_speed_to,
                                     value=self.scale_speed_current_value.get(),
                                     variable=self.scale_speed_current_value,
                                     orient=tk.HORIZONTAL)
        self.scale_speed.grid(row=0, column=1)

        # start button
        self.button_start_resume = ttk.Button(master=self.frame_visualization, text='Start',
                                              command=self._on_click_button_start_resume)
        self.button_start_resume.grid(row=1, column=0, sticky='WE')

        # stop button
        self.button_pause = ttk.Button(master=self.frame_visualization, text='Stop',
                                       command=self._on_click_button_pause)
        self.button_pause.grid(row=2, column=0, sticky='WE')

        # next step button
        self.button_next_step = ttk.Button(master=self.frame_visualization, text='Next Step',
                                           command=self._on_click_button_next_step)
        self.button_next_step.grid(row=1, column=1, sticky='WE')

        # n label
        self.label_n = ttk.Label(master=self.frame_analysis, text=f'Data Size: {Settings.data_size}')
        self.label_n.grid(row=0, column=0, sticky='W')

        # comparison count label
        self.label_comparison_count = ttk.Label(master=self.frame_analysis, text='Comparisons: 0')
        self.label_comparison_count.grid(row=1, column=0, sticky='W')

        # swap count label
        self.label_swap_count = ttk.Label(master=self.frame_analysis, text='Swaps: 0')
        self.label_swap_count.grid(row=2, column=0, sticky='W')

        # replace count label
        self.label_replace_count = ttk.Label(master=self.frame_analysis, text='Replacements: 0')
        self.label_replace_count.grid(row=3, column=0, sticky='W')

        # visualization worker
        self.visualization_worker = Worker.Worker(self.diagram,
                                                  callback_on_no_next_step_available=self._on_no_next_step_available,
                                                  callback_on_update_comparison_count=self._on_update_comparison_count,
                                                  callback_on_update_swap_count=self._on_update_swap_count,
                                                  callback_on_update_replace_count=self._on_update_replace_count,
                                                  delay=Settings.Speed.speed_function(
                                                      self.scale_speed_current_value.get()))

        # initiate
        self._on_click_button_initiate()

    def _on_click_button_initiate(self, *args) -> None:
        # set gui status
        self.option_menu_initialization_algorithms.config(state='normal')
        self.option_menu_sorting_algorithms.config(state='normal')
        self.button_initiate.config(state='normal')
        self.button_start_resume.config(state='normal', text='Start')
        self.button_pause.config(state='disabled')
        self.button_next_step.config(state='normal')

        # initiate visualization
        self.visualization_worker.initiate_visualization(
            Data.Data(initiator=Settings.InitializationAlgorithms[
                self.option_menu_initialization_algorithms_current_value.get()],
                      sorter=Settings.SortingAlgorithms[
                          self.option_menu_sorting_algorithms_current_value.get()],
                      n=Settings.data_size))

    def _on_change_scale_speed(self, *args) -> None:
        # set delay of VisualizationWorker
        self.visualization_worker.set_delay(Settings.Speed.speed_function(self.scale_speed_current_value.get()))

    def _on_click_button_start_resume(self) -> None:
        # setup gui status
        self.option_menu_initialization_algorithms.config(state='disabled')
        self.option_menu_sorting_algorithms.config(state='disabled')
        self.button_initiate.config(state='disabled')
        self.button_start_resume.config(state='disabled')
        self.button_pause.config(state='normal')
        self.button_next_step.config(state='disabled')

        # start visualization
        self.visualization_worker.start_visualization()

    def _on_click_button_pause(self) -> None:
        # setup gui status
        self.option_menu_initialization_algorithms.config(state='normal')
        self.option_menu_sorting_algorithms.config(state='normal')
        self.button_initiate.config(state='normal')
        self.button_start_resume.config(state='normal', text='Resume')
        self.button_pause.config(state='disabled')
        self.button_next_step.config(state='normal')

        # pause visualization
        self.visualization_worker.pause_visualization()

    def _on_click_button_next_step(self) -> None:
        # visualize next step
        self.visualization_worker.visualize_next_step()

    def _on_no_next_step_available(self) -> None:
        # setup gui status
        self.option_menu_initialization_algorithms.config(state='normal')
        self.option_menu_sorting_algorithms.config(state='normal')
        self.button_initiate.config(state='normal')
        self.button_start_resume.config(state='disabled', text='Start')
        self.button_pause.config(state='disabled')
        self.button_next_step.config(state='disabled')

    def _on_update_swap_count(self, count: int) -> None:
        # display swap count in label
        self.label_swap_count.config(text=f'Swaps: {count}')

    def _on_update_comparison_count(self, count: int) -> None:
        # display comparison count in label
        self.label_comparison_count.config(text=f'Comparisons: {count}')
    def _on_update_replace_count(self, count: int) -> None:
        # display replace count in label
        self.label_replace_count.config(text=f'Replacements: {count}')
