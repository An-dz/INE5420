import numpy as np
from numpy.typing import NDArray

from displayFile import DisplayFile
from objects.geometricObject import Coordinate
from transformation import rotate_matrix, scale_matrix, translate


class Window:
    """The Window of the world"""
    def __init__(
        self,
        display_file: DisplayFile,
        center: Coordinate,
        size: Coordinate,
    ) -> None:
        """
        Creates a window of the world

        @param display_file: The "world"
        @param min_coord: The initial small coordinates of the world rectangle
        @param max_coord: The initial large coordinates of the world rectangle
        """
        self._wcenter = center
        self._size = size
        self._display_file = display_file
        self._angle: float = 0.
        self.update_scn_matrix()

    def get_visible_objects(self):
        """
        Returns the list of visible objects inside the window

        @note Not yet implemented, only returns the whole world

        @returns: The display file list
        """
        return self._display_file.objects()

    def get_xw(self, xw: float) -> float:
        """
        Returns a normalised X coordinate

        @param xw: Point in the X axis to be normalised

        @returns: Point normalised to the window position
        """
        return (xw + 1) / 2

    def get_yw(self, yw: float) -> float:
        """
        Returns a normalised Y coordinate

        @param yw: Point in the Y axis to be normalised

        @returns: Point normalised to the window position
        """
        return 1 - ((yw + 1) / 2)

    def get_scn_matrix(self) -> NDArray[np.float64]:
        """
        Generates the SCN transformation matrix for the current params

        @returns: SCN transformation matrix as numpy array
        """
        return translate(
            -self._wcenter[0],
            -self._wcenter[1],
        ) @ rotate_matrix(
            self._angle * np.pi / 180,
        ) @ scale_matrix(
            1 / (self._size[0] / 2),
            1 / (self._size[1] / 2),
        )

    def update_scn_matrix(self) -> None:
        """
        Updates the SCN transformation matrix for the current params
        """
        self._display_file.set_scn_matrix(
            self.get_scn_matrix(),
        )

    def move(self, times_dx: float, times_dy: float) -> None:
        """
        Moves the window around

        @note This uses a percentage style so movement is consistent no matter the zoom

        @param times_dx: Percentage of the axis length to move
        @param times_dy: Percentage of the axis length to move
        """
        amount = np.array(
            [
                self._size[0] * times_dx,
                self._size[1] * times_dy,
                1,
            ] @ rotate_matrix(-self._angle * np.pi / 180),
        )
        self._wcenter = (self._wcenter[0] + amount[0], self._wcenter[1] + amount[1])
        self.update_scn_matrix()

    def pan(self, dx: float, dy: float) -> None:
        """
        Moves the window around

        @note This uses a pixel style but adjusts with the window size
              so movement with mouse is smooth

        @param dx: amount in the X axis the mouse moved
        @param dy: amount in the Y axis the mouse moved
        """
        amount = np.array(
            [
                dx * self._size[0],
                -dy * self._size[1],
                1,
            ] @ rotate_matrix(-self._angle * np.pi / 180),
        )
        self._wcenter = (self._wcenter[0] + amount[0], self._wcenter[1] + amount[1])
        self.update_scn_matrix()

    def zoom(self, times: float) -> None:
        """
        Scales the window size

        @param times: How many times the sizes should be adjusted
        """
        self._size = (self._size[0] * times, self._size[1] * times)
        self.update_scn_matrix()

    def rotate(self, angle: float) -> None:
        """
        Rotates the window in the world

        @param angle: Angle in degrees to rotate the world around the window center
        """
        if angle != 0:
            self._angle = (self._angle + angle) % 360
        else:
            self._angle = 0
        self.update_scn_matrix()
