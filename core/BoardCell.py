from kivy.properties import BooleanProperty
from kivy.uix.button import Button


class BoardCell(Button):
    """
    A board cell
    """

    def __init__(self, row, col, level_item=None, **kwargs):
        """
        :param row: the row of the bard cell at the board
        :param col: the col of the bard cell at the board
        :param level_item: the inside level item that this widget wrap up
        :param kwargs: other buttons params
        :return:
        """
        Button.__init__(self, **kwargs)

        self.i, self.j = row, col

        self.text = str(row*col + 1)

        if level_item is not None:
            self.level_item = level_item

            self.text = level_item.name
            self.active = self.level_item.active
            self.visible = self.level_item.visible

