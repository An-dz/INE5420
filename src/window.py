from displayFile import DisplayFile
from objects.geometricObject import Coordinate


class Window:
    """The Window of the world"""
    def __init__(self, display_file: DisplayFile, min_coord: Coordinate, max_coord: Coordinate) -> None:
        """
        Creates a window of the world

        @param display_file: The "world"
        @param min_coord: The initial small coordinates of the world rectangle
        @param max_coord: The initial large coordinates of the world rectangle
        """
        self._x_coordinates = [min_coord[0], max_coord[0]]
        self._y_coordinates = [min_coord[1], max_coord[1]]
        self._display_file = display_file

    def getVisibleObjects(self):
        """
        Returns the list of visible objects inside the window

        @note Not yet implemented, only returns the whole world

        @returns: The display file list
        """
        return self._display_file.objects()

    def getXW(self, xw: float) -> float:
        """
        Returns a normalised X coordinate

        @param xw: Point in the X axis to be normalised

        @returns: Point normalised to the window position
        """
        (xw_min, xw_max) = self._x_coordinates
        return (xw - xw_min) / (xw_max - xw_min)

    def getYW(self, yw: float) -> float:
        """
        Returns a normalised Y coordinate

        @param yw: Point in the Y axis to be normalised

        @returns: Point normalised to the window position
        """
        (yw_min, yw_max) = self._y_coordinates
        return 1 - ((yw - yw_min) / (yw_max - yw_min))

    def move(self, times_dx: float, times_dy: float) -> None:
        """
        Moves the window around

        @note This uses a percentage style so movement is consistent no matter the zoom

        @param times_dx: Percentage of the axis length to move
        @param times_dy: Percentage of the axis length to move
        """
        amount_x = (self._x_coordinates[1] - self._x_coordinates[0]) * times_dx
        amount_y = (self._y_coordinates[1] - self._y_coordinates[0]) * times_dy
        self._x_coordinates[0] += amount_x
        self._x_coordinates[1] += amount_x
        self._y_coordinates[0] += amount_y
        self._y_coordinates[1] += amount_y

    def zoom(self, times: float) -> None:
        """
        Scales the window size

        @param times: How many times the sizes should be adjusted
        """
        self._x_coordinates[0] *= times
        self._x_coordinates[1] *= times
        self._y_coordinates[0] *= times
        self._y_coordinates[1] *= times
