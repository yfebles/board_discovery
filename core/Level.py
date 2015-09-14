from core.LevelItem import LevelItem


class Level:
    """
    A class to represent a game level.
    Contain the elements
    """

    def __init__(self, name="", time_seg=60, points=1000, items=None, relations=None):
        """
        Create a new level of game.
        :param items: the board items
        :param name: the name of the level
        :param points: the points for each action on the game
        :param time_seg: the time of duration of the level in segs
        :type relations: bolean matrix of len items*items with the relations between items
        :return:
        """

        if items is None or not isinstance(items, list):
            self.items = []

        self.items = [LevelItem(item["image"], item["name"], item["visible"], item["unlocked_times"], item["hints"])
                      for item in items]

        self.relations = relations
        if self.relations is None:
            self.relations = [[None for _ in self.items] for _ in self.items]

        elif len(relations) != len(items) * len(items):
            raise Exception("Relations must be a square matrix of size {0}".format(len(items) * len(items)))

        self.name = name
        self.points = points
        self.time_seg = time_seg

    def get_hint(self, index):
        """
        Get and return (if exists) the next hint for
        the item in the position index (zero based)
        :param index:
        :return:
        """
        if not 0 <= index < len(self.items):
            raise IndexError()

        return self.items[index].get_hint()

    def are_connected(self, i, j):
        """
        return True if the level items at positions i and j are connected
        on the relation matrix
        :param i: index of first item
        :param j: index of second item
        :return:
        """
        if not 0 <= i < len(self.items) or not 0 <= j < len(self.items):
            raise IndexError()

        return self.relations[i][j]

    @staticmethod
    def from_json(json_data):
        """
        Load a Level from json or dict format
        :param json_data: the json or dict format of the level.
        :return:
        """
        ok = "name" in json_data and "time_seg" in json_data and "points" in json_data \
             and "items" in json_data and "relations" in json_data

        if not ok:
            raise Exception("Invalid data to create a level")

        name = json_data["name"]
        time = json_data["time_seg"]
        points = json_data["points"]
        items = json_data["items"]
        relations = json_data["relations"]

        return Level(name, time, points, items, relations)
