from kivy.uix.screenmanager import Screen
from core.Board import Board


class PlayScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

    def increase_lives(self):
        self.lives_lbl.text = str(int(self.lives_lbl.text) + 1)

    def load_level(self, level):
        """
        Load into the play screen the data of the level supplied
        :param level:
        :return:
        """
        pass