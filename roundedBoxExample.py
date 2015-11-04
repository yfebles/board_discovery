from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from math import sin, cos, pi

kv = '''
BoxLayout:
    FloatLayout:
        RoundedBox:
            pos_hint: {'center': (.5, .5)}
            size: 200, 200
            size_hint: None, None
            id: rb
            corners: 20, 40, 60, 80
            line_width: 10
    GridLayout:
        size_hint_x: .2
        cols: 2
        Label:
            text: 'corner 1'
        Slider:
            value: rb.corners[0]
            on_value: rb.corners[0] = args[1]
        Label:
            text: 'corner 2'
        Slider:
            value: rb.corners[1]
            on_value: rb.corners[1] = args[1]
        Label:
            text: 'corner 3'
        Slider:
            value: rb.corners[2]
            on_value: rb.corners[2] = args[1]
        Label:
            text: 'corner 4'
        Slider:
            value: rb.corners[3]
            on_value: rb.corners[3] = args[1]
        Label:
            text: 'line width'
        Slider:
            value: 100
            on_value: rb.line_width = args[1]
            min: 1
            max: 100
        Label:
            text: 'width'
        Slider:
            value: rb.width
            on_value: rb.width = args[1]
            min: 100
            max: 500
        Label:
            text: 'height'
        Slider:
            value: rb.height
            on_value: rb.height = args[1]
            min: 100
            max: 500
        Label:
            text: 'resolution'
        Slider:
            value: rb.resolution
            on_value: rb.resolution = args[1]
            min: 10
            max: 100
<RoundedBox>:
    on_pos: self.compute_points()
    on_size: self.compute_points()
    on_corners: self.compute_points()
    on_resolution: self.compute_points()
    canvas:
        Line:
            # we don't care about the arguments, pass them to get
            # binding
            points: self.points
            width: self.line_width
            #loop: True
'''


class RoundedBox(Widget):
    corners = ListProperty([0, 0, 0, 0])
    line_width = NumericProperty(1)
    resolution = NumericProperty(100)
    points = ListProperty([])

    def compute_points(self, *args):
        self.points = []

        angle = - pi

        # up left corner
        x, y = self.x + self.corners[0], self.y + self.corners[0]
        while angle < - pi / 2.:
            angle += pi / self.resolution
            self.points.extend([x + cos(angle) * self.corners[0], y + sin(angle) * self.corners[0]])

        # up left corner
        x, y = self.right - self.corners[1], self.y + self.corners[1]
        while angle < 0:
            angle += pi / self.resolution
            self.points.extend([x + cos(angle) * self.corners[1], y + sin(angle) * self.corners[1]])

        # up left corner
        x, y = self.right - self.corners[2], self.top - self.corners[2]
        while angle < pi / 2.:
            angle += pi / self.resolution
            self.points.extend([x + cos(angle) * self.corners[2],  y + sin(angle) * self.corners[2]])

        # up left corner
        x, y = self.x + self.corners[3], self.top - self.corners[3]
        while angle < pi:
            angle += pi / self.resolution
            self.points.extend([x + cos(angle) * self.corners[3], y + sin(angle) * self.corners[3]])

        self.points.extend(self.points[:2])


class RoundedDemo(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    RoundedDemo().run()