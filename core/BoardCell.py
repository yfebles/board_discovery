import os
from kivy.core.audio import SoundLoader
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.animation import Animation, AnimationTransition


class BoardCell(Button):
    """
    A board cell
    """

    # region CONSTANTS

    DESCP_SHOW_DELAY_TIME = 0.4
    IMG_PATH = os.path.join('assets', 'images', 'items')
    FLIP_SOUND = os.path.join('assets', 'sounds', 'flip_sound.wav')
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

        self.row, self.col = row, col

        # visibility, active and selection state of the cell
        self._visible, self._active, self._selected, self.animation_ongoing = [False] * 4

        self.flip_animation = None

        sound = SoundLoader.load(self.FLIP_SOUND)

        self.flip_sound = None if not sound else sound

        self.level_item = level_item

        self.item_image_canvas_instruction = []

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if self._visible == value:
            return

        self._visible = value
        if self.flip_sound and value:
            self.flip_sound.play()

        self.flip()

    # region Level Items Properties

    @property
    def name(self):
        return self.level_item.name

    @property
    def description(self):
        descp = self.level_item.description
        return "" if descp is None else descp

    @property
    def image(self):
        return os.path.join(self.IMG_PATH, "naranja.jpg" if not self.level_item.image else self.level_item.image)

    # endregion

    # region Future Use

    @property
    def active(self):
        return self._active

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    # endregion

    def release_animation(self, obj=None, button=None):
        self.animation_ongoing = False

    def between_flip_change(self, obj=None, button=None):
        if self.visible:
            for instruction in self.item_image_canvas_instruction:
                self.canvas.after.add(instruction)
        else:
            self.canvas.after.clear()

    def flip(self):
        if self.animation_ongoing:
            return

        self.animation_ongoing = True

        old_x = self.pos[0]
        old_width = self.size_hint_x

        self.item_image_canvas_instruction = []
        self.item_image_canvas_instruction.append(Rectangle(source=self.image, pos=self.pos, size=self.size))
        self.item_image_canvas_instruction.append(Rectangle(source=self.BORDER_IMAGE, pos=self.pos, size=self.size))

        self.flip_animation = Animation(size_hint_x=0, x=old_x + self.width / 2, duration=self.DESCP_SHOW_DELAY_TIME / 2)

        self.flip_animation.bind(on_complete=self.between_flip_change)

        self.flip_animation += Animation(size_hint_x=old_width, x=old_x, duration=self.DESCP_SHOW_DELAY_TIME / 2)
        self.flip_animation.bind(on_complete=self.release_animation)

        self.flip_animation.start(self)

