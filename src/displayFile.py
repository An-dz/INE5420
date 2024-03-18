from objects.geometricObject import GeometricObject


class DisplayFile:
    """The Display File holds all objetcts in the scene"""
    def __init__(self) -> None:
        self._objects: list[GeometricObject] = []

    def add(self, object: GeometricObject) -> None:
        self._objects.append(object)

    def objects(self):
        return self._objects
