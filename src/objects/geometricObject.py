Coordinate = tuple[float, float]
"""Coordinate in 2D plane"""

class GeometricObject:
    """Geometric Object is the base class for all objects that can be drawn"""
    i = 0
    """Singleton for hashing / static property"""

    def __init__(self, name: str, obj_type: str, coordinates: list[Coordinate]) -> None:
        self._name = name
        self._type = obj_type
        self._coordinates = coordinates
        self._hash = hash((self.getType(), self.getName(), GeometricObject.i))
        GeometricObject.i += 1

    def __hash__(self) -> int:
        return self._hash

    def getType(self) -> str:
        return self._type

    def getName(self) -> str:
        return self._name

    def getCoordinates(self) -> list[Coordinate]:
        return self._coordinates
