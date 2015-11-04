import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from core.screens import *

class GameApp(App):

    # region CONSTANTS

    KV_FILE_PATH = os.path.join("assets", "kv_files", "menu_screen.kv")

    # endregion

    use_kivy_settings = False

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

        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.add_widget(self.play_screen)
        self.screen_manager.add_widget(self.levels_screen)
        self.screen_manager.add_widget(self.author_screen)

        self.levels_screen.bind(on_open_level=self.load_level)

        Clock.schedule_once(self._load_configs_on_play_screen, timeout=1)

        # dict for i18n
        self.translate_dict = {}

    def _load_configs_on_play_screen(self, dt):
        try:

            self.play_screen.sounds = self.config.getboolean('configs', 'sounds')
            self.play_screen.effects = self.config.getboolean('configs', 'effects')
            self.play_screen.first_run = self.config.getboolean('configs', 'first_run')

        except Exception as ex:
            print("errors changings " + ex.message)

    def load_level(self, obj, level):
        self.play_screen.pause()
        self.play_screen.load_level(level)
        self.screen_manager.current = 'play'

    def build_config(self, config):
        config.add_section('configs')
        config.set('configs', 'sounds', True)
        config.set('configs', 'effects', True)
        config.set('configs', 'show_hints', True)
        config.set('configs', 'first_run', True)

    def build_settings(self, settings):
        jsondata = '''[

        { "type": "bool", "title": "Sound",
          "desc": "Active application sounds",
          "section": "configs", "key": "sounds" },

        { "type": "bool", "title": "Effects",
          "desc": "Active application effects",
          "section": "configs", "key": "effects" },

        { "type": "bool", "title": "Hints",
          "desc": "Active hints",
          "section": "configs", "key": "show_hints" }
        ]'''

        settings.add_json_panel('Settings', self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        # value is 0 or 1 for the booleans
        if key == "sounds":
            self.play_screen.sounds = value != '0'

        if key == "effects":
            self.play_screen.effects = value != '0'

        if key == "first_run":
            self.play_screen.first_run = value != '0'

    # endregion

    def translate(self, text):
        pass

    def build(self):
        return self.screen_manager

    def close(self):
        try:

            self.config.set('configs', 'first_run', 0)
            self.config.write()

        except Exception as ex:
            print("errors changings " + ex.message)

        self.stop()

if __name__ == '__main__':
    app = GameApp()
    app.run()