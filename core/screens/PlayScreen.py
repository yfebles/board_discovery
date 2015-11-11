# -*- coding: utf-8 -*-

from math import sqrt
from kivy.config import Config, ConfigParser
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.popup import Popup
from core.BoardCell import BoardCell
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, Clock
from core.levels.LevelManager import LevelManager
from core.levels.orm.db_orm import DB


class GameWinPopup(Popup):
    continue_playing_bttn = ObjectProperty()


class GameLosePopup(Popup):
    repeat_level_bttn = ObjectProperty()


class PlayScreen(Screen):

    # region WIDGETS

    board_widget = ObjectProperty()
    points_lbl = ObjectProperty()
    hints_lbl = ObjectProperty()

    time_lbl = ObjectProperty()
    time_button = ObjectProperty()
    time_box = ObjectProperty()
    time_color = ObjectProperty()

    item_name_lbl = ObjectProperty()
    item_descp_lbl = ObjectProperty()
    item_image = ObjectProperty()

    # endregion

    TIME_FONT_RELATION = 0.8

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        self.level_manager = LevelManager()

        self.db = DB().get_db_session()

        # the colors to put in the time label when the game moves on
        self.time_colors = []

        # Config Vars
        self.sounds = True
        self.effects = True
        self.first_run = True

        # the level currently being played
        self.current_level = None

        self.game_paused = True

        self.board = [[]]

        # the cell to selected by user
        self.cell_selected = None

        # region win & lose Popups

        self.lose_popup = GameLosePopup()
        self.lose_popup.pos = [self.width * 0.5, self.height * 0.5]
        self.lose_popup.repeat_level_bttn.bind(on_press=lambda obj: self.load_level(self.current_level))

        self.win_popup = GameWinPopup()
        self.win_popup.pos = [self.width * 0.5, self.height * 0.5]
        self.win_popup.continue_playing_bttn.bind(on_press=self.save_and_continue)

        # endregion

        # Clock.schedule_interval(self.update_time, 1)

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

    # region Level Handling

    def save_and_continue(self, obj):
        """
        save the data of the current level of play. Unlock the next levels
        and load the next one
        :return:
        """
        self.level_manager.save_points(self.current_level, self.points)

        self.load_next_level()

    def load_level(self, level):
        """
        Load into the play screen the data of the level supplied
        :param level: the level supplied (if any) else try to load the next
        un played level
        """

        self.current_level = level
        self.hints, self.points = 0, 0
        # self.time_sec = level.time_seg

        self.board_widget.clear_widgets()
        self.update_info_widget()

        # items are a list of n**2 elements with n the size of the board
        self.board_widget.cols = int(sqrt(len(level.items)))

        cols = self.board_widget.cols

        self.board = []

        for i in xrange(cols):
            self.board.append([])

            for j in xrange(cols):

                self.board[i].append(BoardCell(i, j, level.items[i * cols + j]))
                self.board[i][j].bind(on_press=self.cell_pressed)
                self.board_widget.add_widget(self.board[i][j])

    def load_next_level(self):
        next_level = self.level_manager.get_next_level(self.current_level)

        if next_level is None:
            self.clear_widgets()
            Clock.schedule_once(self.win_popup.open, timeout=1)

        self.load_level(next_level)

    # endregion

    # region Game Behavior

    def check_game_state(self):
        """
        checks if the game is finished or not.
        If game has been wined or lose raise the events accordingly
        :return:
        """
        # the game is wined if all the cells are visible
        columns = self.board_widget.cols

        all_visible = all([self.board[i][j].visible for i in xrange(columns) for j in xrange(columns)])

        if all_visible:
            # game win animation
            self.pause()

            Clock.schedule_once(self.win_popup.open, timeout=1)

    def update_info_widget(self, board_cell=None):

        name = "" if board_cell is None else board_cell.name
        description = "" if board_cell is None else board_cell.description
        image = "" if board_cell is None else board_cell.image

        self.item_name_lbl.text = name
        self.item_descp_lbl.text = description
        self.item_image.source = image

    def cell_pressed(self, board_cell):

        print(self.sounds, self.effects, self.first_run)

        if not board_cell.visible or self.current_level is None or self.game_paused:
            return

        self.update_info_widget(board_cell)

        # if no previous selection
        if self.cell_selected is None:

            board_cell.selected = True
            self.cell_selected = board_cell
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
            if self.current_level.are_connected(cell_1_position, cell_2_position):
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
        # directions up, down, left and right
        adjacent_cells = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

        columns = self.board_widget.cols

        for row, col in adjacent_cells:
            if 0 <= row < columns and 0 <= col < columns and not self.board[row][col].visible:
                self.points += self.current_level.points
                self.board[row][col].visible = True
                return

    # endregion

    # region Pause & Play

    def switch_pause_state(self):
        action = self.play if self.game_paused else self.pause
        action()

    def pause(self):
        self.game_paused = True
        self.time_button.text = ""
        self.time_button.font_size = min(self.time_box.width, self.time_box.height) * self.TIME_FONT_RELATION * 0.9

    def play(self, dt=None):
        # dt is the arg supplied by the clock timer call
        self.game_paused = False
        self.time_button.text = ""
        self.time_button.font_size = min(self.time_box.width, self.time_box.height) * self.TIME_FONT_RELATION

    def on_leave(self, *args):
        self.pause()

    def on_enter(self, *args):
        # if no level has been played
        # if self.current_level is None:
        #     self.load_next_level()

        if self.game_paused:
            Clock.schedule_once(self.play, 1)

    # endregion

    def update_time(self, dt):
        # if pause nothing to do
        if self.game_paused:
            return True

        current_time = self.time_sec - 1

        # the time has finished so the time has ended
        if current_time <= 0:
            self.pause()

            # game lose animation
            Clock.schedule_once(self.lose_popup.open, timeout=1)

        self.time_sec = current_time

        # always return true to keep alive the timer
        return True
