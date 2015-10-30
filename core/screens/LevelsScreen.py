from kivy._event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from core.levels.LevelManager import LevelManager


class LevelsScreen(Screen):

    levels_grid = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(LevelsScreen, self).__init__(*args, **kwargs)

        self.level_manager = LevelManager()

        self.register_event_type("on_open_level")

        self.levels_grid.bind(minimum_height=self.levels_grid.setter('height'))

    def load_levels(self):

        self.levels_grid.clear_widgets()

        # load the levels as
        for index, level in enumerate(self.level_manager.levels):
            text = "X" if level.blocked else str(index + 1)

            on_press_event = lambda obj: None if level.blocked else self.raise_open_level(index)

            self.levels_grid.add_widget(Button(text=text, size_hint_y=None, on_press=on_press_event))

    def raise_open_level(self, index):
        return lambda obj: self.dispatch("on_open_level", self.level_manager.levels[index])

    def on_open_level(self, level):
        """
        Event raised when a level should be opened
        by the play screen directly from this screen
        :param level: the level to open
        :return:
        """
        pass

    def on_enter(self, *args):
        self.load_levels()
