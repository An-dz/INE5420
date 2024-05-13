import numpy as np
from numpy.typing import NDArray

from objects.geometricObject import Coordinate


def translate_matrix(x: float, y: float, z: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate translation matrix

    @param x: Amount to translate on the X axis
    @param y: Amount to translate on the Y axis

    @returns: 4x4 Numpy array/matrix
    """
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1],
    ])


def scale_matrix(x: float, y: float, z: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate scale matrix

    @param x: Amount to scale on the X axis
    @param y: Amount to scale on the Y axis

    @returns: 4x4 Numpy array/matrix
    """
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1],
    ])


def rotate_matrix_x(teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate rotation matrix

    @param teta: Angle to rotate in radians

    @returns: 4x4 Numpy array/matrix
    """
    cos = np.cos(teta)
    sin = np.sin(teta)
    return np.array([
        [1, 0, 0, 0],
        [0, cos, sin, 0],
        [0, -sin, cos, 0],
        [0, 0, 0, 1],
    ])


def rotate_matrix_y(teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate rotation matrix

    @param teta: Angle to rotate in radians

    @returns: 4x4 Numpy array/matrix
    """
    cos = np.cos(teta)
    sin = np.sin(teta)
    return np.array([
        [cos, 0, -sin, 0],
        [0, 1, 0, 0],
        [sin, 0, cos, 0],
        [0, 0, 0, 1],
    ])


def rotate_matrix_z(teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate rotation matrix

    @param teta: Angle to rotate in radians

    @returns: 4x4 Numpy array/matrix
    """
    cos = np.cos(teta)
    sin = np.sin(teta)
    return np.array([
        [cos, sin, 0, 0],
        [-sin, cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def translate(dx: float, dy: float, dz: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for translating

    @param dx: Amount to translate on the X axis
    @param dy: Amount to translate on the Y axis

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    return translate_matrix(dx, dy, dz)


def scale(
    center: NDArray[np.float64],
    sx: float,
    sy: float,
    sz: float,
) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    scaling around a central point

    @param center: Central point to scale around
    @param sx: Amount to scale on the X axis
    @param sy: Amount to scale on the Y axis

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    dx = center[0]
    dy = center[1]
    dz = center[2]
    return (
        translate_matrix(-dx, -dy, -dz)
        @ scale_matrix(sx, sy, sz)
        @ translate_matrix(dx, dy, dz)
    )


def rotate_around(
    axis: list[Coordinate],
    rotation: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    rotating around an arbitrary axis

    @param center: Central point to rotate around
    @param teta: Angle to rotate in radians

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    dx = axis[0][0]
    dy = axis[0][1]
    dz = axis[0][2]
    x = axis[1][0] - dx
    y = axis[1][1] - dy
    z = axis[1][2] - dz
    v = np.sqrt(y ** 2 + z ** 2)
    teta_x = np.pi / 2 if z == 0 else np.arctan(y / z)
    teta_y = np.pi / 2 if v == 0 else np.arctan(x / v)
    return (
        translate_matrix(-dx, -dy, -dz)
        @ rotate_matrix_x(teta_x)
        @ rotate_matrix_y(-teta_y)
        @ rotation
        @ rotate_matrix_y(teta_y)
        @ rotate_matrix_x(-teta_x)
        @ translate_matrix(dx, dy, dz)
    )


def rotate_around_x(axis: list[Coordinate], teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    rotating around an arbitrary axis

    @param center: Central point to rotate around
    @param teta: Angle to rotate in radians

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    return rotate_around(axis, rotate_matrix_x(teta))


def rotate_around_y(axis: list[Coordinate], teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    rotating around an arbitrary axis

    @param center: Central point to rotate around
    @param teta: Angle to rotate in radians

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    return rotate_around(axis, rotate_matrix_y(teta))


def rotate_around_z(axis: list[Coordinate], teta: float) -> NDArray[np.float64]:
    """
    Create a homogeneous coordinate transformation matrix for
    rotating around an arbitrary axis

    @param center: Central point to rotate around
    @param teta: Angle to rotate in radians

    @returns: 4x4 transformation matrix as a numpy array/matrix
    """
    return rotate_around(axis, rotate_matrix_z(teta))
