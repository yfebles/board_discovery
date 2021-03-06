# -*- coding: utf-8 -*-

import os
import webbrowser
from kivy.app import App
from kivy.core.image import Image
from core.screens import *
from core.Sounds import Sounds
from core.Configs import Configs
from kivy.utils import platform
from kivy.core.window import Window, android
from kivy.uix.screenmanager import ScreenManager, FadeTransition


class GameApp(App):

    # region CONSTANTS

    use_kivy_settings = False
    ESCAPE_BUTTON_CODE = 27
    ANDROID_MENU_BUTTON_CODE = 1001
    ANDROID_BACK_BUTTON_CODE = 1000

    KV_FILE_PATH = os.path.join("assets", "kv_files", "menu_screen.kv")
    PLAY_STORE_PAGE = "http://play.google.com/giftyplay"
    FB_PAGE = "https://www.facebook.com/GiftyGames-613182575451414/"
    TWITTER_PAGE = "https://www.twitter.com"

    # endregion

    def __init__(self, *args, **kwargs):
        super(GameApp, self).__init__(*args, **kwargs)

        self.load_kv(self.KV_FILE_PATH)

        self.sounds = Sounds()

        # set the transition manager between screens
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = FadeTransition(duration=0.4)

        # set the screens configuration
        self.presentation_screen = PresentationScreen(name='presentation')

        # no author, level or menu screen on lite version
        # self.author_screen = AuthorScreen(name='author')
        # self.levels_screen = LevelsScreen(name='levels')
        # self.menu_screen = MenuScreen(name='menu')

        self.play_screen = PlayScreen(name='play')

        self.screen_manager.add_widget(self.presentation_screen)
        self.screen_manager.add_widget(self.play_screen)

        # self.screen_manager.add_widget(self.menu_screen)
        # self.screen_manager.add_widget(self.levels_screen)
        # self.screen_manager.add_widget(self.author_screen)

        # self.levels_screen.bind(on_open_level=self.load_level)

        Clock.schedule_once(self._load_configs, timeout=1)

        self.bind(on_start=self.post_build_init)

        # dict for i18n
        self.translate_dict = {}

    # region Build & Configs

    def build(self):
        return self.screen_manager

    def close(self):
        try:

            self.config.set('configs', 'first_run', 0)
            self.config.write()

        except Exception as ex:
            print("errors changings " + ex.message)

        self.stop()

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

    def _load_configs(self, dt):
        try:
            Configs().sounds = self.config.getboolean('configs', 'sounds')
            Configs().effects = self.config.getboolean('configs', 'effects')
            Configs().first_run = self.config.getboolean('configs', 'first_run')

        except Exception as ex:
            print("errors changing " + ex.message)

    def on_config_change(self, config, section, key, value):
        # value is '0' or '1' for the booleans

        if key == "sounds":
            Configs().sounds = value != '0'

        if key == "effects":
            Configs().effects = value != '0'

        if key == "first_run":
            Configs().first_run = value != '0'

        if key == "hints":
            Configs().hints = value != '0'

    # endregion

    # region Handle back button on Android

    def post_build_init(self, *args):
        if platform() == 'android':
            android.map_key(android.KEYCODE_BACK, self.ANDROID_BACK_BUTTON_CODE)

        win = Window
        win.bind(on_keyboard=self.key_handler)

    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [self.ESCAPE_BUTTON_CODE, self.ANDROID_BACK_BUTTON_CODE, self.ANDROID_MENU_BUTTON_CODE]:
            # if self.screen_manager.current in ['menu', 'presentation']:
            #     self.close()

            # self.screen_manager.current = 'menu'
            return True

        return False

    # endregion

    def load_level(self, obj, level):
        self.play_screen.pause()
        self.play_screen.load_level(level)
        self.screen_manager.current = 'play'

    # region Visit Page

    def visit_page(self, obj=None, url=""):
        webbrowser.open(url)

    def visit_fb_page(self, obj=None):
        webbrowser.open(self.FB_PAGE)

    def visit_twitter_page(self, obj=None):
        webbrowser.open(self.TWITTER_PAGE)

    def visit_googleplay_page(self, obj=None):
        webbrowser.open(self.PLAY_STORE_PAGE)

    # endregion

    def translate(self, text):
        return text

if __name__ == '__main__':
    app = GameApp()
    app.run()
