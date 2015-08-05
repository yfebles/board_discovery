from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import *


class GameApp(App):

    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)

        # set the transition manager between screens
        self.screen_manager = ScreenManager()

        self.screen_manager.add_widget(MenuScreen(name='menu'))
        # self.screen_manager.add_widget(LevelsScreen(name='levels'))
        # self.screen_manager.add_widget(SettingsScreen(name='settings'))
        # self.screen_manager.add_widget(AuthorScreen(name='author'))

    # def change_to(self, screen_name):
    #     if screen_name == 'play':
    #

    def build(self):
        return self.screen_manager

if __name__ == '__main__':
    app = GameApp()
    app.run()

#