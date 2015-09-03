from kivy.properties import BooleanProperty
from kivy.uix.button import Button


class BoardCell(Button):
    """
    A board cell
    """

    # If the cell is available to be used.
    active = BooleanProperty(True)

    visible = BooleanProperty(True)

    # background_img = ImageProperty(None)

    def __init__(self, i, j, **kwargs):
        Button.__init__(self, **kwargs)

        self.i, self.j = i, j

        self.text = str(i*j + 1)