import math
import numpy as np
from numpy.typing import NDArray

from objects.clipping import ClippingAlgo
from objects.geometricObject import Colour, GeometricObject, VerticesList


class BezierSurface(GeometricObject):
    """
    A Bezier Curve consists of multiple points identifying the Pi points in the curve
    """
    def __init__(
        self,
        name: str,
        colour: Colour,
        curve_points: VerticesList,
    ):
        if len(curve_points) != 16:
            raise ValueError("Bézier surfaces require exactly 16 points")

        self._points = np.array(curve_points).reshape(4, 4, 4)

        super(BezierSurface, self).__init__(
            name,
            "BezierSurface",
            colour,
            curve_points,
            [],
        )

    def bezier_line(
        self,
        lines: list[NDArray[np.float64]],
        smoothness: int,
        bezier_points: NDArray[np.float64],
    ) -> None:
        prev_vertex = np.array([])

        for s_int in range(smoothness + 1):
            s = s_int / smoothness
            sv = np.array([
                1 - 3 * s + 3 * s ** 2 - s ** 3,
                3 * s - 6 * s ** 2 + 3 * s ** 3,
                3 * s ** 2 - 3 * s ** 3,
                s ** 3,
            ])

            for t_int in range(smoothness + 1):
                t = t_int / smoothness
                tv = np.array([
                    1 - 3 * t + 3 * t ** 2 - t ** 3,
                    3 * t - 6 * t ** 2 + 3 * t ** 3,
                    3 * t ** 2 - 3 * t ** 3,
                    t ** 3,
                ])
                new_vertex = np.array([
                    sv @ bezier_points[:, :, 0] @ tv,
                    sv @ bezier_points[:, :, 1] @ tv,
                    sv @ bezier_points[:, :, 2] @ tv,
                    sv @ bezier_points[:, :, 3] @ tv,
                ])

                if t_int > 0:
                    lines.append(np.array([prev_vertex, new_vertex]))

                prev_vertex = new_vertex

    def set_window_coordinates(
        self,
        win_coords_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        win_bezier = self._points @ win_coords_matrix
        # print(win_bezier[0])
        # print(win_bezier / win_bezier[:, :, -1])
        # win_bezier = win_bezier / win_bezier[:, :, -1]
        self._window_coordinates = []
        lines: list[NDArray[np.float64]] = []

        # p1, _, _, p4 = win_bezier[0][0:4]
        # points_diff = np.abs(p4[:2] - p1[:2])
        # base smoothness is the amount of lines for half screen
        # base_smoothness = 25
        # adjust smoothness according to zoom
        # smoothness = max(2, math.ceil(points_diff.max() * base_smoothness))
        smoothness = 25
        self.bezier_line(lines, smoothness, win_bezier)
        self.bezier_line(lines, smoothness, win_bezier.transpose(1, 0, 2))
        np_lines = np.array(lines)
        np_lines = np_lines / np_lines[:, :, -1:]

        for win_coords in np_lines:
            obj = None

            if line_clip == ClippingAlgo.Points:
                obj = self.clip_by_point(win_coords)
            elif line_clip == ClippingAlgo.CohenSutherland:
                obj = self.clip_cohen_sutherland(win_coords)
            elif line_clip == ClippingAlgo.LiangBarsky:
                obj = self.clip_liang_barsky(win_coords)
            elif line_clip == ClippingAlgo.NichollLeeNicholl:
                obj = self.clip_nicholl_lee_nicholl(win_coords)

            if obj is not None:
                self._window_coordinates.append(obj)

    def get_coordinates(self) -> list[NDArray[np.float64]]:
        """
        Returns the global coordinates of each point of the object

        @returns: Tuple of global coordinates for each point
        """
        return [self._points]

    def transform(
        self,
        transform_matrix: NDArray[np.float64],
        window_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        """
        Transform the object throught a tranformation matrix

        @param transform_matrix: Transformation Matrix to apply on the obejct
        """
        self._points = self._points @ transform_matrix
        self._center = self._center @ transform_matrix
        self.set_window_coordinates(window_matrix, line_clip)
