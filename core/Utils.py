# -*- coding: utf-8 -*-
import os
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label


class EffectLabel(Label):
    def __init__(self, *args, **kwargs):
        super(EffectLabel, self).__init__(*args, **kwargs)
        self.font_name = "Ravie"
        self.font_size = 50


class WellDoneLabel(EffectLabel):
    def __init__(self, *args, **kwargs):
        super(WellDoneLabel, self).__init__(*args, **kwargs)
        self.texture = Image(source=os.path.join("assets", "images", "app_graphics", "right_points_texture.jpg")).texture
        self.texture_update()


class WrongDoneLabel(EffectLabel):
    def __init__(self, *args, **kwargs):
        super(WellDoneLabel, self).__init__(*args, **kwargs)
        self.texture = Image(source=os.path.join("assets", "images", "app_graphics", "wrong_points_texture.jpg")).texture
        self.texture_update()