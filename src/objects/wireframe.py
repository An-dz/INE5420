from objects.geometricObject import Colour, Coordinate, GeometricObject


class Wireframe(GeometricObject):
    """A Wireframe consists of multiple points in space"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        points: tuple[Coordinate, ...],
    ) -> None:
        """
        Creates a Wireframe object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param points: A tuple of Coordinate tuples
        """
        if len(points) < 3:
            raise ValueError("Wireframe requires more than 2 points")

        super(Wireframe, self).__init__(name, "Wireframe", colour, points)
