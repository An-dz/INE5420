from objects.geometricObject import Colour, GeometricObject, NormalCoordinate


class Line(GeometricObject):
    """A line consists of two points in space"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        start_point: NormalCoordinate,
        end_point: NormalCoordinate,
    ) -> None:
        """
        Creates a Line object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param start_point: A starting Coordinate
        @param end_point: An ending Coordinate
        """
        if start_point == end_point:
            raise ValueError("Start and end points must be different")

        super(Line, self).__init__(
            name,
            "Line",
            colour,
            [start_point, end_point],
            [(start_point, end_point)],
        )
