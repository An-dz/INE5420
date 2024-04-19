import numpy as np
from numpy.typing import NDArray

from objects.clipping import ClippingAlgo
from objects.geometricObject import GeometricObject


class DisplayFile:
    """The Display File holds all objetcts in the scene"""
    def __init__(self, clipping_algorithm: ClippingAlgo) -> None:
        """
        Creates the Display File
        """
        self._clipping_algorithm = clipping_algorithm
        self._objects: list[GeometricObject] = []
        self._scn_matrix: NDArray[np.float64] = np.array(
            [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
        )

    def at(self, index: int) -> GeometricObject:
        """
        Return the object at the requested index

        @param index: Index of the object in the display file list

        @returns: Geometric object in display file at provided index
        """
        return self._objects[index]

    def add(self, obj: GeometricObject) -> None:
        """
        Adds a geometric object into the display file

        @param obj: The geometric object to include into the world
        """
        self._objects.append(obj)
        obj.set_window_coordinates(self._scn_matrix, self._clipping_algorithm)

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

    def set_scn_matrix(self, matrix: NDArray[np.float64]) -> None:
        """
        Sets the matrix that transform global coordinates into SCN coordinates

        @param matrix: Matrix to transform the global coordinates into SCN coordinates
        """
        self._scn_matrix = matrix
        for obj in self._objects:
            obj.set_window_coordinates(matrix, self._clipping_algorithm)

    def set_clipping_algorithm(self, clipping_algorithm: ClippingAlgo) -> None:
        self._clipping_algorithm = clipping_algorithm
        for obj in self._objects:
            obj.set_window_coordinates(self._scn_matrix, self._clipping_algorithm)
