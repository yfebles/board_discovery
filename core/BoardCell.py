from kivy.uix.button import Button


class BoardCell(Button):
    """
    A board cell
    """

    def __init__(self, i, j, **kwargs):
        Button.__init__(self, **kwargs)

        self.i, self.j = i, j

        self.text = str(i*j + 1)