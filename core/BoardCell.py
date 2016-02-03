import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.event import EventDispatcher
from kivy.graphics.vertex_instructions import Rectangle
from core.Sounds import Sounds


class BoardCell(Button, EventDispatcher):
    """
    A board cell
    """

    # region CONSTANTS

    DESCP_SHOW_DELAY_TIME = 0.4
    IMG_PATH = os.path.join('assets', 'images', 'items')
    BORDER_IMAGE = os.path.join("assets", "images", "app_graphics", "board_btn_border.png")

    # endregion

    def __init__(self, level_item, row=0, col=0, **kwargs):
        """
        :param row: the row of the bard cell at the board
        :param col: the col of the bard cell at the board
        :param level_item: the inside level item that this widget wrap up
        :param kwargs: other buttons params
        :return:
        """
        Button.__init__(self, **kwargs)
        super(EventDispatcher, self).__init__(**kwargs)

        self.row, self.col = row, col

        self.unlocked_action = None

        # visibility, active and selection state of the cell
        self._visible, self.locked = False, False

        self.flip_animation = None

        self.vibrate_animation = None

        self.level_item = level_item

        self.item_image_canvas_instruction = []

    def on_animation_ended(self):
        """
        Event raised when a board cell animation has ended
        :return:
        """
        pass

    # region visible, name, image and description properties

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if self._visible == value:
            return

        if self.locked:
            return

        self._visible = value

        self.flip()

    @property
    def name(self):
        return self.level_item.name

    @property
    def description(self):
        descp = self.level_item.description

        return "" if descp is None else descp

    @property
    def image(self):
        return os.path.join(self.IMG_PATH, "" if not self.level_item.image else self.level_item.image)

    # endregion

    def release_animation(self, obj=None, button=None):
        self.locked = False

        if self.unlocked_action is not None:
            self.unlocked_action()
            self.unlocked_action = None

    def between_flip_change(self, obj=None, button=None):
        if self.visible:
            for instruction in self.item_image_canvas_instruction:
                self.canvas.after.add(instruction)
        else:
            self.canvas.after.clear()

    def flip(self):
        if self.locked:
            raise Exception("Invalid Operation on lock")

        self.locked = True

        old_x = self.pos[0]
        old_width = self.size_hint_x

        self.item_image_canvas_instruction = []
        shift_pos = self.pos[0] - self.width * 0.02, self.pos[1] - self.height * 0.02
        scaled_size = self.size[0] * 1.04, self.size[1] * 1.04
        self.item_image_canvas_instruction.append(Rectangle(source=self.image, pos=shift_pos, size=scaled_size))

        self.flip_animation = Animation(size_hint_x=0, x=old_x + self.width / 2, duration=self.DESCP_SHOW_DELAY_TIME / 2)

        self.flip_animation.bind(on_complete=self.between_flip_change)

        self.flip_animation += Animation(size_hint_x=old_width, x=old_x, duration=self.DESCP_SHOW_DELAY_TIME / 2)
        self.flip_animation.bind(on_complete=self.release_animation)

        self.flip_animation.start(self)

        Sounds().play_cell_flip_sound()

