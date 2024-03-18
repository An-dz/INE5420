from PyQt6 import QtGui, QtWidgets
from objects.geometricObject import Coordinate
from window import Window


class Viewport:
    """docstring for Viewport"""
    def __init__(self, window: Window, size: Coordinate):
        self._window = window
        self._size = size
        self._graphic_scene = QtWidgets.QGraphicsScene()
        drawing_color = QtGui.QColor(246, 158, 67)
        self._pen = QtGui.QPen(drawing_color)
        self._pen.setWidth(2)
        self._brush = QtGui.QBrush(drawing_color)

    def getScene(self) -> QtWidgets.QGraphicsScene:
        return self._graphic_scene

    def draw(self):
        self._graphic_scene.clear()
        objects = self._window.getVisibleObjects()
        for obj in objects:
            coords = iter(obj.getCoordinates())
            last_point = next(coords)
            if obj.getType() != "Point":
                for cur_point in coords:
                    self.getScene().addLine(
                        self._window.getXW(last_point[0]) * self._size[0],
                        self._window.getYW(last_point[1]) * self._size[1],
                        self._window.getXW(cur_point[0]) * self._size[0],
                        self._window.getYW(cur_point[1]) * self._size[1],
                        self._pen
                    )
                    last_point = cur_point
            else:
                self.getScene().addEllipse(
                    self._window.getXW(last_point[0]) * self._size[0],
                    self._window.getYW(last_point[1]) * self._size[1],
                    5, 5,
                    self._pen,
                    self._brush
                )
