Coordinate = tuple[float, float]
"""Coordinate in 2D plane"""


class GeometricObject:
    """Geometric Object is the base class for all objects that can be drawn"""
    def __init__(
        self,
        name: str,
        obj_type: str,
        colour: tuple[int, int, int],
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

    def get_colour(self) -> tuple[int, int, int]:
        return self._colour

    def get_coordinates(self) -> tuple[Coordinate, ...]:
        """
        Returns the coordinates of each point of the object

        @returns: Tuple of coordinates for each point
        """
        return self._coordinates
