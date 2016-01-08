
class Configs:
    """
    Singleton class to store and handling configs
    """

    class __Singleton:

        def __init__(self):
            self.sounds, self.hints, self.effects, self.first_run = [True] * 4
            self.current_level = 0

    # storage for the instance reference
    __instance = None

    def __init__(self, **kwargs):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Configs.__instance is None:
            # Create and remember instance
            Configs.__instance = Configs.__Singleton(**kwargs)

        # Store instance reference as the only member in the handle
        self.__dict__['_Configs__instance'] = Configs.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)