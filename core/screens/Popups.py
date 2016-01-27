# -*- coding: utf-8 -*-
import os
from kivy.animation import Animation, AnimationTransition
from kivy.properties import ObjectProperty, Clock
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

__author__ = 'y.febles'


class ModalViewBD(ModalView):
    pass


class GameWinView(ModalViewBD):
    continue_playing_bttn = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(GameWinView, self).__init__(*args, **kwargs)

    def start_open_animations(self):
        self.show_continue_button()

    def show_continue_button(self):
        self.continue_playing_bttn.opacity = 0
        self.continue_playing_bttn.x = self.pos[0] + self.width

        x_end = self.pos[0] + self.width * 0.25

        anim = Animation(x=x_end, transition=AnimationTransition.out_bounce)
        anim.start(self.continue_playing_bttn)


class GameLoseView(ModalViewBD):
    repeat_level_bttn = ObjectProperty()
    board_widget = ObjectProperty()
    container_layout = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(GameLoseView, self).__init__(*args, **kwargs)
        self.repeat_level_bttn.bind(on_press=self.reset)

        self.label_board_widgets = []
        self.board = None

    def start_open_animations(self):
        n = len(self.board)

        row_animation_duration = 0.2
        spacing = 0.02

        w, h = self.board_widget.width, self.board_widget.height
        x_base = self.board_widget.pos[0] + self.board_widget.width * spacing / 2
        y_base = self.board_widget.pos[1] + self.board_widget.height * spacing / 2

        for i in xrange(n):
            for j in xrange(n):
                cell_text = "" if self.board[i][j].visible else ""
                label = Label(text=cell_text, valign='middle', halign='center')

                label.font_name = os.path.join("assets", "fonts", "fontawesome-webfont.ttf")
                label.size_hint = [(1.0 - spacing * (n - 1)) / n, (1.0 - spacing * (n - 1)) / n]
                label.font_size = min(label.width, label.height) * 0.6
                label.pos = x_base + j * w / n, y_base + h

                self.board_widget.add_widget(label)
                self.label_board_widgets.append(label)

                anim = Animation(y=y_base + i * h / n, duration=((i + 1) * row_animation_duration))

                if not self.board[i][j].visible:
                    label_font_size = label.font_size
                    anim_expand_font = Animation(font_size=label_font_size * 6./5, duration=0.2)
                    anim_expand_font += Animation(font_size=label_font_size * 5./6, duration=0.2)

                    anim_expand_font.repeat = True

                    anim += anim_expand_font

                anim.start(label)

        Clock.schedule_once(self.start_continue_button,  timeout=(0.3 + n * row_animation_duration))

    def reset(self, obj=None):
        for w in self.label_board_widgets:
            self.board_widget.remove_widget(w)

        self.label_board_widgets = []

        self.repeat_level_bttn.opacity = 0
        self.repeat_level_bttn.pos = self.pos[0] + self.width, self.pos[1] + self.height * 0.025

    def start_continue_button(self, obj=None):
        x_end = self.pos[0] + self.width * 0.25

        anim = Animation(x=x_end, transition=AnimationTransition.out_bounce, duration=1)
        anim &= Animation(opacity=1)

        anim.start(self.repeat_level_bttn)


class HowToPlay(ModalView):
    close_bttn = ObjectProperty()