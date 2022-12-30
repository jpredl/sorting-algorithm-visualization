from collections import namedtuple
from dataclasses import dataclass
import tkinter
import tkinter as tk


# Settings for VisualizationDiagram widget
@dataclass
class Settings:
    # width of slots
    width_of_slots: int = 10

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

    # color palette
    @dataclass
    class ColorPalette:
        background: str = 'white'
        slot_space_default_fill: str = ''
        slot_space_default_outline: str = ''
        slot_space_highlight_fill: str = 'gray'
        slot_space_highlight_outline: str = 'gray'
        slot_space_swap_fill: str = 'medium sea green'
        slot_space_swap_outline: str = 'medium sea green'
        slot_head_default_fill: str = 'black'
        slot_head_default_outline: str = 'black'
        slot_body_default_fill: str = 'sky blue'
        slot_body_default_outline: str = 'sky blue'
        slot_body_marked_fill: str = 'orange red'
        slot_body_marked_outline: str = 'orange red'
        focus_rectangle_outline: str = 'gainsboro'
        focus_rectangle_fill: str = 'gainsboro'


@dataclass
class DiagramSlot:
    space = None
    head = None
    body = None


Point = namedtuple('Point', 'x y')


class VisualizationDiagram(tk.Canvas):

    def __init__(self, master: tkinter.Widget, n: int):
        # number of slots
        self.number_of_slots: int = n

        # bottom left x slot positions (in cartesian coordinates)
        self.bottom_left_x_slot_position: int = [i * (Settings.width_of_slots + Settings.separation_between_slots)
                                            for i in range(self.number_of_slots)]

        # up right x slot positions (in cartesian coordinates)
        self.up_right_x_slot_position: int = [i * (Settings.width_of_slots + Settings.separation_between_slots) +
                                         Settings.width_of_slots for i in range(self.number_of_slots)]

        # diagram contains n slots
        self.slots: list[DiagramSlot] = []

        # horizontal offset for coordinates
        self.horizontal_offset: int = 3

        # vertical offset for coordinates
        self.vertical_offset: int = 2

        # width of widget
        self.width: int = Settings.horizontal_margin_left + self.number_of_slots * Settings.width_of_slots +\
                     (self.number_of_slots - 1) * Settings.separation_between_slots +\
                     Settings.horizontal_margin_right + 1

        # height of widget
        self.height: int = Settings.vertical_margin_top + (self.number_of_slots + 2) * Settings.width_of_slots +\
                      Settings.vertical_margin_bottom + 1

        # cartesian coordinates of point bottom left
        self.bottom_left: Point = Point(0, 0)

        # cartesian coordinates of point up right
        self.up_right: Point = Point(self.width - Settings.horizontal_margin_right - 1,
                              self.height - Settings.vertical_margin_top - Settings.vertical_margin_bottom - 1)

        # currently marked slot
        self.currently_marked_slot = None

        # currently highlighted slots
        self.currently_highlighted_slots = None

        # rectangle used to visualize focus
        self.focus_rectangle = None

        # initiate canvas widget
        tk.Canvas.__init__(self, master=master, width=self.width, height=self.height, background=Settings.ColorPalette.background)

    def _convert_cartesian_x_to_canvas_x(self, x: int) -> int:
        return Settings.horizontal_margin_left + self.horizontal_offset + x

    def _convert_cartesian_y_to_canvas_y(self, y: int) -> int:
        return self.height - Settings.vertical_margin_bottom + self.vertical_offset - y

    def _create_cartesian_rectangle(self, bottom_left: Point, up_right: Point,
                                    outline: str = 'black', fill: str = '') -> None:
        # create a rectangle using cartesian coordinates
        return tk.Canvas.create_rectangle(self, self._convert_cartesian_x_to_canvas_x(bottom_left.x),
                                          self._convert_cartesian_y_to_canvas_y(bottom_left.y),
                                          self._convert_cartesian_x_to_canvas_x(up_right.x),
                                          self._convert_cartesian_y_to_canvas_y(up_right.y),
                                          outline=outline, fill=fill)

    def _get_cartesian_bottom_left_x_coordinate_of_slot(self, pos: int) -> int:
        return pos * Settings.width_of_slots

    def setup_slots(self, heights):
        # clear diagram
        self.slots.clear()
        tk.Canvas.delete(self, 'all')

        # check if the number of provided heights is equal to the number of slots
        if len(heights) == self.number_of_slots:

            # create slots
            self.slots = [DiagramSlot() for _ in range(self.number_of_slots)]

            for i in range(self.number_of_slots):
                # create space of slot
                self.slots[i].space = self._create_cartesian_rectangle(
                    Point(self.bottom_left_x_slot_position[i], (heights[i] + 1) * Settings.width_of_slots),
                    Point(self.up_right_x_slot_position[i], self.up_right.y),
                    outline=Settings.ColorPalette.slot_space_default_outline,
                    fill=Settings.ColorPalette.slot_space_default_fill)

                # create head of slot
                self.slots[i].head = self._create_cartesian_rectangle(
                    Point(self.bottom_left_x_slot_position[i], heights[i] * Settings.width_of_slots),
                    Point(self.up_right_x_slot_position[i], (heights[i] + 1) * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_head_default_outline,
                    fill=Settings.ColorPalette.slot_head_default_fill)

                # create body of slot
                self.slots[i].body = self._create_cartesian_rectangle(
                    Point(self.bottom_left_x_slot_position[i], self.bottom_left.y),
                    Point(self.up_right_x_slot_position[i], heights[i] * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_body_default_outline,
                    fill=Settings.ColorPalette.slot_body_default_fill)


    def swap_slots(self, pos_1, pos_2):
        # if slots are setup
        if len(self.slots):

            # swap space of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].space, self.bottom_left_x_slot_position[pos_2] -
                           self.bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self.slots[pos_2].space, self.bottom_left_x_slot_position[pos_1] -
                           self.bottom_left_x_slot_position[pos_2], 0)

            # swap head of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].head, self.bottom_left_x_slot_position[pos_2] -
                           self.bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self.slots[pos_2].head, self.bottom_left_x_slot_position[pos_1] -
                           self.bottom_left_x_slot_position[pos_2], 0)

            # swap body of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].body, self.bottom_left_x_slot_position[pos_2] -
                           self.bottom_left_x_slot_position[pos_1], 0)
            tk.Canvas.move(self, self.slots[pos_2].body, self.bottom_left_x_slot_position[pos_1] -
                           self.bottom_left_x_slot_position[pos_2], 0)

            # swap slots in list of slots
            temp = self.slots[pos_1]
            self.slots[pos_1] = self.slots[pos_2]
            self.slots[pos_2] = temp

    def highlight_slots(self, pos_1, pos_2, swap=False):
        # if slots are setup
        if len(self.slots):

            # unhighlight currently highlighted slots
            self.unhighlight_slots()

            # determine color in regard if the highlight is for a swap
            outline = Settings.ColorPalette.slot_space_swap_outline if swap\
                else Settings.ColorPalette.slot_space_highlight_outline
            fill = Settings.ColorPalette.slot_space_swap_fill if swap \
                else Settings.ColorPalette.slot_space_highlight_fill

            # highlight slots at positions pos_1 and pos_2
            for pos in (pos_1, pos_2):
                tk.Canvas.itemconfig(self, self.slots[pos].space,
                                     outline=outline,
                                     fill=fill)

            # set currently highlighted slots
            self.currently_highlighted_slots = (self.slots[pos_1], self.slots[pos_2])


    def unhighlight_slots(self):
        # if slots are highlighted
        if self.currently_highlighted_slots:

            # unhighlight currently highlighted slots
            for slot in self.currently_highlighted_slots:
                tk.Canvas.itemconfig(self, slot.space,
                                     outline=Settings.ColorPalette.slot_space_default_outline,
                                     fill=Settings.ColorPalette.slot_space_default_fill)

            # set currently highlighted slots
            self.currently_highlighted_slots = None

    def mark_slot(self, pos: int):
        # if slots are setup
        if len(self.slots):

            # unmark currently marked slot
            self.unmark_slot()

            # mark slot at position pos
            tk.Canvas.itemconfig(self, self.slots[pos].body, outline=Settings.ColorPalette.slot_body_marked_outline,
                                 fill=Settings.ColorPalette.slot_body_marked_fill)

            # set currently marked slot
            self.currently_marked_slot = self.slots[pos]

    def unmark_slot(self):
        # if slots are marked
        if self.currently_marked_slot:

            # unmark currently marked slot
            tk.Canvas.itemconfig(self, self.currently_marked_slot.body,
                                 outline=Settings.ColorPalette.slot_body_default_outline,
                                 fill=Settings.ColorPalette.slot_body_default_fill)

            # set currently marked slot
            self.currently_marked_slot = None

    def focus_slots(self, pos_from, pos_to):
        # if slots are setup
        if len(self.slots):

            # unfocus currently focused slots
            self.unfocus_slots()

            # determine bottom left x and up right x coordinates of slots (in canvas coordinates)
            bottom_left_x = tk.Canvas.coords(self, self.slots[pos_from].body)[0]
            up_right_x = tk.Canvas.coords(self, self.slots[pos_to].space)[2]

            # create focus rectangle at positions from pos_from to pos_to
            self.focus_rectangle = tk.Canvas.create_rectangle(self, bottom_left_x,
                                                              self._convert_cartesian_y_to_canvas_y(self.bottom_left.y),
                                                              up_right_x,
                                                              self._convert_cartesian_y_to_canvas_y(self.up_right.y),
                                                              outline=Settings.ColorPalette.focus_rectangle_outline,
                                                              fill=Settings.ColorPalette.focus_rectangle_fill)

            # set focus rectangle to background
            tk.Canvas.tag_lower(self, self.focus_rectangle)

    def unfocus_slots(self):
        # if slots are focused
        if self.focus_rectangle:

            # unfocus currently focused slots
            tk.Canvas.delete(self, self.focus_rectangle)
            self.focus_rectangle = None