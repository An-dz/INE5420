from PyQt6 import QtGui
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QLabel
from window import Window


class Viewport:
    """The viewport in the UI where the window is displayed"""
    def __init__(self, window: Window, viewport_canvas: QLabel):
        """
        Creates the viewport

        @param window: The window this viewport will display
        @param viewport_canvas: The QT object to manipulate the pixmap
        """
        self._window = window
        self._size = (viewport_canvas.width() - 2, viewport_canvas.height() - 2)
        self._canvas = QtGui.QPixmap(self._size[0], self._size[1])
        self._viewport_canvas = viewport_canvas

    def get_canvas(self) -> QtGui.QPixmap:
        """
        Returns the pixmap object

        @returns: pixmap of the UI object
        """
        return self._canvas

    def get_viewport_canvas(self) -> QLabel:
        """
        Returns the UI object

        @returns: UI object that the pixmap is being manipulated
        """
        return self._viewport_canvas

    def draw(self) -> None:
        """
        Redraws the viewport according to the window
        """
        painter = QtGui.QPainter(self.get_canvas())
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBackground(QtGui.QColor(61, 61, 61))
        painter.setBackgroundMode(Qt.BGMode.OpaqueMode)
        painter.eraseRect(0, 0, self._size[0], self._size[1])
        objects = self._window.get_visible_objects()
        for obj in objects:
            drawing_color = QtGui.QColor(*obj.get_colour())
            pen = QtGui.QPen(drawing_color)
            pen.setWidth(2)
            painter.setPen(pen)
            coords = obj.get_window_coordinates()

            if obj.get_type() != "Point":
                for line in coords:
                    painter.drawLine(
                        QPointF(
                            self._window.get_xw(line[0][0]) * self._size[0],
                            self._window.get_yw(line[0][1]) * self._size[1],
                        ),
                        QPointF(
                            self._window.get_xw(line[1][0]) * self._size[0],
                            self._window.get_yw(line[1][1]) * self._size[1],
                        ),
                    )
            else:
                painter.drawPoint(
                    QPointF(
                        self._window.get_xw(coords[0][0][0]) * self._size[0],
                        self._window.get_yw(coords[0][0][1]) * self._size[1],
                    ),
                )
        painter.end()
        self.get_viewport_canvas().setPixmap(self.get_canvas())
