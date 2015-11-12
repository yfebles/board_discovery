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

    # region CONSTANTS

    SOUND_BRICKS = os.path.join('assets', 'sounds', 'broke_brick.wav')
    IMG_PATH = os.path.join('assets', 'images', 'items')
    NO_VISIBLE_BACKGROUND = os.path.join('assets', 'images', 'bricks.png')
    NORMAL_BACKGROUND = os.path.join('assets', 'images', 'normal.png')
    SELECTED_BACKGROUND = os.path.join('assets', 'images', 'down.png')

    # endregion

    def __init__(self, row=0, col=0, level_item=None, visible=False, selected=False, **kwargs):
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

        # if the cell is active to be used
        self._active = True

        # the selection state of the cell
        self._selected = selected

        # self.sound = SoundLoader.load(self.SOUND_BRICKS)
        # if self.sound:
        #     self.sound.volume = 0.2

        # self.level_item = level_item

        self.visible = False

    def set_cell_content(self, obj):
        """
        Set the content of a cell after make it visible
        :param obj:
        :return:
        """
        if self.level_item.image:
            self.background_normal = os.path.join(self.IMG_PATH, self.level_item.image)
        else:
            self.text = self.level_item.name

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    # region Level Items Properties

    @property
    def name(self):
        return self.level_item.name

    @property
    def description(self):
        return self.level_item.description

    @property
    def image(self):
        return os.path.join(self.IMG_PATH, self.level_item.image)

    # endregion

    @property
    def active(self):
        return self.level_item.active

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value