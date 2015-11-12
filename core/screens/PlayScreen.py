# -*- coding: utf-8 -*-

from math import sqrt

from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, Clock

from core.BoardCell import BoardCell
from core.levels.db_orm import DB
from core.levels.LevelManager import LevelManager
from core.DescriptionWidget import DescriptionWidget


class GameWinPopup(Popup):
    continue_playing_bttn = ObjectProperty()


class GameLosePopup(Popup):
    repeat_level_bttn = ObjectProperty()


class PlayScreen(Screen):

    # region WIDGETS

    board_widget = ObjectProperty()
    points_lbl = ObjectProperty()
    hints_lbl = ObjectProperty()

    help_button = ObjectProperty()

    time_lbl = ObjectProperty()
    time_box = ObjectProperty()
    time_color = ObjectProperty()
    time_button = ObjectProperty()

    # endregion

    TIME_FONT_RELATION = 0.8
    DESCP_SHOW_DELAY_TIME = 0.45

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        self.db = DB().get_db_session()
        self.level_manager = LevelManager()

        self.help_widget = DescriptionWidget()
        self.description_widget = DescriptionWidget()

        self.description_widget.size_hint = [0, 0]

        # animations
        self.show_descp_animation = Animation(size_hint_y=1, size_hint_x=1, duration=self.DESCP_SHOW_DELAY_TIME)
        self.hide_descp_animation = Animation(size_hint_y=0, size_hint_x=0, duration=self.DESCP_SHOW_DELAY_TIME)

        # self.hide_descp_animation.bind(on_complete=self.)

        # Config Vars
        self.sounds, self.effects, self.first_run = [True] * 3

        self.board = []
        self.game_paused = True
        self.cell_selected = None
        self.current_level = None

        self.lose_popup = GameLosePopup()
        self.lose_popup.pos = [self.width * 0.5, self.height * 0.5]
        self.lose_popup.repeat_level_bttn.bind(on_press=lambda obj: self.load_level(self.current_level))

        self.win_popup = GameWinPopup()
        self.win_popup.pos = [self.width * 0.5, self.height * 0.5]
        self.win_popup.continue_playing_bttn.bind(on_press=self.save_and_continue)

    # region Properties

    @property
    def points(self):
        return int(self.points_lbl.text)

    @points.setter
    def points(self, points):
        self.points_lbl.text = str(points)

    @property
    def hints(self):
        return 0

    @hints.setter
    def hints(self, hints_count):
        pass

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

        self.points = 0
        self.current_level = level
        self.time_sec = level.time_seg

        self.description_widget.clear()
        self.board_widget.clear_widgets()

        # items are a list of n**2 elements with n the size of the board
        cols = int(sqrt(len(level.items)))

        if cols < 2:
            raise Exception("The board must have at least 2x2 cells")

        self.board = [[] for _ in xrange(cols)]

        for i in xrange(cols):
            for j in xrange(cols):
                board_cell = BoardCell(i, j, level.items[i * cols + j])

                # board[i][j]
                self.board[i].append(board_cell)

                self.board_widget.add_widget(board_cell)
                board_cell.bind(on_press=self.cell_pressed)

        self.update_cells_positions()

    def update_cells_positions(self):
        # in % from 0 to 1
        spacing = 0.02

        cols = len(self.board)
        w, h = self.board_widget.width, self.board_widget.height

        for i in xrange(cols):
            for j in xrange(cols):
                board_cell = self.board[i][j]

                # updating the width and height on each cell including the spacing between them
                board_cell.size_hint = [(1.0 - spacing * (cols -1)) / cols, (1.0 - spacing * (cols -1)) / cols]

                x = self.board_widget.pos[0] + j * w / cols + spacing * w
                y = self.board_widget.pos[1] + i * h / cols + spacing * h

                board_cell.pos = x, y

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

    def cell_pressed(self, board_cell):
        if self.current_level is None or self.game_paused:
            return

        if board_cell.visible:
            self.description_widget.update(board_cell.name, board_cell.description, board_cell.image)
            self.show_descp_widget(board_cell.center)
            return

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

        columns = int(sqrt(len(self.current_level.items)))

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

    def play(self, dt=None):
        # dt is the arg supplied by the clock timer call
        self.game_paused = False

    def on_leave(self, *args):
        self.pause()

    def on_enter(self, *args):
        # if no level has been played
        # if self.current_level is None:
        #     self.load_next_level()

        if self.game_paused:
            Clock.schedule_once(self.play, 1)

    # endregion

    def help_button_pressed(self, bttn=None):
        self.load_level(self.level_manager.levels[0])

    def show_descp_widget(self, pos):
        """
        Shows the descp widget on the position supplied
        :param pos: tuple of pos_x, pos_y
        :return:
        """

        if self.description_widget in self.board_widget.children:
            return

        self.description_widget.pos = pos
        self.board_widget.add_widget(self.description_widget)

        show_animation = Animation(x=self.board_widget.pos[0], y=self.board_widget.pos[1], duration=self.DESCP_SHOW_DELAY_TIME)
        show_animation &= self.show_descp_animation
        show_animation.start(self.description_widget)

    def hide_descp_widget(self):
        if self.description_widget not in self.board_widget.children:
            return

        self.hide_descp_animation.start(self.description_widget)

    def update_(self):
        self.board_widget.remove_widget(self.description_widget)
        self.description_widget.pos = self.board_widget.pos

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
