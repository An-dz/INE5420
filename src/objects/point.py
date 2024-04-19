from objects.geometricObject import Colour, GeometricObject, NormalCoordinate


class Point(GeometricObject):
    """A single point in space"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        coordinate: NormalCoordinate,
    ) -> None:
        """
        Creates a Point object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param point: The Coordinates of the point
        """
        super(Point, self).__init__(name, "Point", colour, (coordinate,), [(coordinate,)])
