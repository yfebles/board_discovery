# -*- coding: utf-8 -*-

import random
from math import sqrt

from kivy.app import App
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, Clock

from core.Utils import *
from core.Sounds import Sounds
from core.db.db_orm import DB
from core.BoardCell import BoardCell
from kivy.uix.bubble import Bubble
from core.LevelManager import LevelManager
from core.DescriptionWidget import DescriptionWidget
from core.screens.Popups import GameFinishView, HowToPlay


class PlayScreen(Screen):
    """
    In several methods an argument dt is supplied
    cause are methods called from a clock timer schedule
    """

    # region WIDGETS

    board_widget = ObjectProperty()
    toast_widget = ObjectProperty()
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


    # endregion

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        self.db = DB().get_db_session()
        self.level_manager = LevelManager()

        self.help_widget, self.description_widget = [DescriptionWidget()] * 2

        self.description_widget.bind(on_hide=self.hide_descp_widget)
        self.description_widget.size_hint = [0, 0]

        # animations
        self.show_descp_animation = Animation(size_hint_y=1, size_hint_x=1, duration=self.DESCP_SHOW_DELAY_TIME)
        self.hide_descp_animation = Animation(size_hint_y=0, size_hint_x=0, duration=self.DESCP_SHOW_DELAY_TIME)
        self.pause_animation = Animation(opacity=0, duration=0.8) + Animation(opacity=1, duration=0.8)

        self.hide_descp_animation.bind(on_complete=self.remove_descp_widget)
        self.pause_animation.repeat = True

        # Config Vars
        self.effects, self.first_run, self.game_paused = [True] * 3

        self.board = []
        self.hide_descp_pos = 0,0
        self.cell_selected, self.second_cell_selected, self.current_level = [None] * 3

        # list with the randomized operations of the last loaded level
        self.randomized_positions = []

        # win and lose level animations widgets (Popups by now)
        self.game_finish_view = GameFinishView()

        # friend classes behavior
        self.game_finish_view.play_screen = self

        self.how_to_play_popup = HowToPlay()

        self.how_to_play_popup.close_bttn.bind(on_press=lambda obj: self.play() if not self.is_descp_visible() else None)

        Clock.schedule_interval(self.update_time, timeout=1)

    # region Properties

    @property
    def game_wined(self):
        """
        prop that says if the game if wined or loosed according to the visibility of their cells
        (all --> wined, loosed otherwise)
        :return:
        """
        # the game is wined if all the cells are visible
        return all([self.board[i][j].visible for i in xrange(self.columns) for j in xrange(self.columns)])

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
        if time_sec_count < 10:
            Sounds().play_clock_sound()

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

    def save_and_continue(self, obj=None):
        """
        save the data of the current level of play. Unlock the next levels
        and load the next one
        :return:
        """
        self.level_manager.save_points(self.current_level, self.points)

        self.load_next_level()

    def reload_level(self):
        self.load_level(self.current_level, True)

    def load_level(self, level=None, re_load=False):
        """
        Load into the play screen the data of the level supplied
        :param level: the level supplied (if any) else try to load the next
        un played level
        """
        self.current_level = self.current_level if re_load else level

        cols = self.columns
        if cols < 2:
            raise Exception("The board must have at least 2x2 cells")

        self.points = 0
        self.time_sec = level.time_seg
        self.cell_selected, self.second_cell_selected = None, None

        self.board_widget.clear_widgets()

        self.board = [[] for _ in xrange(cols)]

        for i in xrange(cols):
            for j in xrange(cols):
                board_cell = BoardCell(level.items[i * cols + j], i, j)

                # board[i][j]
                self.board[i].append(board_cell)

                self.board_widget.add_widget(board_cell)
                board_cell.bind(on_press=self.cell_pressed)

        self._randomize_board(re_load)

        self.update_cells_positions()
        self.hide_descp_widget()
        self.play()

    def _randomize_board(self, re_load):
        """
        Randomize the items on the board
        :param re_load: True if re use the previous randomization for the level
        :return:
        """
        cols = self.columns

        if not re_load:
            self.randomized_positions = [[random.randint(0, cols - 1) for _ in range(cols)] for _ in xrange(cols * cols)]

        # randomize the level with cols^2 changes or load the previous order if reload level
        for r in self.randomized_positions:

            temp = self.board[r[0]][r[1]]
            self.board[r[0]][r[1]] = self.board[r[2]][r[3]]
            self.board[r[2]][r[3]] = temp

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
            Clock.schedule_once(self.game_finish_view.open, timeout=0.5)

        self.load_level(next_level)

    # endregion

    # region Game Behavior

    def check_game_state(self):
        """
        checks if the game is finished or not.
        If game has been wined or lose raise the events accordingly
        :return:
        """

        if self.game_wined:
            # game win animation
            self.pause()

            Clock.schedule_once(self.game_finish_view.open, timeout=1)

    def cell_pressed(self, board_cell):
        if board_cell.visible:
            self.show_descp_widget(board_cell)
            return

        if board_cell.locked or self.game_paused or self.current_level is None or self.is_descp_visible():
            return

        board_cell.visible = True

        # if no un-paired cell is visible (just visible the already paired)
        if self.cell_selected is None:
            self.cell_selected = board_cell
            return

        cells_related = self.current_level.are_connected(self.cell_selected.level_item, board_cell.level_item)

        cell_selected = self.cell_selected
        self.cell_selected = None

        if cells_related:
            action = lambda: self.cell_paired_ok(cell_selected, board_cell)
        else:
            action = lambda: self.cell_paired_failed(cell_selected, board_cell)

        board_cell.unlocked_action = action

    def cell_paired_ok(self, cell_selected, board_cell):
        # play paired sound if must be
        Sounds().play_cell_paired_ok_sound()

        # if related cells show points
        pos, w, h = cell_selected.pos, cell_selected.width, cell_selected.height
        pos1, w1, h1 = board_cell.pos, board_cell.width, board_cell.height

        Clock.schedule_once(lambda obj: self.create_points_effect(pos, w, h, self.current_level.points), 0.1)
        Clock.schedule_once(lambda obj: self.create_points_effect(pos1, w1, h1, self.current_level.points), 0.3)

        # check if the game has been wined
        self.check_game_state()

    def cell_paired_failed(self, cell_selected, board_cell):
        # play un-paired sound if must be
        Sounds().play_cell_paired_wrong_sound()

        cell_selected.visible = False
        board_cell.visible = False

        board_cell.unbind()

    # endregion

    # region Pause & Play

    def switch_pause_state(self):
        action = self.play if self.game_paused else self.pause
        action()

    def pause(self, dt=None):
        self.game_paused = True
        self.pause_animation.start(self.time_lbl)

        Sounds().stop_clock_sound()

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

    def show_descp_widget(self, board_cell):
        """
        Shows the descp widget on the position supplied
        :param pos: tuple of pos_x, pos_y
        :return:
        """
        if not self.is_descp_visible():

            self.hide_descp_pos = board_cell.center
            self.description_widget.pos = board_cell.center

            self.description_widget.update(board_cell)
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

            pos = self.hide_descp_pos
            hide_animation = Animation(x=pos[0], y=pos[1], duration=self.DESCP_SHOW_DELAY_TIME)
            hide_animation &= self.hide_descp_animation
            hide_animation.start(self.description_widget)

    def remove_descp_widget(self, obj=None, button=None):
        self.board_widget.remove_widget(self.description_widget)
        self.description_widget.pos = self.board_widget.pos

    # endregion

    # region Effects

    def remove_widget_later(self, widget, time=1):
        function = lambda obj: self.board_widget.remove_widget(widget)
        Clock.schedule_once(function, timeout=time)

    def create_points_effect(self, pos, width, height, points_change=0, duration=1):
        """
        Display a text with animation inside of the rectangle with left bottom corner at pos
        and the dimension supplied of width, height.

        :param pos: The pos of the text message
        :param width:
        :param height:
        :param points_change: The amount of points that are modified (sum or rest) by this action
        :param duration: The duration in seconds of the animation
        :return:
        """
        self.points += points_change

        animation_type = random.random()

        lbl = WellDoneLabel(text=str(self.current_level.points))

        x_orig, y_orig = pos[0] - self.board_widget.width / 2.0, pos[1] - self.board_widget.height / 2.0

        anim = Animation(opacity=0) & Animation(font_size=lbl.font_size * 1.5)

        # region Animation Types

        if animation_type < 0.3:
            # from the bottom center to right upper corner
            x_end = x_orig + width
            x_orig += width / 2.0

        elif animation_type < 0.65:
            # from the bottom center to upper center
            x_end = x_orig + width / 2.0
            x_orig += width / 2.0

        else:
            # from the bottom right to left upper corner
            x_end = x_orig
            x_orig += width

        # endregion

        y_end = y_orig + height

        lbl.pos = x_orig, y_orig
        anim &= Animation(x=x_end, y=y_end)

        anim.start(lbl)

        self.board_widget.add_widget(lbl)
        self.remove_widget_later(lbl, duration)

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
            Clock.schedule_once(self.game_finish_view.open, timeout=0.5)

        self.time_sec = current_time

        # always return true to keep alive the timer
        return True

    def display_how_to_play(self, obj=None):
        self.pause()

        self.how_to_play_popup.open()

    def display_balloon(self, text, pos, time=3):
        """
        Display a balloon widget with text to help the user or
        give him some text message
        :param text:
        :return:
        """

        self.toast_widget.opacity = 1
        self.toast_widget.width = 100
        self.toast_widget.height = 100

        self.toast_widget.pos = self.board_widget.pos

        anim = Animation(opacity=0)

        Clock.schedule_once(lambda dt: anim.start(self.toast_widget), timeout=time)