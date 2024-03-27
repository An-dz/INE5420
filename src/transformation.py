import numpy as np
from numpy.typing import NDArray


def translate_matrix(x: float, y: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate translation matrix

    @param x: Amount to translate on the X axis
    @param y: Amount to translate on the Y axis

    @returns: 3x3 Numpy array/matrix
    """
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1],
    ])


def scale_matrix(x: float, y: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate scale matrix

    @param x: Amount to scale on the X axis
    @param y: Amount to scale on the Y axis

    @returns: 3x3 Numpy array/matrix
    """
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1],
    ])


def rotate_matrix(teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate rotation matrix

    @param x: Amount to translate on the X axis
    @param y: Amount to translate on the Y axis

    @returns: 3x3 Numpy array/matrix
    """
    cos = np.cos(teta)
    sin = np.sin(teta)
    return np.array([
        [cos, -sin, 0],
        [sin, cos, 0],
        [0, 0, 1],
    ])


def translate(dx: float, dy: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for translating

    @param dx: Amount to translate on the X axis
    @param dy: Amount to translate on the Y axis

    @returns: 3x3 transforrmation matrix as a numpy array/matrix
    """
    return translate_matrix(dx, dy)


def scale(center: NDArray[np.float64], sx: float, sy: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    scaling around a central point

    @param center: Central point to scale around
    @param sx: Amount to scale on the X axis
    @param sy: Amount to scale on the Y axis

    @returns: 3x3 transforrmation matrix as a numpy array/matrix
    """
    dx = center[0]
    dy = center[1]
    return translate_matrix(-dx, -dy) @ scale_matrix(sx, sy) @ translate_matrix(dx, dy)


def rotate_around(center: NDArray[np.float64], teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    rotating around a central point

    @param center: Central point to rotate around
    @param teta: Angle to rotate in radians

    @returns: 3x3 transforrmation matrix as a numpy array/matrix
    """
    dx = center[0]
    dy = center[1]
    return translate_matrix(-dx, -dy) @ rotate_matrix(teta) @ translate_matrix(dx, dy)
