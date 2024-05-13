import numpy as np
from numpy.typing import NDArray

from displayFile import DisplayFile
from objects.geometricObject import Coordinate
from transformation import (
    rotate_around_x,
    rotate_around_y,
    rotate_matrix_x,
    rotate_matrix_y,
    rotate_matrix_z,
    scale_matrix,
    translate,
)


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
        self._wcenter = np.array(center)
        self._size = np.array(size)
        self._display_file = display_file
        self._rx: float = 0.
        """Rotation around X axis"""
        self._ry: float = 0.
        """Rotation around Y axis"""
        self._rz: float = 0.
        """Rotation around Z axis"""
        self._vpn = np.array([0, 0, 80000, 1])
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
        return (
            translate(-self._wcenter[0], -self._wcenter[1], -self._wcenter[2])
            @ rotate_matrix_x(self._rx * np.pi / 180)
            @ rotate_matrix_y(-self._ry * np.pi / 180)
            @ rotate_matrix_z(self._rz * np.pi / 180)
            @ scale_matrix(
                1 / (self._size[0] / 2),
                1 / (self._size[1] / 2),
                1,
            )
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
        amount = [
            self._size[0] * times_dx,
            self._size[1] * times_dy,
            0,
            1,
        ] @ rotate_matrix_x(
            -self._rx * np.pi / 180,
        ) @ rotate_matrix_y(
            -self._ry * np.pi / 180,
        ) @ rotate_matrix_z(
            -self._rz * np.pi / 180,
        )
        self._wcenter = self._wcenter + amount[:3]
        self.update_scn_matrix()

    def pan(self, dx: float, dy: float) -> None:
        """
        Moves the window around

        @note This uses a pixel style but adjusts with the window size
              so movement with mouse is smooth

        @param dx: amount in the X axis the mouse moved
        @param dy: amount in the Y axis the mouse moved
        """
        amount = [
            dx * self._size[0],
            -dy * self._size[1],
            0,
            1,
        ] @ rotate_matrix_x(
            -self._rx * np.pi / 180,
        ) @ rotate_matrix_y(
            -self._ry * np.pi / 180,
        ) @ rotate_matrix_z(
            -self._rz * np.pi / 180,
        )
        self._wcenter = self._wcenter + amount[:3]
        self.update_scn_matrix()

    def zoom(self, times: float) -> None:
        """
        Scales the window size

        @param times: How many times the sizes should be adjusted
        """
        self._size = np.array([self._size[0] * times, self._size[1] * times, 1])
        self.update_scn_matrix()

    def set_angles(self, rx: float, ry: float, rz: float) -> None:
        """
        Force set axis angles

        @param rx: Rotation around X axis angle
        @param ry: Rotation around Y axis angle
        @param rz: Rotation around Z axis angle
        """
        self._rx = rx
        self._ry = ry
        self._rz = rz
        self.update_scn_matrix()

    def roll(self, angle: float) -> None:
        """
        Rotates the window in the world around the window's Z axis

        @param angle: Angle in degrees to rotate the world around the Z axis
        """
        self._rz = (self._rz + angle) % 360
        self.update_scn_matrix()

    def pitch(self, angle: float) -> None:
        """
        Rotates the window in the world around the window's X axis

        @param angle: Angle in degrees to rotate the world around the X axis
        """
        self._rx = (self._rx + angle % 360)
        # new_angle = [0, 0, 1, 1] @ rotate_matrix_x(
        #     angle * np.pi / 180,
        # ) @ rotate_matrix_x(
        #     -self._rx * np.pi / 180,
        # ) @ rotate_matrix_y(
        #     self._ry * np.pi / 180,
        # )
        # x, y, z, _ = new_angle
        # invert_xz = -1 if z < 0 else 1
        # v = invert_xz * np.sqrt(y ** 2 + z ** 2)
        # teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
        # teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
        # print("{: .2f} {: .2f} {: .2f}".format(x, y, z))
        # print(teta_x / np.pi * 180)
        # print(teta_y / np.pi * 180)
        # full_circle_yz = 180 if z < 0 or z == 0 and y < 0 else 0
        # full_circle_xz = 180 if z < 0 or z == 0 and x < 0 else 0
        # self._rx = teta_x / np.pi * 180 + full_circle_yz
        # self._ry = teta_y / np.pi * 180 + full_circle_xz
        # print(self._rx)
        # print(self._ry)
        # print("--------")
        #############
        # self._vpn = self._vpn @ rotate_around_x(
        #     [
        #         (self._wcenter[0], self._wcenter[1], self._wcenter[2]),
        #         (self._vpn[0], self._vpn[1], self._vpn[2]),
        #     ],
        #     angle % 360 * np.pi / 180,
        # )
        # x, y, z, _ = self._vpn
        # invert_xz = -1 if z < 0 else 1
        # v = invert_xz * np.sqrt(y ** 2 + z ** 2)
        # teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
        # teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
        # print("{: .2f} {: .2f} {: .2f}".format(x, y, z))
        # full_circle_yz = 180 if z < 0 or z == 0 and y < 0 else 0
        # full_circle_xz = 180 if z < 0 or z == 0 and x < 0 else 0
        # self._rx = teta_x / np.pi * 180 + full_circle_yz
        # self._ry = teta_y / np.pi * 180 + full_circle_xz
        # print(self._rx)
        # print(self._ry)
        # print("--------")
        self.update_scn_matrix()

    def yaw(self, angle: float) -> None:
        """
        Rotates the window in the world around the window's Y axis

        @param angle: Angle in degrees to rotate the world around the Y axis
        """
        self._ry = (self._ry + angle % 360)
        # new_angle = [0, 0, 1, 1] @ rotate_matrix_y(
        #     angle * np.pi / 180,
        # ) @ rotate_matrix_x(
        #     -self._rx * np.pi / 180,
        # ) @ rotate_matrix_y(
        #     self._ry * np.pi / 180,
        # )
        # x, y, z, _ = new_angle
        # invert_xz = -1 if z < 0 else 1
        # v = invert_xz * np.sqrt(y ** 2 + z ** 2)
        # teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
        # teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
        # print("{: .2f} {: .2f} {: .2f}".format(x, y, z))
        # print(teta_x / np.pi * 180)
        # print(teta_y / np.pi * 180)
        # full_circle_yz = 180 if z < 0 or z == 0 and y < 0 else 0
        # full_circle_xz = 180 if z < 0 or z == 0 and x < 0 else 0
        # self._rx = teta_x / np.pi * 180 + full_circle_yz
        # self._ry = teta_y / np.pi * 180 + full_circle_xz
        # print(self._rx)
        # print(self._ry)
        # print("--------")
        #############
        # self._vpn = self._vpn @ rotate_around_y(
        #     [
        #         (self._wcenter[0], self._wcenter[1], self._wcenter[2]),
        #         (self._vpn[0], self._vpn[1], self._vpn[2]),
        #     ],
        #     angle % 360 * np.pi / 180,
        # )
        # x, y, z, _ = self._vpn
        # invert_xz = -1 if z < 0 else 1
        # v = invert_xz * np.sqrt(y ** 2 + z ** 2)
        # teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
        # teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
        # print("{: .2f} {: .2f} {: .2f}".format(x, y, z))
        # full_circle_yz = 180 if z < 0 or z == 0 and y < 0 else 0
        # full_circle_xz = 180 if z < 0 or z == 0 and x < 0 else 0
        # self._rx = teta_x / np.pi * 180 + full_circle_yz
        # self._ry = teta_y / np.pi * 180 + full_circle_xz
        # print(self._rx)
        # print(self._ry)
        # print("--------")
        # self.update_scn_matrix()
        #############
        # x, y, z, _ = self._vpn
        # v = np.sqrt(y ** 2 + z ** 2)
        # teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
        # teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
        # print(self._vpn)
        # full_circle_yz = 180 if z < 0 or z == 0 and y < 0 else 0
        # full_circle_xz = 360 if x < 0 and z >= 0 else 0
        # invert_xz = -1 if z < 0 else 1
        # self._rx = teta_x / np.pi * 180 + full_circle_yz
        # self._ry = invert_xz * teta_y / np.pi * 180 + full_circle_xz + full_circle_yz
        # print(self._rx)
        # print(self._ry)
        # print("--------")
        self.update_scn_matrix()
