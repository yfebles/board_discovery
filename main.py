from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import *
from utils import *


class GameApp(App):

    def __init__(self, *args, **kwargs):
        super(GameApp, self).__init__(*args, **kwargs)

        # set the transition manager between screens
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = NoTransition()

    def build(self):

        # add the screens to use on the app
        self.screen_manager.add_widget(MenuScreen(name='menu'))
        self.screen_manager.add_widget(LevelsScreen(name='levels'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(AuthorScreen(name='author'))
        self.screen_manager.add_widget(PlayScreen(name='play'))

        return self.screen_manager

if __name__ == '__main__':
    app = GameApp()
    app.run()
