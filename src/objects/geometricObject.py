from typing import Literal

import numpy as np
from numpy.typing import NDArray

from objects.clipping import Clipping, ClippingAlgo

Coordinate = tuple[float, float, float]
"""Coordinate in 3D plane"""
NormalCoordinate = tuple[float, float, float, Literal[1]]
"""Coordinate in 3D plane with normalised W"""
VerticesList = list[NormalCoordinate]
"""List of vertices in Normalised Coordinates"""
ObjectsList = list[tuple[NormalCoordinate, ...]]
"""
List of the basic types (points, edges & faces) as tuples of Normalised Coordinates

 - Points are represented as a tuple of single values  
 - Edges are represented as tuples of two values  
 - Faces are represented as tuples of more than two values
"""
Colour = tuple[int, int, int]
"""A RGB colour tuple, each value goes from 0 to 255"""


class GeometricObject(Clipping):
    """Geometric Object is the base class for all objects that can be drawn"""
    def __init__(
        self,
        name: str,
        obj_type: str,
        colour: Colour,
        vertices: VerticesList,
        obj_list: ObjectsList,
    ) -> None:
        """
        Creates a Geometric Object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param obj_type: A string representing the specific type of the object
        @param colour: A colour to draw the object
        @param obj_list: A list of tuples of NormalCoordinates
        """
        self._name = name
        self._type = obj_type
        self._colour = colour
        self._coordinates: list[NDArray[np.float64]] = [np.array(c) for c in obj_list]
        self._window_coordinates: list[NDArray[np.float64]] = []
        unique_vertices = np.unique(np.array(vertices), axis=0)
        self._center = unique_vertices.sum(axis=0) / len(unique_vertices)

    def get_type(self) -> str:
        """
        Returns the type of the object

        @note The type is the class name of the object

        @returns: Type as a string
        """
        return self._type

    def get_name(self) -> str:
        """
        Returns the name given to the object

        @returns: Name as a string
        """
        return self._name

    def get_colour(self) -> Colour:
        """
        Returns the colour that was set for this object to be painted

        @return: RGB tuple
        """
        return self._colour

    def get_coordinates(self) -> list[NDArray[np.float64]]:
        """
        Returns the global coordinates of each point of the object

        @returns: Tuple of global coordinates for each point
        """
        return self._coordinates

    def get_window_coordinates(self) -> list[NDArray[np.float64]]:
        """
        Returns the window coordinates of each point of the object

        @returns: Tuple of window coordinates for each point
        """
        return self._window_coordinates

    def get_center(self) -> NDArray[np.float64]:
        """
        Returns the center point of the object

        @returns: Coordinates of the center
        """
        return self._center

    def set_window_coordinates(
        self,
        win_coords_matrix: NDArray[np.float64],
        line_clip: ClippingAlgo,
    ) -> None:
        """
        Sets the window coordinates of the object

        @param win_coords_matrix: Matrix to transform the global coordinates
        into window coordinates
        """
        coords: NDArray[np.float64]
        self._window_coordinates = []

        for coords in self._coordinates:
            win_coords = []

            for c in coords:
                normal_c = c @ win_coords_matrix
                if normal_c[2] > 0:
                    normal_c = normal_c / normal_c[3]
                    win_coords.append(normal_c)

            vertex_count = len(win_coords)
            obj = None
            np_win_coords = np.array(win_coords)

            if vertex_count == 1:  # point
                obj = self.clip_by_point(np_win_coords)
            elif vertex_count == 2:  # edge
                if line_clip == ClippingAlgo.Points:
                    obj = self.clip_by_point(np_win_coords)
                elif line_clip == ClippingAlgo.CohenSutherland:
                    obj = self.clip_cohen_sutherland(np_win_coords)
                elif line_clip == ClippingAlgo.LiangBarsky:
                    obj = self.clip_liang_barsky(np_win_coords)
                elif line_clip == ClippingAlgo.NichollLeeNicholl:
                    obj = self.clip_nicholl_lee_nicholl(np_win_coords)
            else:  # face
                obj = self.clip_sutherland_hodgeman(np_win_coords)

            if obj is not None:
                self._window_coordinates.append(obj)

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
        self._coordinates = [c @ transform_matrix for c in self._coordinates]
        self._center = self._center @ transform_matrix
        self.set_window_coordinates(window_matrix, line_clip)
