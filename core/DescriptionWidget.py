# -*- coding: utf-8 -*-
import os
from kivy._event import EventDispatcher
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation, AnimationTransition

# region Helper Classes


class ColoredLabel(Label):

    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)


class DescriptionName(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

# endregion


class DescriptionWidget(FloatLayout, EventDispatcher):
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
        super(EventDispatcher, self).__init__(**kwargs)

        self.descp = ""

        self.register_event_type("on_hide")

        self.descp_widget = BoxLayout()
        self.descp_widget.orientation = "vertical"

        self.detail_descp_name = DescriptionName()
        self.detail_descp_name.transparency = 0.5
        self.detail_descp_name.size_hint = [1, 0.15]
        self.detail_descp_label = ColoredLabel()

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

    def is_descp_visible(self):
        return self.descp_widget in self.children

    def show_descp(self):
        if not self.is_descp_visible():
            self.show_descp_update()
            self.show_desp_animation.start(self.descp_widget)
            self.name_widget.opacity = 0

    def hide_descp(self, with_animation=True):
        if not self.is_descp_visible():
            return

        if with_animation:
            self.hide_desp_animation.start(self.descp_widget)
        else:
            self.descp_widget.size_hint_y = 0
            self.hide_descp_update()
            self.name_widget.opacity = 1

    def hide_descp_update(self, obj=None, button=None):
        self.remove_widget(self.descp_widget)

        self.name_widget.opacity = 1
        self.detail_descp_name.name = ""
        self.detail_descp_label.text = ""
        self.detail_descp_name.button_text = ""

    def show_descp_update(self, obj=None):
        self.descp_widget.pos = self.pos[0] + self.width * 0.025, self.pos[1] + self.height * 0.025
        self.detail_descp_name.name = self.name_widget.name
        self.detail_descp_name.button_text = ""
        self.detail_descp_label.text = self.descp
        self.add_widget(self.descp_widget)

    def update(self, board_cell):
        self.descp = board_cell.description
        self.image = board_cell.image
        self.name_widget.name = board_cell.name

    def on_hide(self):
        """
        Event raised when the widget must be hided
        :param level: the level to open
        :return:
        """
        pass