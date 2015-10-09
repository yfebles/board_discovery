from kivy.properties import ObjectProperty, Clock
from kivy.uix.screenmanager import Screen
from math import sqrt
from core.BoardCell import BoardCell
from core.Configs import Config
from core.levels.LevelManager import LevelManager


class PlayScreen(Screen):

    # region WIDGETS

    board_widget = ObjectProperty()
    # lives_lbl = ObjectProperty()
    points_lbl = ObjectProperty()
    hints_lbl = ObjectProperty()
    time_lbl = ObjectProperty()

    # endregion

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        # the level currently being played
        self.current_level = None

        self.register_event_type('on_game_ended')

        self.level_manager = LevelManager()

        self.app_configs = Config()

        self.game_paused = False

        self.board_widget.cols = 3
        self.board = [[]]

        # the cell to selected by user
        self.cell_selected = None

        self.load_level(self.level_manager.next_level)

    # region Board Interaction

    def cell_pressed(self, board_cell):

        # the board has to be visible and a level must be loaded
        if not board_cell.visible or self.current_level is None:
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

            columns = self.board_widget.cols

            # the position in the relations level matrix
            cell_1_position = row_1 * columns + col_1
            cell_2_position = row_2 * columns + col_2

            # if the two cells are related
            if self.current_level.relations[cell_1_position][cell_2_position]:
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

        columns = self.board_widget.cols

        if i > 0:
            adjacent_cells.append((i - 1, j))

        if i < columns - 1:
            adjacent_cells.append((i + 1, j))

        if j > 0:
            adjacent_cells.append((i, j - 1))

        if j < columns - 1:
            adjacent_cells.append((i, j + 1))

        for cell in adjacent_cells:
            i, j = cell[0], cell[1]

            if not self.board[i][j].visible:

                self.board[i][j].visible = True

                self.points += self.current_level.points

                # just one cell discovered
                return

    # endregion

    # region Game Interaction

    def check_game_state(self):
        """
        checks if the game is finished or not.
        If game has been wined or lose raise the events accordingly
        :return:
        """
        # the game is wined if all the cells are visible
        all_visible = True

        columns = self.board_widget.cols

        for i in xrange(columns):
            for j in xrange(columns):
                all_visible = all_visible and self.board[i][j].visible

        if all_visible:
            self.dispatch("on_game_ended", True)

    def load_level(self, level):
        """
        Load into the play screen the data of the level supplied
        :param level: the level supplied (if any) else try to load the next
        un played level
        """

        self.current_level = level.clone()

        # self.lives_lbl.text = "3"
        self.hints = 3
        self.points = 0
        self.time_sec = 10
        self.board_widget.clear_widgets()

        cols = self.board_widget.cols

        # items are a list of n**2 elements with n the size of the board
        self.board_widget.cols = int(sqrt(len(level.items)))

        self.board = [[BoardCell(i, j, level.items[i * cols + j])
                       for j in xrange(cols)]
                      for i in xrange(cols)]

        for i in xrange(cols):
            for j in xrange(cols):
                self.board_widget.add_widget(self.board[i][j])

                self.board[i][j].bind(on_press=self.cell_pressed)

        self.resume_game()

    def pause_game(self):
        pass

    def resume_game(self):
        self.game_paused = False

        Clock.schedule_interval(self.update_time, 1)

    def on_game_ended(self, game_win):
        """
        event raised when the game has end in this level
        :return:
        """
        pass

    def game_end(self, game_win):
        # save the user points for the level

        if game_win:
            print("game wined")

            self.level_manager.save_level_points(self.points)

            self.dispatch("on_game_ended", True)
            return

        # ask for repeat level if lose
        repeat_level = False

        if repeat_level:
            # if true reload level
            self.load_level(self.current_level)
        else:
            self.dispatch("on_game_ended", True)

    # endregion

    # region Properties

    @property
    def points(self):
        return int(self.points_lbl.text)

    @points.setter
    def points(self, points):
        self.points_lbl.text = str(points)

    @property
    def hints(self):
        return int(self.hints_lbl.text)

    @hints.setter
    def hints(self, hints_count):
        self.hints_lbl.text = str(hints_count)

    @property
    def time_sec(self):
        # time label in format "00:00" min:sec
        time = self.time_lbl.text

        time_s = int(time[0:2]) * 60 + int(time[3:])

        return time_s

    @time_sec.setter
    def time_sec(self, time_sec_count):
        # time label in format "00:00" min:sec
        minutes = time_sec_count / 60
        seconds = time_sec_count % 60

        minutes_str = str(minutes) if minutes >= 10 else "0" + str(minutes)
        seconds_str = str(seconds) if seconds >= 10 else "0" + str(seconds)

        self.time_lbl.text = minutes_str + ":" + str(seconds_str)

    # endregion

    def update_time(self, dt):
        current_time = self.time_sec

        if current_time > 0:
            current_time -= 1

        self.time_sec = current_time

        if current_time == 0:
            self.game_end(False)

        return current_time > 0