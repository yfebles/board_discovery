from kivy.animation import Animation
from kivy.event import EventDispatcher
from math import sqrt
from core.BoardCell import BoardCell
from kivy.uix.gridlayout import GridLayout


class Board(GridLayout, EventDispatcher):
    """
    An square board game
    """

    def __init__(self, columns=3, **kwargs):
        GridLayout.__init__(self, **kwargs)
        EventDispatcher.__init__(self, **kwargs)

        # register events
        self.register_event_type('on_game_ended')
        self.register_event_type('on_points_made')

        self.cols = columns
        self.board = [[]]

    def load_level(self, level):
        # items are a list of n**2 elements with n the size of the board
        self.cols = int(sqrt(len(level.items)))

        self.board = [[BoardCell(i, j, level.items[i*self.cols + j])
                       for j in xrange(self.cols)]
                      for i in xrange(self.cols)]

        for i in xrange(self.cols):
            for j in xrange(self.cols):
                self.add_widget(self.board[i][j])
                self.board[i][j].bind(on_press=self.cell_pressed)
                self.board[i][j].bind(on_press=self.a)

    def a(self, obj):
        self.dispatch("on_points_made", 10)

        w = obj.width

        b = Animation(duration=0.2, width=2*w) + Animation(duration=0.2, width=w)
        b.start(obj)

    # region EVENTS

    def on_game_ended(self, game_win):
        """
        Event raised when the game has ended
        raise a boolean True if win or False if lose
        :param game_win:
        :return:
        """
        pass

    def on_points_made(self, points):
        """
        Event raised when the user has earned some points
        raise an int with the points
        :param points:
        :return:
        """
        pass

    # endregion

    def cell_pressed(self, button):
        i, j = button.i, button.j

