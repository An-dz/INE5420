import numpy as np
from numpy.typing import NDArray

Coordinate = tuple[float, float]
"""Coordinate in 2D plane"""
Colour = tuple[int, int, int]
"""A RGB colour tuple, each value goes from 0 to 255"""


class GeometricObject:
    """Geometric Object is the base class for all objects that can be drawn"""
    def __init__(
        self,
        name: str,
        obj_type: str,
        colour: Colour,
        coordinates: tuple[Coordinate, ...],
    ) -> None:
        """
        Creates a Geometric Object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param obj_type: A string representing the specific type of the object
        @param colour: A colour to draw the object
        @param coordinates: A tuple of Coordinate tuples
        """
        self._name = name
        self._type = obj_type
        self._colour = colour
        self._coordinates: NDArray[np.float64] = np.array(
            [[*coord, 1] for coord in coordinates],
        )
        self._window_coordinates: NDArray[np.float64] = np.array([])

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

    def get_coordinates(self) -> NDArray[np.float64]:
        """
        Returns the global coordinates of each point of the object

        @returns: Tuple of global coordinates for each point
        """
        return self._coordinates

    def get_window_coordinates(self) -> NDArray[np.float64]:
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
        return np.sum(self._coordinates, axis=0) / len(self._coordinates)

    def set_window_coordinates(self, win_coords_matrix: NDArray[np.float64]) -> None:
        """
        Sets the window coordinates of the object

        @param win_coords_matrix: Matrix to transform the global coordinates
        into window coordinates
        """
        self._window_coordinates = self._coordinates @ win_coords_matrix

    def transform(
        self,
        transform_matrix: NDArray[np.float64],
        window_matrix: NDArray[np.float64],
    ) -> None:
        """
        Transform the object throught a tranformation matrix

        @param transform_matrix: Transformation Matrix to apply on the obejct
        """
        self._coordinates = self._coordinates @ transform_matrix
        self.set_window_coordinates(window_matrix)
