import os
from kivy.storage.jsonstore import JsonStore
from core.levels.Level import Level
from core.levels.LevelItem import LevelItem


class LevelManager:
    """
    Class that manages the levels. The load  and store process.
    Singleton pattern
    """

    class __Singleton:
        LEVELS_PATH = ""

        # the list of levels
        levels = None

        def __init__(self):

            if self.levels is not None:
                return

            # initialize the levels variables
            self.levels = []
            self.level_points = []
            self.current_level_index = -1

            # load the levels info and configure it
            self.db = JsonStore(os.path.join('core', 'levels', 'game.json'))

            self.__load_levels()

        def __load_levels(self):
            """
            set the configs and loads the levels data
            for the game
            :return:
            """
            levels_list = self.db["levels"]

            for l in levels_list:
                name, time, points = l["name"], l["time_seg"], l["points"]

                level = Level(name, time, points)

                level.items = self._get_level_items(l["items"])

                relations = [[value > 0 for value in row] for row in l["relations"]]
                level.relations = relations

                self.levels.append(level)

            self.level_points = self.db["score"]

            self.current_level_index = len(self.level_points)

        def _get_level_items(self, items_json):
            """
            Transform the list of items supplied in json dict format into the levelItem class
            :param items_json: the level item in json format
            :return:
            """

            # create the level items wit params of the json items,  visible is int --> (0,1)
            return [LevelItem(i["image"], i["name"], i["visible"] == 1, i["unlocked_times"], i["hints"])
                    for i in items_json]

        @property
        def next_level(self):
            """
            computes and return the next level if any.
            :return: Level object if there is another level or None if no more levels
            """

            self.current_level_index = len(self.level_points)

            if self.current_level_index >= len(self.levels):
                return None

            return self.levels[self.current_level_index]

        def save_level_points(self, points):

            self.level_points.append(points)
            self.current_level_index += 1

            # save the points data
            self.db.store_put("score", self.level_points)

            print(self.db["score"])

    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if LevelManager.__instance is None:
            # Create and remember instance
            LevelManager.__instance = LevelManager.__Singleton()

        # Store instance reference as the only member in the handle
        self.__dict__['_VisualItemsCache__instance'] = LevelManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
