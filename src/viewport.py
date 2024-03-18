from PyQt6 import QtGui, QtWidgets
from objects.geometricObject import Coordinate
from window import Window


class Viewport:
    """docstring for Viewport"""
    def __init__(self, window: Window, size: Coordinate):
        self._window = window
        self._size = size
        self._graphic_scene = QtWidgets.QGraphicsScene()

    def getScene(self) -> QtWidgets.QGraphicsScene:
        return self._graphic_scene

    def draw(self):
        pen = QtGui.QPen(QtGui.QColor("black"))
        pen.setWidth(2)
        objects = self._window.getVisibleObjects()
        for obj in objects:
            coords = obj.getCoordinates()
            if obj.getType != "Point":
                self.getScene().addLine(coords[0][0], coords[0][1], coords[1][0], coords[1][1], pen)
            else:
                self.getScene().addEllipse(coords[0][0], coords[0][1], 5, 5, pen, QtGui.QBrush(QtGui.QColor("black")))
