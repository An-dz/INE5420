from PyQt6 import QtGui
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QLabel
from window import Window


class Viewport:
    """The viewport in the UI where the window is displayed"""
    def __init__(self, window: Window, viewportCanvas: QLabel):
        """
        Creates the viewport

        @param window: The window this viewport will display
        @param viewportCanvas: The QT object to manipulate the pixmap
        """
        self._window = window
        self._size = (viewportCanvas.width() - 2, viewportCanvas.height() -2)
        self._canvas = QtGui.QPixmap(self._size[0], self._size[1])
        drawing_color = QtGui.QColor(246, 158, 67)
        self._pen = QtGui.QPen(drawing_color)
        self._pen.setWidth(2)
        self._viewportCanvas = viewportCanvas

    def getCanvas(self) -> QtGui.QPixmap:
        """
        Returns the pixmap object

        @returns: pixmap of the UI object
        """
        return self._canvas

    def getViewportCanvas(self) -> QLabel:
        """
        Returns the UI object

        @returns: UI object that the pixmap is being manipulated
        """
        return self._viewportCanvas

    def draw(self) -> None:
        """
        Redraws the viewport according to the window
        """
        painter = QtGui.QPainter(self.getCanvas())
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(self._pen)
        painter.setBackground(QtGui.QColor(61, 61, 61))
        painter.setBackgroundMode(Qt.BGMode.OpaqueMode)
        painter.eraseRect(0,0,self._size[0],self._size[1])
        objects = self._window.getVisibleObjects()
        for obj in objects:
            coords = iter(obj.getCoordinates())
            last_point = next(coords)
            if obj.getType() != "Point":
                for cur_point in coords:
                    painter.drawLine(
                        QPointF(
                            self._window.getXW(last_point[0]) * self._size[0],
                            self._window.getYW(last_point[1]) * self._size[1]
                        ),
                        QPointF(
                            self._window.getXW(cur_point[0]) * self._size[0],
                            self._window.getYW(cur_point[1]) * self._size[1]
                        )
                    )
                    last_point = cur_point
            else:
                painter.drawPoint(
                    QPointF(
                        self._window.getXW(last_point[0]) * self._size[0],
                        self._window.getYW(last_point[1]) * self._size[1]
                    )
                )
        painter.end()
        self.getViewportCanvas().setPixmap(self.getCanvas())