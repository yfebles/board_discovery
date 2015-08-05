from random import randint
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, ShaderTransition, NoTransition, FadeTransition, SlideTransition, \
    SwapTransition, WipeTransition

__author__ = 'y.febles'


class Board(GridLayout):
    """
    An square board
    """

    def __init__(self, columns=3, size=(1000, 1000), **kwargs):
        GridLayout.__init__(self, **kwargs)

        with self.canvas.before:
            Rectangle(source="assets\\f0.jpg")

        self.spacing = 2
        self.cell_image = None
        self.board = []
        self.create_board(columns)

    def create_board(self, dimension):
        self.cols = dimension
        self.board = [[BoardCell(i, j) for j in range(dimension)] for i in range(dimension)]

        for i in xrange(self.cols):
            for j in xrange(self.cols):
                self.add_widget(self.board[i][j])
                self.board[i][j].bind(on_press=self.change_next_ones)

    def change_next_ones(self, button):

        i, j = button.i, button.j

        if i - 1 >= 0:
            self.board[i-1][j].background_color = [x*2.1 for x in button.background_color]
        if i + 1 < self.cols:
            self.board[i+1][j].text = button.text
        if j - 1 >= 0:
            self.board[i][j-1].text = button.text
        if j + 1 < self.cols:
            self.board[i][j+1].text = button.text


class InitialApp(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)

        self.sm = ScreenManager()

        self.i = 0

        # Add few screens
        for i in range(4):
            screen = Screen(name='Title %d' % i)
            b = Button(text='Title %d' % i)
            screen.add_widget(b)
            self.sm.add_widget(screen)

        # self.load_kv('game.kv')

    def build(self):
        box = BoxLayout(orientation='vertical')

        box.add_widget(self.sm)
        b = Button(text='Change screen')

        b.bind(on_press=self.change_next_ones)

        box.add_widget(b)
        return box

    def change_next_ones(self, button):
        x = [ShaderTransition, NoTransition, FadeTransition, SlideTransition, SwapTransition, WipeTransition]
        self.i = (self.i + 1) % 4
        r = randint(0, len(x)-1)
        self.sm.transition = x[r]()
        self.sm.current = 'Title %d' % self.i


class BoardCell(Button):
    """
    A board cell
    """
    sound = SoundLoader.load('assets\\pressed.wav')

    def __init__(self, i, j, **kwargs):
        Button.__init__(self, **kwargs)

        self.i, self.j = i, j

        self.foto = 1

        self.text = str(i*j + 1)

    def on_press(self):
        super(Button, self).on_press()

        self.foto = (self.foto + 1) % 4

        with self.canvas:
            Rectangle(source="assets\\f"+str(self.foto)+".jpg")

        if self.sound:
            self.sound.play()

        self.padding = [x+1 for x in self.padding]


# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
#
# # Create both screens. Please note the root.manager.current: this is how
# # you can control the ScreenManager from kv. Each screen has by default a
# # property manager that gives you the instance of the ScreenManager used.
# Builder.load_string("""
# <MenuScreen>:
#     BoxLayout:
#         Button:
#             text: 'Goto settings'
#             on_press: root.manager.current = 'settings'
#         Button:
#             text: 'Quit'
#
# <SettingsScreen>:
#     BoxLayout:
#         Button:
#             text: 'My settings button'
#         Button:
#             text: 'Back to menu'
#             on_press: root.manager.current = 'menu'
# """)
#
# # Declare both screens
# class MenuScreen(Screen):
#     pass
#
# class SettingsScreen(Screen):
#     pass
#
# # Create the screen manager
# sm = ScreenManager()
# sm.add_widget(MenuScreen(name='menu'))
# sm.add_widget(SettingsScreen(name='settings'))
#
# class TestApp(App):
#
#     def build(self):
#         return sm
#
# if __name__ == '__main__':
#     TestApp().run()