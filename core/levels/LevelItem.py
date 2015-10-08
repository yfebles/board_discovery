

class LevelItem:
    """
    Class that represents a
    """

    def __init__(self, image, name, visible, unlocked_times, hints):

        self.hints = hints
        if hints is None:
            self.hints = []

        self._hints_index = 0

        self.name = name
        self.visible = visible
        self.image = image
        self.unlocked_times = unlocked_times

    def clone(self):
        return LevelItem(self.image, self.name, self.visible, self.unlocked_times, self.hints)

    @property
    def active(self):
        """
        returns True if the level item is active to be used on the game
        False otherwise
        """
        return self.unlocked_times > 0

    def get_hint(self):
        if len(self.hints) == 0:
            return ""

        hint = self.hints[self._hints_index]
        self._hints_index = (self._hints_index + 1) % len(self.hints)
        return hint