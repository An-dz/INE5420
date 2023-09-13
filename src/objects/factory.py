from objects.geometricObject import Colour, NormalCoordinate, GeometricObject
from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe


class Factory:
    """Simple factory for generating the correct type of object based on input"""
    @staticmethod
    def create_object(
        name: str,
        colour: Colour,
        points: list[tuple[NormalCoordinate, NormalCoordinate]],
    ) -> GeometricObject:
        """
        Creates an appropriate geometric object according to the amount of points given

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param points: A list of line segments,
        if the initial and final points are equal its a point
        """
        if len(points) == 1:
            if points[0][0] == points[0][1]:
                return Point(name, colour, points[0][0])
            return Line(name, colour, points[0][0], points[0][1])
        return Wireframe(name, colour, points)
