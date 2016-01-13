from core.db.db_orm import DB, Level, Package, Statistics


class LevelManager:
    """
    Class that manages the levels. The load  and store process.
    Singleton pattern
    """

    class __Singleton:

        def __init__(self):

            self.db = DB().get_db_session()

            # the raw list of levels
            self.levels = self._get_db_data(Level)

            self.packages = self._get_db_data(Package)

        def _get_db_data(self, entity):
            try:

                return self.db.query(entity).all()

            except Exception as e:
                print(e.message)

            return []

        def get_next_level(self, level=None):
            """
            computes and return the next level if any that is just after the supplied one
            The first if no supplied.
            :return: Level object if there is another level or None if no more levels
            """

            level_index = -1 if level is None else -1 if level not in self.levels else self.levels.index(level)

            return None if level_index + 1 >= len(self.levels) else self.levels[level_index + 1]

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
        self.__dict__['_LevelManager__instance'] = LevelManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to singleton """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to singleton """
        return setattr(self.__instance, attr, value)


