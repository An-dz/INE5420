from typing import Literal

import numpy as np
from numpy.typing import NDArray

Coordinate = tuple[float, float]
"""Coordinate in 2D plane"""
NormalCoordinate = tuple[float, float, Literal[1]]
"""Coordinate in 2D plane with normalised Z"""
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


class GeometricObject:
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

    def set_window_coordinates(self, win_coords_matrix: NDArray[np.float64]) -> None:
        """
        Sets the window coordinates of the object

        @param win_coords_matrix: Matrix to transform the global coordinates
        into window coordinates
        """
        coords: NDArray[np.float64]
        self._window_coordinates = []

        for coords in self._coordinates:
            self._window_coordinates.append(coords @ win_coords_matrix)

    def transform(
        self,
        transform_matrix: NDArray[np.float64],
        window_matrix: NDArray[np.float64],
    ) -> None:
        """
        Transform the object throught a tranformation matrix

        @param transform_matrix: Transformation Matrix to apply on the obejct
        """
        self._coordinates = [c @ transform_matrix for c in self._coordinates]
        self._center = self._center @ transform_matrix
        self.set_window_coordinates(window_matrix)
