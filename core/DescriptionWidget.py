# -*- coding: utf-8 -*-

import os
from kivy.animation import Animation, AnimationTransition
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class DescriptionName(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)


class DescriptionWidget(FloatLayout):
    """
    The widget in which would be displayed the
    detailed item description.
    """

    # region CONSTANTS

    name_widget = ObjectProperty()
    descp_widget = ObjectProperty()
    DESCP_SHOW_DELAY_TIME = 0.45

    # endregion

    def __init__(self, **kwargs):
        FloatLayout.__init__(self, **kwargs)

        self.descp_widget = BoxLayout()
        self.descp_widget.orientation = "vertical"

        self.detail_descp_name = DescriptionName()
        self.detail_descp_name.transparency = 0.5
        self.detail_descp_name.size_hint = [1, 0.15]
        self.detail_descp_label = Label()

        self.hide_descp_update()
        self.descp_widget.size_hint = [0.95, 0.001]

        self.descp_widget.add_widget(self.detail_descp_name)
        self.descp_widget.add_widget(self.detail_descp_label)

        self.detail_descp_name.button_callback = self.hide_descp

        # animations
        show_transition = AnimationTransition.out_bounce
        hide_transition = AnimationTransition.out_bounce

        self.show_desp_animation = Animation(size_hint_y=0.95, duration=self.DESCP_SHOW_DELAY_TIME, transition=show_transition)
        self.hide_desp_animation = Animation(size_hint_y=0, duration=self.DESCP_SHOW_DELAY_TIME, transition=hide_transition)

        self.hide_desp_animation.bind(on_complete=self.hide_descp_update)

    def show_descp(self):
        if self.descp_widget not in self.children:
            self.show_descp_update()
            self.show_desp_animation.start(self.descp_widget)

    def hide_descp(self):
        if self.descp_widget in self.children:
            self.hide_desp_animation.start(self.descp_widget)

    def hide_descp_update(self, obj=None, button=None):
        self.remove_widget(self.descp_widget)
        self.detail_descp_name.name = ""
        self.detail_descp_name.button_text = ""
        self.detail_descp_label.text = ""

    def show_descp_update(self, obj=None):
        self.descp_widget.pos = self.pos[0] + self.width * 0.025, self.pos[1] + self.height * 0.025
        self.detail_descp_name.name = self.name_widget.name
        self.detail_descp_name.button_text = ""
        self.detail_descp_label.text = "Hello"

        # self.detail_descp_label.canvas.before.clear()
        with self.detail_descp_label.canvas.before:
            Color(0, 0, 0, 0.5)
            Rectangle(pos=self.descp_widget.pos, size=self.descp_widget.size)

        self.add_widget(self.descp_widget)

    def load_item(self, item):
        pass