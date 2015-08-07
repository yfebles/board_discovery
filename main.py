from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import *
from kivy.config import Config


class GameApp(App):

    def __init__(self, *args, **kwargs):
        super(GameApp, self).__init__(*args, **kwargs)

        # set the transition manager between screens
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = NoTransition()

        # initialize the settings
        self.settings = {"music": True, "effects": True, "hints": True}
        # Config.add_section('global_settings')

        for item, value in self.settings.items():
            Config.set('global_settings', item, value)

        Config.write()

    def build(self):

        # add the screens to use
        self.screen_manager.add_widget(MenuScreen(name='menu'))
        self.screen_manager.add_widget(LevelsScreen(name='levels'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(AuthorScreen(name='author'))

        return self.screen_manager

if __name__ == '__main__':
    app = GameApp()
    app.run()
