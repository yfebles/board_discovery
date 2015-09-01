from core.BoardCell import BoardCell
from kivy.uix.gridlayout import GridLayout


class Board(GridLayout):
    """
    An square board game
    """

    def __init__(self, columns=3, **kwargs):
        GridLayout.__init__(self, **kwargs)

        self.spacing = 2
        self.columns = columns

        self.board = [[BoardCell(i, j)
                       for j in xrange(self.columns)]
                      for i in xrange(self.columns)]

        for i in xrange(self.columns):
            for j in xrange(self.columns):
                self.add_widget(self.board[i][j])
                self.board[i][j].bind(on_press=self.change_next_ones)

    def change_next_ones(self, button):

        i, j = button.i, button.j

        if i - 1 >= 0:
            self.board[i-1][j].text = button.text

        if i + 1 < self.columns:
            self.board[i+1][j].text = button.text

        if j - 1 >= 0:
            self.board[i][j-1].text = button.text

        if j + 1 < self.columns:
            self.board[i][j+1].text = button.text