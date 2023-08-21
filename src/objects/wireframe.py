from objects.geometricObject import Coordinate, GeometricObject


class Wireframe(GeometricObject):
    """A Wireframe consists of multiple points in space"""
    def __init__(self, name: str, points: tuple[Coordinate, ...]) -> None:
        if len(points) < 3:
            raise ValueError("Wireframe requires more than 2 points")

        super(Wireframe, self).__init__(name, "Wireframe", points)
