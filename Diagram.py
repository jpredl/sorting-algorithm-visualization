from collections import namedtuple
from dataclasses import dataclass
import tkinter as tk
import numpy as np

import SortingSteps


@dataclass
class Settings:

    # width of slots
    width_of_slots: int = 8

    # separation between slots
    separation_between_slots: int = 3

    # horizontal margin left
    horizontal_margin_left: int = 2

    # horizontal margin right
    horizontal_margin_right: int = 2

    # vertical margin top
    vertical_margin_top: int = 2

    # vertical margin bottom
    vertical_margin_bottom: int = 2

    @dataclass
    class ColorPalette:
        background: str = 'white'
        slot_space_default: str = ''
        slot_space_compare: str = 'gray70'
        slot_space_swap: str = 'medium sea green'
        slot_head_default: str = 'black'
        slot_body_default: str = 'sky blue'
        slot_body_mark: str = 'indian red'
        slot_body_replace: str = 'dark slate blue'
        focus_rectangle: str = 'gainsboro'


Point = namedtuple('Point', 'x y')


@dataclass
class DiagramSlot:
    space = None
    head = None
    body = None


class Diagram(tk.Canvas):

    def __init__(self, master: tk.Widget, n: int):
        # number of slots
        self._number_of_slots: int = n

        # horizontal offset for coordinates
        self._horizontal_offset: int = 3

        # vertical offset for coordinates
        self._vertical_offset: int = 2

        # width of widget
        self._width: int = Settings.horizontal_margin_left + self._number_of_slots * Settings.width_of_slots + \
                           (self._number_of_slots - 1) * Settings.separation_between_slots + \
                           Settings.horizontal_margin_right + 1

        # height of widget
        self._height: int = Settings.vertical_margin_top + (
                self._number_of_slots + 2) * Settings.width_of_slots + \
                            Settings.vertical_margin_bottom + 1

        # initiate canvas widget
        tk.Canvas.__init__(self, master=master, width=self._width, height=self._height)

        # cartesian coordinates of point bottom left
        self._bottom_left: Point = Point(0, 0)

        # cartesian coordinates of point up right
        self._up_right: Point = Point(self._width - Settings.horizontal_margin_right - 1,
                                      self._height - Settings.vertical_margin_top - Settings.vertical_margin_bottom - 1)

        # bottom left x slot positions (in cartesian coordinates)
        self._bottom_left_x_slot_position: list[int] = [
            i * (Settings.width_of_slots + Settings.separation_between_slots)
            for i in range(self._number_of_slots)]

        # up right x slot positions (in cartesian coordinates)
        self._up_right_x_slot_position: list[int] = [i * (Settings.width_of_slots + Settings.separation_between_slots) +
                                                     Settings.width_of_slots for i in range(self._number_of_slots)]

        # slots
        self._slots: list[DiagramSlot] = []

        # currently compared slots
        self._currently_compared_slots: list[DiagramSlot] = []

        # currently swapped slots
        self._currently_swapped_slots: list[DiagramSlot] = []

        # currently marked slots
        self._currently_marked_slots: list[DiagramSlot] = []

        # currently replaced slots
        self._currently_replaced_slots: list[DiagramSlot] = []

        # current focus rectangle
        self._focus_rectangle = None

    def create_slots(self, heights: np.ndarray) -> None:
        # clear diagram
        self._slots.clear()
        tk.Canvas.delete(self, 'all')

        # check if the number of provided heights is equal to the number of slots
        if len(heights) == self._number_of_slots:

            # create slots
            self._slots = [DiagramSlot() for _ in range(self._number_of_slots)]

            for i in range(self._number_of_slots):
                # create space of slot
                self._slots[i].space = self._create_cartesian_rectangle(
                    Point(self._bottom_left_x_slot_position[i], (heights[i] + 1) * Settings.width_of_slots),
                    Point(self._up_right_x_slot_position[i], self._up_right.y),
                    outline=Settings.ColorPalette.slot_space_default,
                    fill=Settings.ColorPalette.slot_space_default)

                # create head of slot
                self._slots[i].head = self._create_cartesian_rectangle(
                    Point(self._bottom_left_x_slot_position[i], heights[i] * Settings.width_of_slots),
                    Point(self._up_right_x_slot_position[i], (heights[i] + 1) * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_head_default,
                    fill=Settings.ColorPalette.slot_head_default)

                # create body of slot
                self._slots[i].body = self._create_cartesian_rectangle(
                    Point(self._bottom_left_x_slot_position[i], self._bottom_left.y),
                    Point(self._up_right_x_slot_position[i], heights[i] * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_body_default,
                    fill=Settings.ColorPalette.slot_body_default)

    def compare_slots(self, comparison: SortingSteps.Comparison) -> None:
        # colorize space of currently compared slots
        self._uncompare_slots()

        # colorize space of currently swapped slots
        self._unswap_slots()

        # colorize space of comparison
        self._colorize_slot_space(slot=self._slots[comparison.pos_1], color=Settings.ColorPalette.slot_space_compare)
        self._colorize_slot_space(slot=self._slots[comparison.pos_2], color=Settings.ColorPalette.slot_space_compare)

        # append slots to currently compared slots
        self._currently_compared_slots.append(self._slots[comparison.pos_1])
        self._currently_compared_slots.append(self._slots[comparison.pos_2])

    def swap_slots(self, swap: SortingSteps.Swap) -> None:
        # colorize space of current comparison
        self._uncompare_slots()

        # colorize space of current swap
        self._unswap_slots()

        # colorize space of swap
        self._colorize_slot_space(slot=self._slots[swap.pos_1], color=Settings.ColorPalette.slot_space_swap)
        self._colorize_slot_space(slot=self._slots[swap.pos_2], color=Settings.ColorPalette.slot_space_swap)

        # swap the slots
        self._swap_slots(pos_1=swap.pos_1, pos_2=swap.pos_2)

        # append slots to currently swapped slots
        self._currently_swapped_slots.append(self._slots[swap.pos_1])
        self._currently_swapped_slots.append(self._slots[swap.pos_2])

    def mark_slot(self, mark: SortingSteps.Mark) -> None:
        #
        if not mark.multiple:
            self.unmark_slots()

        # colorize body of slot
        self._colorize_slot_body(slot=self._slots[mark.pos], color=Settings.ColorPalette.slot_body_mark)

        # append slot to list of currently marked slots
        self._currently_marked_slots.append(self._slots[mark.pos])

    def unmark_slots(self) -> None:
        # unmark slots
        for slot in self._currently_marked_slots:
            self._colorize_slot_body(slot=slot, color=Settings.ColorPalette.slot_body_default)

        # clear list of currently marked slots
        self._currently_marked_slots.clear()

    def replace_slot(self, replace: SortingSteps.Replace):
        # unreplace slot
        self.unreplace_slots()

        # uncompare slots
        self._uncompare_slots()

        # unswap slots
        self._unswap_slots()

        # replace space of slot
        tk.Canvas.delete(self, self._slots[replace.pos].space)
        self._slots[replace.pos].space = self._create_cartesian_rectangle(
            Point(self._bottom_left_x_slot_position[replace.pos], (replace.height + 1) * Settings.width_of_slots),
            Point(self._up_right_x_slot_position[replace.pos], self._up_right.y),
            outline=Settings.ColorPalette.slot_space_default,
            fill=Settings.ColorPalette.slot_space_default)

        # replace head of slot
        tk.Canvas.delete(self, self._slots[replace.pos].head)
        self._slots[replace.pos].head = self._create_cartesian_rectangle(
            Point(self._bottom_left_x_slot_position[replace.pos], replace.height * Settings.width_of_slots),
            Point(self._up_right_x_slot_position[replace.pos], (replace.height + 1) * Settings.width_of_slots),
            outline=Settings.ColorPalette.slot_head_default,
            fill=Settings.ColorPalette.slot_head_default)

        # replace body of slot
        tk.Canvas.delete(self, self._slots[replace.pos].body)
        self._slots[replace.pos].body = self._create_cartesian_rectangle(
            Point(self._bottom_left_x_slot_position[replace.pos], self._bottom_left.y),
            Point(self._up_right_x_slot_position[replace.pos], replace.height * Settings.width_of_slots),
            outline=Settings.ColorPalette.slot_body_replace,
            fill=Settings.ColorPalette.slot_body_replace)

        # append slot to list of currently replaced slots
        self._currently_replaced_slots.append(self._slots[replace.pos])

    def unreplace_slots(self):
        # colorize body of currently replaced slots
        for slot in self._currently_replaced_slots:
            self._colorize_slot_body(slot=slot, color=Settings.ColorPalette.slot_body_default)

        # clear list of currently replaced slots
        self._currently_replaced_slots.clear()

    def focus_slots(self, focus: SortingSteps.Focus) -> None:
        # clean slots
        self.clean_slots()

        # create focus rectangle at positions from from_pos to to_pos
        self._focus_rectangle = tk.Canvas.create_rectangle(self, self._convert_cartesian_x_to_canvas_x(
            self._bottom_left_x_slot_position[focus.from_pos]),
                                                           self._convert_cartesian_y_to_canvas_y(self._bottom_left.y),
                                                           self._convert_cartesian_x_to_canvas_x(
                                                               self._up_right_x_slot_position[focus.to_pos]),
                                                           self._convert_cartesian_y_to_canvas_y(self._up_right.y),
                                                           outline=Settings.ColorPalette.focus_rectangle,
                                                           fill=Settings.ColorPalette.focus_rectangle)

        # set focus rectangle to background
        tk.Canvas.tag_lower(self, self._focus_rectangle)

    def unfocus_slots(self) -> None:
        # if slots are focused
        if self._focus_rectangle:
            # remove focus rectangle
            tk.Canvas.delete(self, self._focus_rectangle)
            self._focus_rectangle = None

    def clean_slots(self) -> None:
        # colorize space of current comparison
        self._uncompare_slots()

        # colorize space of current swap
        self._unswap_slots()

        # unmark slots
        self.unmark_slots()

        # unfocus slots
        self.unfocus_slots()

    def _uncompare_slots(self):
        # colorize space of currently compared slots
        for slot in self._currently_compared_slots:
            self._colorize_slot_space(slot=slot, color=Settings.ColorPalette.slot_space_default)

        # clear currently compared slots
        self._currently_compared_slots.clear()

    def _unswap_slots(self):
        # colorize space of current swap
        for slot in self._currently_swapped_slots:
            self._colorize_slot_space(slot=slot, color=Settings.ColorPalette.slot_space_default)

        # clear currently swapped slots
        self._currently_swapped_slots.clear()

    def _swap_slots(self, pos_1: int, pos_2: int) -> None:
        # if slots exist
        if self._slots[pos_1].space and self._slots[pos_2].space:
            # swap space of slots on canvas
            tk.Canvas.move(self, self._slots[pos_1].space, self._bottom_left_x_slot_position[pos_2] -
                           self._bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self._slots[pos_2].space, self._bottom_left_x_slot_position[pos_1] -
                           self._bottom_left_x_slot_position[pos_2], 0)

            # swap head of slots on canvas
            tk.Canvas.move(self, self._slots[pos_1].head, self._bottom_left_x_slot_position[pos_2] -
                           self._bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self._slots[pos_2].head, self._bottom_left_x_slot_position[pos_1] -
                           self._bottom_left_x_slot_position[pos_2], 0)

            # swap body of slots on canvas
            tk.Canvas.move(self, self._slots[pos_1].body, self._bottom_left_x_slot_position[pos_2] -
                           self._bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self._slots[pos_2].body, self._bottom_left_x_slot_position[pos_1] -
                           self._bottom_left_x_slot_position[pos_2], 0)

            # swap slots in list of slots
            temp = self._slots[pos_1]
            self._slots[pos_1] = self._slots[pos_2]
            self._slots[pos_2] = temp

    def _colorize_slot_body(self, slot: DiagramSlot, color: str) -> None:
        tk.Canvas.itemconfig(self, slot.body, outline=color, fill=color)

    def _colorize_slot_space(self, slot: DiagramSlot, color: str) -> None:
        tk.Canvas.itemconfig(self, slot.space, outline=color, fill=color)

    def _convert_cartesian_x_to_canvas_x(self, x: int) -> int:
        return Settings.horizontal_margin_left + self._horizontal_offset + x

    def _convert_cartesian_y_to_canvas_y(self, y: int) -> int:
        return self._height - Settings.vertical_margin_bottom + self._vertical_offset - y

    def _create_cartesian_rectangle(self, bottom_left: Point, up_right: Point,
                                    outline: str = 'black', fill: str = ''):
        # create a rectangle using cartesian coordinates
        return tk.Canvas.create_rectangle(self, self._convert_cartesian_x_to_canvas_x(bottom_left.x),
                                          self._convert_cartesian_y_to_canvas_y(bottom_left.y),
                                          self._convert_cartesian_x_to_canvas_x(up_right.x),
                                          self._convert_cartesian_y_to_canvas_y(up_right.y),
                                          outline=outline, fill=fill)
