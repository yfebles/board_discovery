import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from core.screens import *


class GameApp(App):

    # region CONSTANTS

    KV_FILE_PATH = os.path.join("assets", "kv_files", "menu_screen.kv")

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

    def build_config(self, config):
        config.add_section('configs')
        config.set('configs', 'sound', True)
        config.set('configs', 'effects', True)
        config.set('configs', 'show_hints', True)
        config.set('configs', 'first_run', True)

    def build_settings(self, settings):

        jsondata = '''[
        { "type": "bool", "title": "Sound",
          "desc": "Active application sounds",
          "section": "configs", "key": "sound" },

        { "type": "bool", "title": "Effects",
          "desc": "Active application effects",
          "section": "configs", "key": "effects" },

        { "type": "bool", "title": "Hints",
          "desc": "Active hints",
          "section": "configs", "key": "show_hints" }
        ]'''

        settings.add_json_panel('Settings', self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        if config != self.config or section != 'configs':
            return

    # endregion
    def build(self):
        # add the screens to use on the app
        for screen in self.screens:
            self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    app = GameApp()
    app.run()
