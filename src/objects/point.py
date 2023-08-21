from objects.geometricObject import Coordinate, GeometricObject


class Point(GeometricObject):
    """A single point in space"""
    def __init__(self, name: str, coordinate: Coordinate) -> None:
        super(Point, self).__init__(name, "Point", (coordinate,))
