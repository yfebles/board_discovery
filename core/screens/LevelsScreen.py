from kivy.uix.button import Button
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from core.BoardCell import LevelBoardCell
from core.LevelManager import LevelManager


class LevelsScreen(Screen, EventDispatcher):

    levels_grid = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(LevelsScreen, self).__init__(*args, **kwargs)
        super(EventDispatcher, self).__init__(*args, **kwargs)

        self.level_manager = LevelManager()

        self.register_event_type("on_open_level")

        self.levels_grid.bind(minimum_height=self.levels_grid.setter('height'))

    def load_levels(self):

        self.levels_grid.clear_widgets()

        # load the levels as
        for index, level in enumerate(self.level_manager.levels):

            self.levels_grid.add_widget(LevelBoardCell(size_hint_y=None, on_touch_down=self.raise_open_level(index)))

    def raise_open_level(self, index):
        return lambda obj, obj2: self.dispatch("on_open_level", self.level_manager.levels[index])

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
