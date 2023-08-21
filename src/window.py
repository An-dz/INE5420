from displayFile import DisplayFile
from objects.geometricObject import Coordinate
from objects.line import Line
from objects.point import Point


class Window:
    """The Window of the world"""
    def __init__(self, min_coord: Coordinate, max_coord: Coordinate) -> None:
        self.coordinates = [min_coord, max_coord]

        self.display_file = DisplayFile()
        self.display_file.add(Line("test", (0,0), (150,150)))
        self.display_file.add(Point("test", (0,150)))

    def zoom(self):
        pass

    def translate(self):
        pass

    def getVisibleObjects(self):
        return self.display_file.objects()
