import numpy as np
from numpy.typing import NDArray

from objects.bspline_curve import BSplineCurve
from objects.clipping import ClippingAlgo
from objects.geometricObject import Colour


class BSplineSurface(BSplineCurve):
    """
    A B-Spline Surface consists of multiple B-Spline curves at minimum 4x4
    """
    def __init__(
        self,
        name: str,
        colour: Colour,
        surface_points: NDArray[np.float64],
    ):
        if (
            len(surface_points.shape) != 3  # not 3D array
            or surface_points.shape[0] < 4  # less than 4 points on u
            or surface_points.shape[1] < 4  # less than 4 points on v
            or surface_points.shape[2] != 4  # Points don't have 4 coords
        ):
            raise ValueError(
                "B-Spline surfaces requires at minimum a 4x4 matrix of points",
            )

        self._points = surface_points
        d = 0.05
        self._n = int(1 / d)
        self._e = self._e_array(d)
        self._mbs: NDArray[np.float64] = np.array([
            [-1 / 6, 1 / 2, -1 / 2, 1 / 6],
            [1 / 2, -1, 1 / 2, 0],
            [-1 / 2, 0, 1 / 2, 0],
            [1 / 6, 2 / 3, 1 / 6, 0],
        ])

        super(BSplineCurve, self).__init__(
            name,
            "BSplineSurface",
            colour,
            list(self._points.reshape(
                (surface_points.shape[0] * surface_points.shape[1], 4),
            )),
            [],
        )

    def _build_curves(
        self,
        lines: list[NDArray[np.float64]],
        ddx: NDArray[np.float64],
        ddy: NDArray[np.float64],
        ddz: NDArray[np.float64],
        ddw: NDArray[np.float64],
    ) -> None:
        for _ in range(self._n + 1):
            self._fwd_diff_draw(
                self._n, lines,
                ddx[0][0], ddx[0][1], ddx[0][2], ddx[0][3],
                ddy[0][0], ddy[0][1], ddy[0][2], ddy[0][3],
                ddz[0][0], ddz[0][1], ddz[0][2], ddz[0][3],
                ddw[0][0], ddw[0][1], ddw[0][2], ddw[0][3],
            )
            ddx[0:3] = ddx[0:3] + ddx[1:4]
            ddy[0:3] = ddy[0:3] + ddy[1:4]
            ddz[0:3] = ddz[0:3] + ddz[1:4]
            ddw[0:3] = ddw[0:3] + ddw[1:4]

    def set_window_coordinates(
        self,
        win_coords_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        win_spline = self._points @ win_coords_matrix
        self._window_coordinates = []
        lines: list[NDArray[np.float64]] = []

        for j in range(4, win_spline.shape[1] + 1):
            for i in range(4, win_spline.shape[0] + 1):
                cx: NDArray[np.float64] = self._mbs @ win_spline[
                    i - 4:i,
                    j - 4:j,
                    0,
                ] @ self._mbs.T
                cy: NDArray[np.float64] = self._mbs @ win_spline[
                    i - 4:i,
                    j - 4:j,
                    1,
                ] @ self._mbs.T
                cz: NDArray[np.float64] = self._mbs @ win_spline[
                    i - 4:i,
                    j - 4:j,
                    2,
                ] @ self._mbs.T
                cw: NDArray[np.float64] = self._mbs @ win_spline[
                    i - 4:i,
                    j - 4:j,
                    3,
                ] @ self._mbs.T
                ddtx: NDArray[np.float64] = self._e @ cx @ self._e.T
                ddty: NDArray[np.float64] = self._e @ cy @ self._e.T
                ddtz: NDArray[np.float64] = self._e @ cz @ self._e.T
                ddtw: NDArray[np.float64] = self._e @ cw @ self._e.T
                ddsx = np.copy(ddtx.T)
                ddsy = np.copy(ddty.T)
                ddsz = np.copy(ddtz.T)
                ddsw = np.copy(ddtw.T)
                self._build_curves(lines, ddtx, ddty, ddtz, ddtw)
                self._build_curves(lines, ddsx, ddsy, ddsz, ddsw)

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
