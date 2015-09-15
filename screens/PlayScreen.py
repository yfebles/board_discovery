from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from core.Level import Level
from core.Board import Board


class PlayScreen(Screen):

    # region WIDGETS

    points_lbl = ObjectProperty()
    lives_lbl = ObjectProperty()
    hints_lbl = ObjectProperty()
    board = ObjectProperty()

    # endregion

    def __init__(self, *args, **kwargs):
        super(PlayScreen, self).__init__(*args, **kwargs)

        # the level currently being played
        self.current_level = None

        self.register_event_type('on_game_ended')

        self.board.bind(on_game_ended=self.game_end)
        self.board.bind(on_points_made=self.update_points)

    def load_level(self, level):
        """
        Load into the play screen the data of the level supplied
        :param level: the level supplied (if any) else try to load the next
        un played level
        """
        # create
        self.current_level = level.clone()

        self.board.load_level(level)

    def on_game_ended(self):
        """
        event raised when the game has end in this level
        :return:
        """
        pass

    def game_end(self, board, game_win):
        # save the user points for the level

        if game_win:
            points = int(self.points_lbl.text)
            self.db["score"].append(points)
            self.dispatch("on_game_ended")
            return

        # ask for repeat level
        repeat_level = True

        if repeat_level:
            # if true reload level
            self.load_level(self.current_level)
        else:
            self.dispatch("on_game_ended")

    def update_points(self, board, points):
        current_points = int(self.points_lbl.text)

        self.points_lbl.text = str(current_points + points)

