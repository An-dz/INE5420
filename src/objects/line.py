from objects.geometricObject import Coordinate, GeometricObject


class Line(GeometricObject):
    """A line consists of two points in space"""
    def __init__(
        self,
        name: str,
        colour: tuple[int, int, int],
        start_point: Coordinate,
        end_point: Coordinate,
    ) -> None:
        """
        Creates a Line object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param start_point: A starting Coordinate
        @param colour: A colour to draw the object
        @param end_point: An ending Coordinate
        """
        super(Line, self).__init__(name, "Line", colour, (start_point, end_point))
