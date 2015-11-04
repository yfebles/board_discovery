from math import pi, cos, sin
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget


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

        print(len(self.points))
