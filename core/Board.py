from kivy.event import EventDispatcher
from core.BoardCell import BoardCell
from kivy.uix.gridlayout import GridLayout


class Board(GridLayout, EventDispatcher):
    """
    An square board game
    """

    # region SIGNALS

    # method called when the game has end raise True if win or False if lose
    game_end_result_callback = None

    # callback called when the user-board interaction
    #  generate points raise the points won (int)
    points_won_callback = None

    # endregion

    def __init__(self, columns=3, **kwargs):
        GridLayout.__init__(self, **kwargs)
        EventDispatcher.__init__(self, **kwargs)

        self.spacing = 2
        self.cols = columns
        self.size_hint = [0.95, 0.95]

        self.board = [[BoardCell(i, j)
                       for j in xrange(self.cols)]
                      for i in xrange(self.cols)]

        for i in xrange(self.cols):
            for j in xrange(self.cols):
                self.add_widget(self.board[i][j])
                print(i, j)
                self.board[i][j].bind(on_press=self.change_next_ones)

    def load_level(self, level):
        pass

    def end_game(self):
        pass

    def start_game(self):
        pass

    def pause_game(self):
        pass

    def change_next_ones(self, button):

        i, j = button.i, button.j

        if i - 1 >= 0:
            self.board[i-1][j].text = button.text

        if i + 1 < self.cols:
            self.board[i+1][j].text = button.text

        if j - 1 >= 0:
            self.board[i][j-1].text = button.text

        if j + 1 < self.cols:
            self.board[i][j+1].text = button.text