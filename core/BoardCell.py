import os
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button


class BoardCell(Button):
    """
    A board cell
    """

    SOUND_BRICKS = os.path.join('assets', 'sounds', 'broke_brick.wav')
    IMG_PATH = os.path.join('assets', 'images', 'items')
    NO_VISIBLE_BACKGROUND = os.path.join('assets', 'images', 'bricks.png')
    NORMAL_BACKGROUND = os.path.join('assets', 'images', 'normal.png')
    SELECTED_BACKGROUND = os.path.join('assets', 'images', 'down.png')

    def __init__(self, row, col, level_item=None, visible=False, selected=False, **kwargs):
        """
        :param row: the row of the bard cell at the board
        :param col: the col of the bard cell at the board
        :param level_item: the inside level item that this widget wrap up
        :param kwargs: other buttons params
        :return:
        """
        Button.__init__(self, **kwargs)

        self.row, self.col = row, col

        # the visibility state of the cell
        self._visible = visible

        # the selection state of the cell
        self._selected = selected

        self.item_text = ""

        self._animate_back_image_index = 0
        self.bricks_animation_images = [os.path.join('assets', 'images', 'brick_broke' + str(i) + '.png') for i in range(1,5)]

        self.sound = SoundLoader.load(self.SOUND_BRICKS)
        if self.sound:
            self.sound.volume = 0.2

        self.background_normal = self.NORMAL_BACKGROUND

        if level_item is not None:
            self.level_item = level_item

            self.item_text = level_item.name
            self.active = self.level_item.active
            self.visible = self.level_item.visible

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):

        if not value:
            self.background_normal = self.NO_VISIBLE_BACKGROUND

        if not self._visible and value:
            self._animate_back_image_index = 0
            Clock.schedule_interval(self.animate_back_image, 0.05)
            if self.sound:
                self.sound.play()

        self._visible = value

        if self.selected and not value:
            self.selected = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    def animate_back_image(self, dt):

        if self._animate_back_image_index == len(self.bricks_animation_images):
            self.background_normal = self.NORMAL_BACKGROUND
        else:
            self.background_normal = self.bricks_animation_images[self._animate_back_image_index]

        self._animate_back_image_index += 1

        return self._animate_back_image_index <= len(self.bricks_animation_images)


