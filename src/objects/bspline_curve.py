import numpy as np
from numpy.typing import NDArray

from objects.clipping import ClippingAlgo
from objects.geometricObject import Colour, GeometricObject, VerticesList


class BSplineCurve(GeometricObject):
    """
    A B-Spline Curve consists of multiple points identifying the Pi points in the curve
    """
    def __init__(
        self,
        name: str,
        colour: Colour,
        curve_points: VerticesList,
    ):
        if len(curve_points) < 4:
            raise ValueError(
                "B-Spline curves requires a minimum of 4 points",
            )
        d = 0.01
        self._n = int(1 / d)
        self._e = self._e_array(d)

        super(BSplineCurve, self).__init__(
            name,
            "BSplineCurve",
            colour,
            curve_points,
            [curve_points],
        )

    def _e_array(self, d: float) -> NDArray[np.float64]:
        return np.array([
            [0, 0, 0, 1],
            [d ** 3, d ** 2, d, 0],
            [6 * d ** 3, 2 * d ** 2, 0, 0],
            [6 * d ** 3, 0, 0, 0],
        ])

    def _fwd_diff_draw(
        self,
        n: int,
        x: float,
        dx: float,
        d2x: float,
        d3x: float,
        y: float,
        dy: float,
        d2y: float,
        d3y: float,
    ) -> list[NDArray[np.float64]]:
        i = 1
        x_old = x
        y_old = y
        lines: list[NDArray[np.float64]] = []

        while i < n:
            i += 1
            x = x + dx
            dx = dx + d2x
            d2x = d2x + d3x
            y = y + dy
            dy = dy + d2y
            d2y = d2y + d3y
            lines.append(np.array([(x_old, y_old, 1), (x, y, 1)]))
            x_old = x
            y_old = y

        return lines

    def set_window_coordinates(
        self,
        win_coords_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        win_spline = [coords @ win_coords_matrix for coords in self._coordinates[0]]
        self._window_coordinates = []
        lines: list[NDArray[np.float64]] = []

        for i in range(4, len(win_spline) + 1):
            p1, p2, p3, p4 = win_spline[i - 4:i]
            gx: NDArray[np.float64] = np.array([p1[0], p2[0], p3[0], p4[0]])
            gy: NDArray[np.float64] = np.array([p1[1], p2[1], p3[1], p4[1]])
            mbs: NDArray[np.float64] = np.array([
                [-1 / 6, 1 / 2, -1 / 2, 1 / 6],
                [1 / 2, -1, 1 / 2, 0],
                [-1 / 2, 0, 1 / 2, 0],
                [1 / 6, 2 / 3, 1 / 6, 0],
            ])
            cx: NDArray[np.float64] = mbs @ gx
            cy: NDArray[np.float64] = mbs @ gy
            x: NDArray[np.float64] = self._e @ cx
            y: NDArray[np.float64] = self._e @ cy
            lines = self._fwd_diff_draw(
                self._n, x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3],
            )

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
