

class Level:
    """
    A class to represent a game level.
    """

    def __init__(self, name="", time_seg=60, points=1000, hints=None, data=None):

        self.name = name

        # the time of duration of the level in segs
        self.time_seg = time_seg

        self.points = points

        # the list of
        self.hints = [] if hints is None else hints

        # the board data for the level
        self.data = [[]] if data is None else data

    @staticmethod
    def from_json(json_data):
        """
        Load a Level from json or dict format
        :param json_data: the json or dict format of the level.
        :return:
        """
        error = "name" in json_data and "time_seg" in json_data and "points" in json_data

        if error:
            raise Exception("Invalid data for level")

        return Level(json_data["name"], json_data["time_seg"], json_data["points"])
