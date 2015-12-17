# -*- coding: utf-8 -*-

import os
from math import sqrt
from kivy.uix.modalview import ModalView
from core.db_orm import DB
from kivy.uix.popup import Popup
from kivy.animation import Animation
from core.BoardCell import BoardCell
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from core.LevelManager import LevelManager
from kivy.properties import ObjectProperty, Clock
from core.DescriptionWidget import DescriptionWidget


class GameWinView(ModalView):
    continue_playing_bttn = ObjectProperty()


class GameLoseView(ModalView):
    repeat_level_bttn = ObjectProperty()


class PlayScreen(Screen):
    """
    In several methods an argument dt is supplied
    cause are methods called from a clock timer schedule
    """

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

    # region CONSTANTS

    TIME_FONT_RELATION = 0.7
    DESCP_SHOW_DELAY_TIME = 0.45

    CLOCK_SOUND = os.path.join('assets', 'sounds', 'clock.wav')
    FLIP_SOUND = os.path.join('assets', 'sounds', 'flip_sound.wav')
    CELLS_PAIRED_OK = os.path.join('assets', 'sounds', 'cell_paired_ok.wav')
    CELLS_PAIRED_WRONG = os.path.join('assets', 'sounds', 'cell_paired_wrong.wav')

    # endregion

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        self.db = DB().get_db_session()
        self.level_manager = LevelManager()

        self.help_widget, self.description_widget = [DescriptionWidget()] * 2

        self.description_widget.bind(on_hide=self.hide_descp_widget)
        self.description_widget.size_hint = [0, 0]

        # sounds
        self.flip_sound, self.cell_paired_ok_sound, self.cell_paired_wrong_sound, self.clock_sound = [None] * 4
        self.load_sounds()

        # animations
        self.show_descp_animation = Animation(size_hint_y=1, size_hint_x=1, duration=self.DESCP_SHOW_DELAY_TIME)
        self.hide_descp_animation = Animation(size_hint_y=0, size_hint_x=0, duration=self.DESCP_SHOW_DELAY_TIME)
        self.pause_animation = Animation(opacity=0, duration=0.8) + Animation(opacity=1, duration=0.8)

        self.hide_descp_animation.bind(on_complete=self.remove_descp_widget)
        self.pause_animation.repeat = True

        # Config Vars
        self.sounds, self.effects, self.first_run, self.game_paused = [True] * 4

        self.board = []
        self.cell_selected, self.second_cell_selected, self.current_level = [None] * 3

        self.pairing_cells_on_going = False

        # win and lose level animations widgets (Popups by now)
        self.lose_popup = GameLoseView()
        self.lose_popup.color = [0] * 4
        self.lose_popup.repeat_level_bttn.bind(on_press=lambda obj: self.load_level(self.current_level))

        self.win_popup = GameWinView()
        self.win_popup.color = [0] * 4
        self.win_popup.continue_playing_bttn.bind(on_press=self.save_and_continue)

        Clock.schedule_interval(self.update_time, timeout=1)

    def load_sounds(self):
        sounds = [SoundLoader.load(s) for s in [self.FLIP_SOUND, self.CLOCK_SOUND, self.CELLS_PAIRED_OK, self.CELLS_PAIRED_WRONG]]
        sound_flip_cell, sound_clock, sound_pair_ok , sound_pair_wrong = sounds

        self.flip_sound = None if not sound_flip_cell else sound_flip_cell
        self.cell_paired_ok_sound = None if not sound_pair_ok else sound_pair_ok
        self.cell_paired_wrong_sound = None if not sound_pair_wrong else sound_pair_wrong

        if sound_clock:
            self.clock_sound = sound_clock
            self.clock_sound.repeat = True

    def play_sound(self, sound):
        if self.sounds and sound:
            sound.play()

    def stop_sound(self, sound):
        if self.sounds and sound:
            sound.stop()

    # region Properties

    @property
    def columns(self):
        return 0 if self.current_level is None else int(sqrt(len(self.current_level.items)))

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
        if time_sec_count < 10 and self.clock_sound.state is not 'play':
            self.play_sound(self.clock_sound)

        # time label in format "00:00" min:sec
        minutes = time_sec_count / 60
        seconds = time_sec_count % 60

        minutes_str = str(minutes) if minutes >= 10 else "0" + str(minutes)
        seconds_str = str(seconds) if seconds >= 10 else "0" + str(seconds)

        self.time_lbl.text = minutes_str + ":" + str(seconds_str)

        # there is 4 images to show for time color changing
        index = time_sec_count * 4 / self.current_level.time_seg
        img_src = "display_color_time_box{0}.png".format(1 + index)

        if index < 4 and img_src != self.time_box.back_color_img:
            self.time_box.back_color_img = img_src

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

        cols = self.columns
        if cols < 2:
            raise Exception("The board must have at least 2x2 cells")

        self.points = 0
        self.time_sec = 15  # level.time_seg

        self.board_widget.clear_widgets()
        self.cell_selected, self.second_cell_selected = [None] * 2

        self.board = [[] for _ in xrange(cols)]

        for i in xrange(cols):
            for j in xrange(cols):
                board_cell = BoardCell(level.items[i * cols + j], i, j)

                # board[i][j]
                self.board[i].append(board_cell)

                self.board_widget.add_widget(board_cell)
                board_cell.bind(on_press=self.cell_pressed)
                board_cell.bind(on_flip=self.cell_flipped)

        self.update_cells_positions()
        self.hide_descp_widget()
        self.play()

    def update_cells_positions(self):
        cols = self.columns

        # spacing between cells in % from 0 to 1
        spacing = 0.02

        w, h = self.board_widget.width, self.board_widget.height
        x_base = self.board_widget.pos[0] + self.board_widget.width * spacing / 2
        y_base = self.board_widget.pos[1] + self.board_widget.height * spacing / 2

        for i in xrange(cols):
            for j in xrange(cols):
                board_cell = self.board[i][j]

                # updating the width and height on each cell including the spacing between them in % from 0 to 1 of the parent
                board_cell.size_hint = [(1.0 - spacing * (cols - 1)) / cols, (1.0 - spacing * (cols - 1)) / cols]

                board_cell.pos = x_base + j * w / cols, y_base + i * h / cols

    def load_next_level(self):
        next_level = self.level_manager.get_next_level(self.current_level)

        if next_level is None:
            # self.clear_widgets()
            Clock.schedule_once(self.win_popup.open, timeout=0.5)

        self.load_level(next_level)

    # endregion

    # region Game Behavior

    def cell_flipped(self, obj=None):
        """
        Callback for when a cell has been flipped
        :return:
        """
        self.play_sound(self.flip_sound)

    def check_game_state(self):
        """
        checks if the game is finished or not.
        If game has been wined or lose raise the events accordingly
        :return:
        """
        # the game is wined if all the cells are visible

        all_visible = all([self.board[i][j].visible
                           for i in xrange(self.columns)
                           for j in xrange(self.columns)])

        if all_visible:
            # game win animation
            self.pause()

            Clock.schedule_once(self.win_popup.open, timeout=1)

    def cell_pressed(self, board_cell):
        if self.pairing_cells_on_going or self.current_level is None or self.is_descp_visible():
            return

        if board_cell.visible:
            self.show_descp_widget(board_cell.center, board_cell)
            return

        if self.game_paused:
            return

        board_cell.visible = True

        # if no un-paired cell is visible (just visible the already paired)
        if self.cell_selected is None:
            self.cell_selected = board_cell
            return

        # if the two cells are not related hide them
        if not self.are_connected(self.cell_selected, board_cell):

            # play un-paired sound if must be
            if self.sounds and self.cell_paired_wrong_sound:
                self.cell_paired_wrong_sound.play()

            self.pairing_cells_on_going = True
            self.second_cell_selected = board_cell
            Clock.schedule_once(self.pair_cells_failed_restore, timeout=board_cell.DESCP_SHOW_DELAY_TIME * 1.5)
            return

        # play paired sound if must be
        if self.sounds and self.cell_paired_ok_sound:
            self.cell_paired_ok_sound.play()

        # if related cells
        self.points += self.current_level.points

        self.cell_selected = None

        # check if the game has been wined
        self.check_game_state()

    def are_connected(self, cell1, cell2):
        """
        Method that checks the connection between the two supplied cells
        on the current level
        :param cell1: The first Board Cell to check
        :param cell2: The second Board Cell to check
        :return: True if connected on the level False otherwise
        """
        # the indexed in the  level items list
        cell_1_index = cell1.row * self.columns + cell1.col
        cell_2_index = cell2.row * self.columns + cell2.col

        return self.current_level.are_connected(cell_1_index, cell_2_index)

    def pair_cells_failed_restore(self, obj=None):

        self.second_cell_selected.visible = False
        self.cell_selected.visible = False
        self.cell_selected = None

        self.pairing_cells_on_going = False

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

        for row, col in adjacent_cells:
            if 0 <= row < self.columns and 0 <= col < self.columns and not self.board[row][col].visible:
                self.points += self.current_level.points
                self.board[row][col].visible = True
                return

    # endregion

    # region Pause & Play

    def switch_pause_state(self):
        action = self.play if self.game_paused else self.pause
        action()

    def pause(self, dt=None):
        self.game_paused = True
        self.pause_animation.start(self.time_lbl)

        self.stop_sound(self.clock_sound)

    def play(self, dt=None):
        if self.time_sec <= 0:
            return

        self.pause_animation.cancel(self.time_lbl)
        self.time_lbl.opacity = 1
        self.game_paused = False

    def on_leave(self, *args):
        self.pause()

    def on_enter(self, *args):
        # if no level has been played
        if self.current_level is None:
            self.load_next_level()

        if self.game_paused and not self.is_descp_visible():
            Clock.schedule_once(self.play, 1)

    # endregion

    # region Description And Help

    def is_descp_visible(self):
        return self.description_widget in self.board_widget.children

    def help_button_pressed(self, bttn=None):
        pass

    def show_descp_widget(self, pos, board_cell):
        """
        Shows the descp widget on the position supplied
        :param pos: tuple of pos_x, pos_y
        :return:
        """
        if not self.is_descp_visible():
            self.description_widget.update(board_cell)
            self.description_widget.setPos(pos)
            self.board_widget.add_widget(self.description_widget)

            # stop the game timer when the description is visible
            Clock.schedule_once(self.pause, timeout=self.DESCP_SHOW_DELAY_TIME * 1.1)

            show_animation = Animation(x=self.board_widget.pos[0], y=self.board_widget.pos[1], duration=self.DESCP_SHOW_DELAY_TIME)
            show_animation &= self.show_descp_animation
            show_animation.start(self.description_widget)

    def hide_descp_widget(self, obj=None, animation=True):
        if self.is_descp_visible():
            self.description_widget.hide_descp(animation)

            # start the game timer when the description is hide
            Clock.schedule_once(self.play, timeout=self.DESCP_SHOW_DELAY_TIME * 1.1)

            pos = self.description_widget.old_pos
            hide_animation = Animation(x=pos[0], y=pos[1], duration=self.DESCP_SHOW_DELAY_TIME)
            hide_animation &= self.hide_descp_animation
            hide_animation.start(self.description_widget)

    def remove_descp_widget(self, obj=None, button=None):
        self.board_widget.remove_widget(self.description_widget)
        self.description_widget.pos = self.board_widget.pos

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
            Clock.schedule_once(self.lose_popup.open, timeout=0.5)

        self.time_sec = current_time

        # always return true to keep alive the timer
        return True
