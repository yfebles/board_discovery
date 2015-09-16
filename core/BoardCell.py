from kivy.properties import BooleanProperty
from kivy.uix.button import Button


class BoardCell(Button):
    """
    A board cell
    """

    NORMAL_BACKGROUND = 'assets\\images\\normal.png'
    SELECTED_BACKGROUND = 'assets\\images\\down.png'

    def __init__(self, row, col, level_item=None, **kwargs):
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
        self._visible = False

        # the selection state of the cell
        self._selected = False

        self.item_text = ""

        if level_item is not None:
            self.level_item = level_item

            self.item_text = level_item.name
            self.active = self.level_item.active
            self.visible = self.level_item.visible

        self.border = [30, 30, 30, 30]

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

        self.text = self.item_text if value else ""
        self.background_normal = self.NORMAL_BACKGROUND if value else ''

        if self.selected and not value:
            self.selected = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):

        self._selected = value

        self.background_normal = self.SELECTED_BACKGROUND if value else self.NORMAL_BACKGROUND