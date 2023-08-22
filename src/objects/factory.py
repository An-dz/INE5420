from objects.geometricObject import Coordinate, GeometricObject
from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe


class Factory:
    """Simple factory for generating the correct type of object based on input"""
    @staticmethod
    def createObject(name: str, points: tuple[Coordinate, ...]) -> GeometricObject:
        """
        Creates an appropriate geometric object according to the amount of points given

        @param name: A name to show in the object list
        @param points: A tuple of Coordinate tuples
        """
        if len(points) == 1:
            return Point(name, points[0])
        if len(points) == 2:
            return Line(name, points[0], points[1])
        return Wireframe(name, points)
