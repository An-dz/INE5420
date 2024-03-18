from objects.geometricObject import Coordinate, GeometricObject


class Line(GeometricObject):
    """A line consists of two points in space"""
    def __init__(self, name: str, start_point: Coordinate, end_point: Coordinate) -> None:
        super(Line, self).__init__(name, "Line", [ start_point, end_point ])
