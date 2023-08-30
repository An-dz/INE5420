from objects.geometricObject import GeometricObject


class DisplayFile:
    """The Display File holds all objetcts in the scene"""
    def __init__(self) -> None:
        self._objects: list[GeometricObject] = []

    def at(self, index: int) -> GeometricObject:
        return self._objects[index]

    def add(self, obj: GeometricObject) -> None:
        """
        Adds a geometric object into the display file

        @param obj: The geometric object to include into the world
        """
        self._objects.append(obj)

    def remove(self, index: int) -> None:
        """
        Removes a geometric object from the display file

        @param index: Index of the object, this should be equal to the list in the UI
        """
        self._objects.pop(index)

    def objects(self) -> list[GeometricObject]:
        """
        Returns the display file list so it can be iterated

        @returns: All objects in the display file
        """
        return self._objects
