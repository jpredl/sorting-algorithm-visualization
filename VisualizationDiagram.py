import tkinter as tk

from dataclasses import dataclass
from collections import namedtuple

# Settings for VisualizationDiagram widget
@dataclass
class Settings:
    # width of slots
    width_of_slots = 10

    # separation between slots
    separation_between_slots = 3

    # horizontal margin left
    horizontal_margin_left = 2

    # horizontal margin right
    horizontal_margin_right = 2

    # vertical margin top
    vertical_margin_top = 2

    # vertical margin bottom
    vertical_margin_bottom = 2

    # color palette
    @dataclass
    class ColorPalette:
        background = 'white'
        slot_space_default_fill = ''
        slot_space_default_outline = ''
        slot_space_highlight_fill = 'gray'
        slot_space_highlight_outline = 'gray'
        slot_space_swap_fill = 'medium sea green'
        slot_space_swap_outline = 'medium sea green'
        slot_head_default_fill = 'black'
        slot_head_default_outline = 'black'
        slot_body_default_fill = 'sky blue'
        slot_body_default_outline = 'sky blue'
        slot_body_marked_fill = 'orange red'
        slot_body_marked_outline = 'orange red'
        focus_rectangle_outline = 'gainsboro'
        focus_rectangle_fill = 'gainsboro'


@dataclass
class DiagramSlot:
    space = None
    head = None
    body = None


Point = namedtuple('Point', 'x y')


class VisualizationDiagram(tk.Canvas):

    def __init__(self, master, n):
        # number of slots
        self.number_of_slots = n

        # diagram contains n slots
        self.slots = []

        # horizontal offset for coordinates
        self.horizontal_offset = 3

        # vertical offset for coordinates
        self.vertical_offset = 2

        # width of widget
        self.width = Settings.horizontal_margin_left + self.number_of_slots * Settings.width_of_slots +\
                     (self.number_of_slots - 1) * Settings.separation_between_slots +\
                     Settings.horizontal_margin_right + 1

        # height of widget
        self.height = Settings.vertical_margin_top + (self.number_of_slots + 2) * Settings.width_of_slots +\
                      Settings.vertical_margin_bottom + 1

        # cartesian coordinates of point bottom left
        self.bottom_left = Point(0, 0)

        # cartesian coordinates of point up right
        self.up_right = Point(self.width - Settings.horizontal_margin_right - 1,
                              self.height - Settings.vertical_margin_top - Settings.vertical_margin_bottom - 1)

        # currently marked slot
        self.currently_marked_slot = None

        # currently highlighted slots
        self.currently_highlighted_slots = None

        # rectangle used to visualize focus
        self.focus_rectangle = None

        # initiate canvas widget
        tk.Canvas.__init__(self, master=master, width=self.width, height=self.height, background=Settings.ColorPalette.background)

    def convert_cartesian_x_to_canvas_x(self, x):
        return Settings.horizontal_margin_left + self.horizontal_offset + x

    def convert_cartesian_y_to_canvas_y(self, y):
        return self.height - Settings.vertical_margin_bottom + self.vertical_offset - y

    def create_cartesian_rectangle(self, bottom_left: Point, up_right: Point,
                                   outline: str = 'black', fill: str = ''):
        # create a rectangle using cartesian coordinates
        return tk.Canvas.create_rectangle(self, self.convert_cartesian_x_to_canvas_x(bottom_left.x),
                                          self.convert_cartesian_y_to_canvas_y(bottom_left.y),
                                          self.convert_cartesian_x_to_canvas_x(up_right.x),
                                          self.convert_cartesian_y_to_canvas_y(up_right.y),
                                          outline=outline, fill=fill)

    def get_cartesian_bottom_left_x_coordinate_of_slot(self, pos):
        return pos * Settings.width_of_slots

    def setup_bars(self, heights):
        # clear diagram
        self.slots.clear()
        tk.Canvas.delete(self, 'all')

        # check if the number of provided heights is equal to the number of slots
        if len(heights) == self.number_of_slots:

            # create slots
            self.slots = [DiagramSlot() for _ in range(self.number_of_slots)]

            for i in range(self.number_of_slots):
                # determine cartesian x coordinates
                bottom_left_x = i * (Settings.width_of_slots + Settings.separation_between_slots)
                up_right_x = i * (Settings.width_of_slots + Settings.separation_between_slots) + Settings.width_of_slots

                # create space of slot
                self.slots[i].space = self.create_cartesian_rectangle(
                    Point(bottom_left_x, (heights[i] + 1) * Settings.width_of_slots),
                    Point(up_right_x, self.up_right.y),
                    outline=Settings.ColorPalette.slot_space_default_outline,
                    fill=Settings.ColorPalette.slot_space_default_fill)

                # create head of slot
                self.slots[i].head = self.create_cartesian_rectangle(
                    Point(bottom_left_x, heights[i] * Settings.width_of_slots),
                    Point(up_right_x, (heights[i] + 1) * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_head_default_outline,
                    fill=Settings.ColorPalette.slot_head_default_fill)

                # create body of slot
                self.slots[i].body = self.create_cartesian_rectangle(
                    Point(bottom_left_x, self.bottom_left.y),
                    Point(up_right_x, heights[i] * Settings.width_of_slots),
                    outline=Settings.ColorPalette.slot_body_default_outline,
                    fill=Settings.ColorPalette.slot_body_default_fill)

    def swap_slots(self, pos_1, pos_2):
        # if slots are setup
        if len(self.slots):

            # highlight space of slots at position pos_1 and pos_2 for swapping
            self.highlight_slots(pos_1, pos_2, swap=True)

            # get current bottom left x coordinate of slots (in canvas coordinates)
            bottom_left_x_pos_1 = tk.Canvas.coords(self, self.slots[pos_1].space)[0]
            bottom_left_x_pos_2 = tk.Canvas.coords(self, self.slots[pos_2].space)[0]

            # swap space of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].space, bottom_left_x_pos_2 - bottom_left_x_pos_1, 0)
            tk.Canvas.move(self, self.slots[pos_2].space, bottom_left_x_pos_1 - bottom_left_x_pos_2, 0)

            # swap head of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].head, bottom_left_x_pos_2 - bottom_left_x_pos_1, 0)
            tk.Canvas.move(self, self.slots[pos_2].head, bottom_left_x_pos_1 - bottom_left_x_pos_2, 0)

            # swap body of slots on canvas
            tk.Canvas.move(self, self.slots[pos_1].body, bottom_left_x_pos_2 - bottom_left_x_pos_1, 0)
            tk.Canvas.move(self, self.slots[pos_2].body, bottom_left_x_pos_1 - bottom_left_x_pos_2, 0)

            # swap slots in list of slots
            temp = self.slots[pos_2]
            self.slots[pos_2] = self.slots[pos_1]
            self.slots[pos_1] = temp

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
                                                              self.convert_cartesian_y_to_canvas_y(self.bottom_left.y),
                                                              up_right_x,
                                                              self.convert_cartesian_y_to_canvas_y(self.up_right.y),
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