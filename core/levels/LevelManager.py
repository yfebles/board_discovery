from core.levels.orm.db_orm import DB, Statistics, Level


class LevelManager:
    """
    Class that manages the levels. The load  and store process.
    Singleton pattern
    """

    class __Singleton:

        # the list of levels
        levels = None

        def __init__(self):

            if self.levels is not None:
                return

            # initialize the levels variables
            self.levels = []
            self.level_points = []

            # load the levels info and configure it
            self.db = DB().get_db_session()

            self.__load_levels()

        def __load_levels(self):
            """
            set the configs and loads the levels data
            for the game
            :return:
            """
            self.levels = []

            try:
                print("AAAAAAAAAAAAAAAAAAAAA")
                a = self.db.query(Level).all()

                for l in a:
                    name, time, points = l.name, l.time_seg, l.points

                    level = Level(name, time, points)

                    level.items = self._get_level_items(l["items"])

                    relations = [[value for value in row] for row in l["relations"]]
                    level.relations = relations
    
                    self.levels.append(level)
            except:
                pass

        def get_next_level(self, level=None):
            """
            computes and return the next level if any that is just after the supplied one
            The first if no supplied.
            :return: Level object if there is another level or None if no more levels
            """

            index = -1 if level is None else -1 if level not in self.levels else self.levels.index(level)

            index += 1

            if index > len(self.levels):
                return None

            return self.levels[index]

        def save_points(self, level, points):
            """
            save the amount of points as the result of play the
            level supplied
            :return:
            """
            try:

                self.db.add(Statistics(level=level, points=points))
                self.db.commit()

            except Exception as ex:
                print(ex.message)

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
