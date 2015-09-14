from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from core.Board import Board


class PlayScreen(Screen):

    points_lbl = ObjectProperty()
    lives_lbl = ObjectProperty()
    hints_lbl = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)
        self.db = JsonStore('levels\\game.json')

        self.points_lbl.text = str(self.all_points)

    @property
    def all_points(self):
        """
        computes and returns all the user points across levels
        :return:
        """
        try:
            points = self.db.get("score")

        except:
            points = []

        return sum(points)

    def load_level(self, level=None):
        """
        Load into the play screen the data of the level supplied
        :param level: the level supplied (if any) else try to load the next
        un played level
        """
        pass

    def pause(self):