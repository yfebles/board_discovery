import os
from kivy.core.audio import SoundLoader
from core.Configs import Configs


class Sounds:
    """
    Singleton class that handles all the app sounds
    """

    class __Singleton:

        # region SOUNDS PATHS

        CLOCK_SOUND = os.path.join('assets', 'sounds', 'clock.wav')
        CLICK_SOUND = os.path.join('assets', 'sounds', 'click.wav')
        FLIP_SOUND = os.path.join('assets', 'sounds', 'flip_sound.wav')
        CELLS_PAIRED_OK = os.path.join('assets', 'sounds', 'cell_paired_ok.wav')
        CELLS_PAIRED_WRONG = os.path.join('assets', 'sounds', 'cell_paired_wrong.wav')


        # endregion

        def __init__(self, **kwargs):

            self.flip_sound, self.cell_paired_ok_sound, self.cell_paired_wrong_sound = [None] * 3
            self.click_sound = None

            self._load_sounds()

            self.play_clock_sound = lambda: self.try_play(self.clock_sound) \
                if self.clock_sound and self.clock_sound.state is not 'play' else None

            self.play_click_sound = lambda: self.try_play(self.click_sound)
            self.play_cell_flip_sound = lambda: self.try_play(self.flip_sound)
            self.play_cell_paired_ok_sound = lambda: self.try_play(self.cell_paired_ok_sound)
            self.play_cell_paired_wrong_sound = lambda: self.try_play(self.cell_paired_wrong_sound)

            self.stop_clock_sound = lambda: self.try_stop(self.flip_sound)
            self.stop_click_sound = lambda: self.try_stop(self.click_sound)
            self.stop_cell_flip_sound = lambda: self.try_stop(self.clock_sound)
            self.stop_cell_paired_ok_sound = lambda: self.try_stop(self.cell_paired_ok_sound)
            self.stop_cell_paired_wrong_sound = lambda: self.try_stop(self.cell_paired_wrong_sound)

        def try_play(self, sound):
            if Configs().sounds and sound:
                sound.play()

        def try_stop(self, sound):
            if Configs().sounds and sound:
                sound.stop()

        def _load_sounds(self):
            sounds = [SoundLoader.load(s) for s in [self.FLIP_SOUND, self.CLOCK_SOUND, self.CELLS_PAIRED_OK,
                                                    self.CELLS_PAIRED_WRONG, self.CLICK_SOUND]]

            sound_flip_cell_ok, sound_clock_ok, sound_pair_ok, sound_pair_wrong, sound_click_ok = sounds

            self.click_sound = None if not sound_click_ok else sound_click_ok
            self.flip_sound = None if not sound_flip_cell_ok else sound_flip_cell_ok
            self.cell_paired_ok_sound = None if not sound_pair_ok else sound_pair_ok
            self.cell_paired_wrong_sound = None if not sound_pair_wrong else sound_pair_wrong

            # the clock tick tack effect
            if sound_clock_ok:
                self.clock_sound = sound_clock_ok
                self.clock_sound.repeat = True

    # storage for the instance reference
    __instance = None

    def __init__(self, **kwargs):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Sounds.__instance is None:
            # Create and remember instance
            Sounds.__instance = Sounds.__Singleton(**kwargs)

        # Store instance reference as the only member in the handle
        self.__dict__['_Sounds__instance'] = Sounds.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)