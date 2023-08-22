from displayFile import DisplayFile
from objects.geometricObject import Coordinate


class Window:
    """The Window of the world"""
    def __init__(self, display_file: DisplayFile, min_coord: Coordinate, max_coord: Coordinate) -> None:
        self._x_coordinates = [min_coord[0], max_coord[0]]
        self._y_coordinates = [min_coord[1], max_coord[1]]
        self._display_file = display_file

    def getVisibleObjects(self):
        return self._display_file.objects()

    def getXW(self, xw: float) -> float:
        (xw_min, xw_max) = self._x_coordinates
        return (xw - xw_min) / (xw_max - xw_min)

    def getYW(self, yw: float) -> float:
        (yw_min, yw_max) = self._y_coordinates
        return 1 - ((yw - yw_min) / (yw_max - yw_min))

    def move(self, dx: float, dy: float) -> None:
        amount_x = (self._x_coordinates[1] - self._x_coordinates[0]) * dx
        amount_y = (self._y_coordinates[1] - self._y_coordinates[0]) * dy
        self._x_coordinates[0] += amount_x
        self._x_coordinates[1] += amount_x
        self._y_coordinates[0] += amount_y
        self._y_coordinates[1] += amount_y

    def zoom(self, times: float) -> None:
        self._x_coordinates[0] *= times
        self._x_coordinates[1] *= times
        self._y_coordinates[0] *= times
        self._y_coordinates[1] *= times
