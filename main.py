from screens import *
from kivy.app import App
from levels.Level import Level
from levels.LevelItem import LevelItem
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, FadeTransition


class GameApp(App):

    # region CONSTANTS

    KV_FILE_PATH = "assets\\kv_files\\menu_screen.kv"

    # endregion

    # region Initialize

    def __init__(self, *args, **kwargs):
        super(GameApp, self).__init__(*args, **kwargs)

        self.load_kv(self.KV_FILE_PATH)

        # set the transition manager between screens
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = FadeTransition(duration=0.1)

        # set the screens configuration
        self.menu_screen = MenuScreen(name='menu')
        self.play_screen = PlayScreen(name='play')
        self.author_screen = AuthorScreen(name='author')
        self.levels_screen = LevelsScreen(name='levels')
        self.settings_screen = SettingsScreen(name='settings')

        self.screens = [self.menu_screen, self.levels_screen, self.settings_screen, self.author_screen, self.play_screen]

        # load the levels info and configure it
        self.db = JsonStore('levels\\game.json')

        self.levels = []
        self.current_level_index = -1
        self.configure_levels()

        self.app_config = JsonStore('levels\\config.json')

    def configure_levels(self):
        """
        set the configs and loads the levels data
        for the game
        :return:
        """
        levels_list = self.db["levels"]

        self.levels = []

        for l in levels_list:
            name, time, points = l["name"], l["time_seg"], l["points"]

            level = Level(name, time, points)

            level.items = self._get_level_items(l["items"])

            relations = [[value > 0 for value in row] for row in l["relations"]]
            level.relations = relations

            self.levels.append(level)

        self.current_level_index = len(self.db["score"])

    def _get_level_items(self, items_json):
        """
        Transform the list of items supplied in
        json dict format into the levelItem class
        :param items_json:
        :return:
        """
        # create the level items wit params of the json items,  visible is int --> (0,1)

        return [LevelItem(i["image"], i["name"], i["visible"] == 1, i["unlocked_times"], i["hints"])
                for i in items_json]

    # endregion

    @property
    def next_level(self):
        """
        computes and return the next level if any.
        :return: Level object if there is another level or None if no more levels
        """

        self.current_level_index = len(self.db["score"])

        if self.current_level_index >= len(self.levels):
            return None

        return self.levels[self.current_level_index]

    @property
    def all_points(self):
        """
        computes and returns all the user points across levels
        :return:
        """
        try:
            points = self.db.get("score")

        except Exception as e:
            print(e.message)
            points = []

        return sum(points)

    def build(self):

        # add the screens to use on the app
        for screen in self.screens:
            self.screen_manager.add_widget(screen)

        next_level = self.next_level

        if next_level is not None:
            self.play_screen.load_level(next_level)

        return self.screen_manager

if __name__ == '__main__':
    app = GameApp()
    app.run()
