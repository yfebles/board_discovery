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

        # the current level data
        self.level = None

        # the cell to selected by user
        self.cell_selected = None

        # sounds for the user actions
        self.sound_ok = None
        self.sound_wrong = None

    def load_level(self, level):
        self.clear_widgets()

        self.level = level

        # items are a list of n**2 elements with n the size of the board
        self.cols = int(sqrt(len(level.items)))

        self.board = [[BoardCell(i, j, level.items[i*self.cols + j])
                       for j in xrange(self.cols)]
                      for i in xrange(self.cols)]

        for i in xrange(self.cols):
            for j in xrange(self.cols):
                self.add_widget(self.board[i][j])
                self.board[i][j].bind(on_press=self.cell_pressed)

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

    def check_game_state(self):
        """
        checks if the game is finished or not.
        If game has been wined or lose raise the events accordingly
        :return:
        """
        # the game is wined if all the cells are visible
        all_visible = True

        for i in xrange(self.cols):
            for j in xrange(self.cols):
                all_visible = all_visible and self.board[i][j].visible

        if all_visible:
            self.dispatch("on_game_ended", True)

    def cell_pressed(self, board_cell):

        # the board has to be visible and a level must be loaded
        if not board_cell.visible or self.level is None:
            return

        # if no previous selection
        if self.cell_selected is None:
            self.cell_selected = board_cell
            board_cell.selected = True
            return

        else:
            # check if the two cells are related
            row_1, col_1 = self.cell_selected.row, self.cell_selected.col
            row_2, col_2 = board_cell.row, board_cell.col

            # the position in the relations level matrix
            cell_1_position = row_1 * self.cols + col_1
            cell_2_position = row_2 * self.cols + col_2

            # if the two cells are related
            if self.level.relations[cell_1_position][cell_2_position]:
                self.discover_cells(row_1, col_1)
                self.discover_cells(row_2, col_2)

            self.cell_selected.selected = False
            self.cell_selected = None

        # check if the game has been wined
        self.check_game_state()

    def discover_cells(self, i, j):
        """
        Method that discover all the cells adjacent
        to the position supplied
        :param i: row of the cell to center the discovery in
        :param j: col of the cell to center the discovery in
        :return:
        """
        adjacent_cells = []

        if i > 0:
            adjacent_cells.append((i - 1, j))

        if i < self.cols - 1:
            adjacent_cells.append((i + 1, j))

        if j > 0:
            adjacent_cells.append((i, j - 1))

        if j < self.cols - 1:
            adjacent_cells.append((i, j + 1))

        for cell in adjacent_cells:
            if not self.board[cell[0]][cell[1]].visible:
                self.board[cell[0]][cell[1]].visible = True
                self.dispatch("on_points_made" ,self.level.points)
                return