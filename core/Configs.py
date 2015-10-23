from kivy.config import Config


class Config:
    """
    Singleton class to store and handling configs
    """

    class __Singleton:

        def __init__(self, **kwargs):
            self.use_sounds = kwargs["sounds"] if "sounds" in kwargs else True
            self.use_hints = kwargs["hints"] if "hints" in kwargs else True
            self.use_effects = kwargs["effects"] if "effects" in kwargs else True
            self.current_level = kwargs["current_level"] if "current_level" in kwargs else 0

    # storage for the instance reference
    __instance = None

    def __init__(self, **kwargs):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Config.__instance is None:
            # Create and remember instance
            Config.__instance = Config.__Singleton(**kwargs)

        # Store instance reference as the only member in the handle
        self.__dict__['_VisualItemsCache__instance'] = Config.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)