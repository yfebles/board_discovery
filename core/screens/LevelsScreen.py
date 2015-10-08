from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from core.levels.LevelManager import LevelManager


class LevelsScreen(Screen):

    levels_grid = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(LevelsScreen, self).__init__(*args, **kwargs)

        level_manager = LevelManager()
        levels_count = len(level_manager.levels)

        self.levels_grid.bind(minimum_height=self.levels_grid.setter('height'))

        self.spacing = 20

        for i in xrange(levels_count):
            bttn = Button(text=str(i), size_hint_y=None)

            self.levels_grid.add_widget(bttn)

