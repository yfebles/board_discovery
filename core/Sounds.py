from kivy.config import Config
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
        FLIP_SOUND = os.path.join('assets', 'sounds', 'flip_sound.wav')
        CELLS_PAIRED_OK = os.path.join('assets', 'sounds', 'cell_paired_ok.wav')
        CELLS_PAIRED_WRONG = os.path.join('assets', 'sounds', 'cell_paired_wrong.wav')

        # endregion

        def __init__(self, **kwargs):

            self.flip_sound, self.cell_paired_ok_sound, self.cell_paired_wrong_sound, self.clock_sound = [None] * 4

            self._load_sounds()

        # region Play Methods

        def try_play(self, sound):
            if Configs().sounds and sound:
                sound.play()

        def play_cell_flip_sound(self):
            """
            Plays the button click sound
            :return:
            """
            self.try_play(self.flip_sound)

        def play_cell_paired_ok_sound(self):
            """
            Plays the button click sound
            :return:
            """
            self.try_play(self.cell_paired_ok_sound)

        def play_cell_paired_wrong_sound(self):
            """
            Plays the button click sound
            :return:
            """

            self.try_play(self.cell_paired_wrong_sound)

        def play_clock_sound(self):
            """
            Plays the button click sound
            :return:
            """
            if self.clock_sound and self.clock_sound.state is not 'play':
                self.try_play(self.clock_sound)

        # endregion

        # region Stop Methods

        def try_stop(self, sound):
            if Configs().sounds and sound:
                sound.stop()

        def stop_cell_flip_sound(self):
            """
            Plays the button click sound
            :return:
            """
            self.try_stop(self.flip_sound)

        def stop_cell_paired_ok_sound(self):
            """
            Plays the button click sound
            :return:
            """
            self.try_stop(self.cell_paired_ok_sound)

        def stop_cell_paired_wrong_sound(self):
            """
            Plays the button click sound
            :return:
            """

            self.try_stop(self.cell_paired_wrong_sound)

        def stop_clock_sound(self):
            """
            Plays the button click sound
            :return:
            """

            self.try_stop(self.clock_sound)
        # endregion

        def _load_sounds(self):
            sounds = [SoundLoader.load(s) for s in [self.FLIP_SOUND, self.CLOCK_SOUND, self.CELLS_PAIRED_OK,
                                                    self.CELLS_PAIRED_WRONG]]

            sound_flip_cell, sound_clock, sound_pair_ok , sound_pair_wrong = sounds

            self.flip_sound = None if not sound_flip_cell else sound_flip_cell
            self.cell_paired_ok_sound = None if not sound_pair_ok else sound_pair_ok
            self.cell_paired_wrong_sound = None if not sound_pair_wrong else sound_pair_wrong

            # the clock tick tack effect
            if sound_clock:
                self.clock_sound = sound_clock
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