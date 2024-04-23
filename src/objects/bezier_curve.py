import math
import numpy as np
from numpy.typing import NDArray

from objects.clipping import ClippingAlgo
from objects.geometricObject import Colour, GeometricObject, VerticesList


class BezierCurve(GeometricObject):
    """
    A Bezier Curve consists of multiple points identifying the Pi points in the curve
    """
    def __init__(
        self,
        name: str,
        colour: Colour,
        curve_points: VerticesList,
    ):
        if len(curve_points) < 4 and len(curve_points) % 3 != 1:
            raise ValueError(
                "Bézier curves requires a minimum of 4 points and then 3 more per segment",
            )

        super(BezierCurve, self).__init__(
            name,
            "BezierCurve",
            colour,
            curve_points,
            [curve_points],
        )

    def set_window_coordinates(
        self,
        win_coords_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        win_bezier = [coords @ win_coords_matrix for coords in self._coordinates[0]]
        self._window_coordinates = []
        lines = []

        for i in range(0, len(win_bezier) - 1, 3):
            p1, p2, p3, p4 = win_bezier[i:i + 4]
            prev_vertex = np.array((0, 0, 1))
            points_diff = np.abs(p4 - p1)
            # base smoothness is the amount of lines for half screen
            base_smoothness = 25
            # adjust smoothness according to zoom
            smoothness = math.ceil(points_diff.max() * base_smoothness)

            for t_int in range(smoothness):
                t = (t_int + 1) / smoothness
                v = (
                    1 - 3 * t + 3 * t ** 2 - t ** 3,
                    3 * t - 6 * t ** 2 + 3 * t ** 3,
                    3 * t ** 2 - 3 * t ** 3,
                    t ** 3,
                )
                new_vertex = p1 * v[0] + p2 * v[1] + p3 * v[2] + p4 * v[3]
                new_vertex[2] = 1

                if t_int > 0:
                    lines.append(np.array([prev_vertex, new_vertex]))

                prev_vertex = new_vertex

        for win_coords in lines:
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
