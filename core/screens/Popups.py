# -*- coding: utf-8 -*-
import os
import random
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.animation import Animation, AnimationTransition
from kivy.properties import ObjectProperty, Clock
from core.Utils import WellDoneLabel


class ModalViewBD(ModalView):
    def start_animations(self):
        pass


class HowToPlay(ModalViewBD):
    close_bttn = ObjectProperty()


class GameFinishView(ModalViewBD):

    # region UI objects

    action_bttn = ObjectProperty()
    container_layout = ObjectProperty()
    message_label = ObjectProperty()
    board_widget = ObjectProperty()
    time_box = ObjectProperty()
    time_label = ObjectProperty()

    points_label = ObjectProperty()
    points_box = ObjectProperty()

    # endregion

    def __init__(self, *args, **kwargs):
        super(GameFinishView, self).__init__(*args, **kwargs)
        self.action_bttn.bind(on_press=self.continue_action)
        self.action_bttn.bind(on_press=self.reset)

        self.continue_playing_action = None
        self.repeat_level_action = None
        self.animations = []

        self.label_board_widgets = []

        # friend classes behavior with the play screen
        self.play_screen = None

    # region Properties

    @property
    def board(self):
        return self.play_screen.board

    @property
    def game_wined(self):
        """
        prop that says if the game if wined or loosed according to the visibility of their cells
        (all --> wined, loosed otherwise)
        :return:
        """
        return True

        # return self.play_screen.game_wined

    @property
    def points(self):
        return int(self.points_label.text)

    @points.setter
    def points(self, points):
        self.points_label.text = str(points)

    @property
    def time_sec(self):
        # time label in format "00:00" min:sec
        time = self.time_label.text

        time_s = int(time[0:2]) * 60 + int(time[3:])

        return time_s

    @time_sec.setter
    def time_sec(self, time_sec_count):

        # time label in format "00:00" min:sec
        minutes = time_sec_count / 60
        seconds = time_sec_count % 60

        minutes_str = str(minutes) if minutes >= 10 else "0" + str(minutes)
        seconds_str = str(seconds) if seconds >= 10 else "0" + str(seconds)

        self.time_label.text = minutes_str + ":" + str(seconds_str)

        # there is 4 images to show for time color changing
        index = time_sec_count * 4 / self.play_screen.current_level.time_seg
        img_src = "display_color_time_box{0}.png".format(1 + index)

        if index < 4 and img_src != self.time_box.back_color_img:
            self.time_box.back_color_img = img_src

    # endregion

    # region Animations

    def start_animations(self):
        """
        Start the animations of board objects like ? or emoticons
        :return:
        """

        n = len(self.board)

        game_wined = self.game_wined

        self.message_label.text = "Bien Hecho" if game_wined else "Has Perdido"
        self.action_bttn.user_text = "Continuar" if game_wined else "Repetir Nivel"

        row_animation_duration = 0.4

        w, h = self.board_widget.width * 1., self.board_widget.height * 1.
        x_base, y_base = self.board_widget.pos[0], self.board_widget.pos[1]

        for i in xrange(n):
            for j in xrange(n):
                cell_text = "" if self.board[i][j].visible else ""

                label = Label(valign='middle', halign='center', width=(w / n), height=(h / n), pos=(x_base + j * w / n, y_base + h),
                              markup=True, font_name=os.path.join("assets", "fonts", "fontawesome-webfont.ttf"))
                label.font_size = min(label.width, label.height) * 0.8

                label.text = "[color=#00FF00]" + cell_text + "[/color]"

                self.board_widget.add_widget(label)
                self.label_board_widgets.append(label)

                anim = Animation(y=y_base + i * h / n, duration=((i + 1) * row_animation_duration),
                                 transition=AnimationTransition.out_bounce)

                if not self.board[i][j].visible:
                    label.text = cell_text

                    label_font_size = label.font_size

                    # expand animation
                    anim_expand_font = Animation(font_size=label_font_size * 6./5, duration=0.2)
                    anim_expand_font += Animation(font_size=label_font_size * 5./6, duration=0.2)
                    anim_expand_font.repeat = True
                    anim += anim_expand_font

                anim.start(label)
                self.animations.append((anim, label))

        Clock.schedule_once(self.start_time_animation,  timeout=(n * row_animation_duration))

    def start_time_animation(self, obj=None):
        """
        method that continue the animations with the time and points effects
        :return:
        """
        if not self.game_wined:
            # if game loosed go straight to continue button
            Clock.schedule_once(self.continue_button_animation,  timeout=0.3)
            return

        # make the time and points animations
        self.reset()

        x_end = self.pos[0] + self.width * 0.25
        self.time_sec = self.play_screen.time_sec
        self.points = self.play_screen.points

        anim = Animation(opacity=1, x=x_end, transition=AnimationTransition.out_bounce, duration=1)

        anim.start(self.time_box)
        anim.start(self.points_box)

        Clock.schedule_once(self.add_points_anim_handler, timeout=1)

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
        animation_type = random.random()

        lbl = WellDoneLabel(text=str(self.play_screen.current_level.points), pos=self.board_widget.pos)

        x_orig, y_orig = pos[0], pos[1]

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

    def add_points_anim_handler(self, dt):
        """

        :param dt:
        :return:
        """
        if self.time_sec <= 0:
            Clock.schedule_once(self.show_performance_text_anim,  timeout=0.2)
            return

        self.time_sec -= 1

        self.points += self.play_screen.current_level.points

        w = random.randint(int(self.board_widget.width * 0.05), int(self.board_widget.width * 0.15))

        x = random.randint(int(self.board_widget.pos[0]), int(self.board_widget.pos[0] + self.board_widget.width))
        y = random.randint(int(self.board_widget.pos[1]), int(self.board_widget.pos[1] + self.board_widget.height))

        self.create_points_effect((x, y), w, w)

        # todo check speed
        new_dt = 0.3 if dt > 0.5 else dt * 0.9

        Clock.schedule_once(self.add_points_anim_handler,  timeout=new_dt)

    def show_performance_text_anim(self, obj=None):
        """
        method that shows a text animation for the user result based on the points earned
        :param obj:
        :return:
        """

        Clock.schedule_once(self.continue_button_animation,  timeout=0.5)

    def continue_button_animation(self, obj=None):
        """
        Animation that shows the button of continue action to the user
        :param obj:
        :return:
        """
        x_end = self.pos[0] + self.width * 0.25

        anim = Animation(x=x_end, transition=AnimationTransition.out_bounce, duration=1)
        anim &= Animation(opacity=1)

        anim.start(self.action_bttn)

    # endregion

    def remove_widget_later(self, widget, time=1):
        function = lambda obj: self.board_widget.remove_widget(widget)
        Clock.schedule_once(function, timeout=time)

    def continue_action(self, obj=None):
        """
        Method that execute the supplied action when the button of continue or
        repeat level has been pressed.
        :param obj:
        :return:
        """
        if self.play_screen is None:
            raise Exception()

        action = self.play_screen.save_and_continue if self.game_wined else self.play_screen.reload_level

        action()

    def reset(self, obj=None):
        for w in self.label_board_widgets:
            self.board_widget.remove_widget(w)

        for anim, label in self.animations:
            anim.cancel(label)

        self.animations = []
        self.label_board_widgets = []

        self.action_bttn.opacity = 0
        self.action_bttn.pos = self.pos[0] + self.width, self.pos[1] + self.height * 0.03

        w, h = self.board_widget.width, self.board_widget.height

        # reset time box
        self.time_box.opacity = 0
        self.time_box.width, self.time_box.height = self.width * 0.6, self.height * 0.15
        self.time_box.pos = self.board_widget.pos[0] + w, self.board_widget.pos[1] + h * 0.65

        # reset points box
        self.points_box.opacity = 0
        self.points_box.width, self.points_box.height = self.width * 0.6, self.height * 0.2
        self.points_box.pos = self.board_widget.pos[0] - w, self.board_widget.pos[1] + h * 0.15