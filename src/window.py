from displayFile import DisplayFile
from objects.geometricObject import Coordinate
from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe


class Window:
    """The Window of the world"""
    def __init__(self, min_coord: Coordinate, max_coord: Coordinate) -> None:
        self._x_coordinates = [min_coord[0], max_coord[0]]
        self._y_coordinates = [min_coord[1], max_coord[1]]

        self.display_file = DisplayFile()
        self.display_file.add(Line("test", (0,0), (150,150)))
        self.display_file.add(Point("test", (0,150)))
        self.display_file.add(Wireframe("square", ((20,100), (40,100), (40,80), (20,80), (20,100))))

    def getVisibleObjects(self):
        return self.display_file.objects()

    def getXW(self, xw: float) -> float:
        (xw_min, xw_max) = self._x_coordinates
        return (xw - xw_min) / (xw_max - xw_min)

    def getYW(self, yw: float) -> float:
        (yw_min, yw_max) = self._y_coordinates
        return 1 - ((yw - yw_min) / (yw_max - yw_min))

    def move(self, dx: float, dy: float) -> None:
        self._x_coordinates[0] += dx
        self._x_coordinates[1] += dx
        self._y_coordinates[0] += dy
        self._y_coordinates[1] += dy

    def zoom(self, times: float) -> None:
        self._x_coordinates[0] *= times
        self._x_coordinates[1] *= times
        self._y_coordinates[0] *= times
        self._y_coordinates[1] *= times
