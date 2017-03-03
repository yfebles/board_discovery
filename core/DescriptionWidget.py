# -*- coding: utf-8 -*-
import os
from kivy._event import EventDispatcher
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation, AnimationTransition

# region Helper Classes

class ShadowLabel(Label):
    decal = ListProperty([0, 0])
    tint = ListProperty([1, 1, 1, 1])

class ColoredLabel(Label):
    pass

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

    close_bttn = ObjectProperty()
    descp_widget = ObjectProperty()

    DESCP_SHOW_DELAY_TIME = 0.45

    # endregion

    def __init__(self, **kwargs):
        FloatLayout.__init__(self, **kwargs)
        super(EventDispatcher, self).__init__(**kwargs)

        self.register_event_type("on_hide")

        self.descp_widget.button_callback = self.show_descp

        # animations
        show_transition = AnimationTransition.out_bounce
        hide_transition = AnimationTransition.out_bounce

        self.show_desp_animation = Animation(size_hint_y=0.85, duration=self.DESCP_SHOW_DELAY_TIME, transition=show_transition)
        self.hide_desp_animation = Animation(size_hint_y=0, duration=self.DESCP_SHOW_DELAY_TIME, transition=hide_transition)

        self.show_desp_container_anim = Animation(size_hint_y=0.95, duration=self.DESCP_SHOW_DELAY_TIME, transition=show_transition)
        self.hide_desp_container_anim = Animation(size_hint_y=0.15, duration=self.DESCP_SHOW_DELAY_TIME, transition=hide_transition)

    def is_descp_visible(self):
        # if has some height
        return self.descp_widget.descp_item.size_hint[1] > 0.15

    def show_descp(self):
        if self.is_descp_visible():
            return

        self.close_bttn.opacity = 0
        self.descp_widget.button_text = ""
        self.descp_widget.button_callback = self.hide_descp

        # open the description label
        self.show_desp_animation.start(self.descp_widget.descp_item)
        self.hide_desp_container_anim.start(self.descp_widget.name_widget)

        # open the description container
        self.show_desp_container_anim.start(self.descp_widget)

    def hide_descp(self, with_animation=True):
        if not self.is_descp_visible():
            return

        if with_animation:
            # hide the description label
            self.hide_desp_animation.start(self.descp_widget.descp_item)
            self.show_desp_container_anim.start(self.descp_widget.name_widget)

            # hide the description container
            self.hide_desp_container_anim.start(self.descp_widget)

        else:
            self.descp_widget.descp_item.size_hint_y = 15

        self.descp_widget.button_callback = self.show_descp
        self.descp_widget.button_text = ""
        self.close_bttn.opacity = 1

    def update(self, board_cell):
        self.image = board_cell.image
        self.descp_widget.name = board_cell.name
        self.descp_widget.descp = board_cell.description

    def dispatch_hide(self):
        self.hide_descp(False)
        self.dispatch("on_hide")

    def on_hide(self):
        """
        Event raised when the widget must be hided
        :param level: the level to open
        :return:
        """
        pass