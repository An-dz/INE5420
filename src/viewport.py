from PyQt6 import QtCore, QtGui, QtWidgets

from window import Window

MARGIN = 20
"""Clipping margin"""


class Viewport:
    """The viewport in the UI where the window is displayed"""
    def __init__(self, window: Window, viewport_canvas: QtWidgets.QLabel):
        """
        Creates the viewport

        @param window: The window this viewport will display
        @param viewport_canvas: The QT object to manipulate the pixmap
        """
        self._window = window
        self._size = (
            (viewport_canvas.width() - 2) - (2 * MARGIN),
            (viewport_canvas.height() - 2) - (2 * MARGIN),
        )
        self._canvas = QtGui.QPixmap(
            (viewport_canvas.width() - 2),
            (viewport_canvas.height() - 2),
        )
        self._viewport_canvas = viewport_canvas
        self._selected_colour = QtGui.QColor(246, 158, 67)

    def get_canvas(self) -> QtGui.QPixmap:
        """
        Returns the pixmap object

        @returns: pixmap of the UI object
        """
        return self._canvas

    def get_viewport_canvas(self) -> QtWidgets.QLabel:
        """
        Returns the UI object

        @returns: UI object that the pixmap is being manipulated
        """
        return self._viewport_canvas

    def draw(self, selected: int) -> None:
        """
        Redraws the viewport according to the window
        """
        painter = QtGui.QPainter(self.get_canvas())
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBackground(QtGui.QColor(61, 61, 61))
        painter.setBackgroundMode(QtCore.Qt.BGMode.OpaqueMode)
        painter.eraseRect(self._canvas.rect())
        objects = self._window.get_visible_objects()
        pen = QtGui.QPen()
        pen.setWidth(2)

        self.draw_clipping_area(painter)

        for index, obj in enumerate(objects):
            fill_colour = QtGui.QColor(*obj.get_colour())
            line_colour = fill_colour if selected != index else self._selected_colour
            pen.setColor(line_colour)
            painter.setPen(pen)
            painter.setBrush(fill_colour)
            geometric_objects = obj.get_window_coordinates()

            for vertices in geometric_objects:
                if len(vertices) == 1:  # point
                    painter.drawPoint(
                        QtCore.QPointF(
                            self._window.get_xw(vertices[0][0]) * self._size[0] + MARGIN,
                            self._window.get_yw(vertices[0][1]) * self._size[1] + MARGIN,
                        ),
                    )
                elif len(vertices) == 2:  # line
                    painter.drawLine(
                        QtCore.QPointF(
                            self._window.get_xw(vertices[0][0]) * self._size[0] + MARGIN,
                            self._window.get_yw(vertices[0][1]) * self._size[1] + MARGIN,
                        ),
                        QtCore.QPointF(
                            self._window.get_xw(vertices[1][0]) * self._size[0] + MARGIN,
                            self._window.get_yw(vertices[1][1]) * self._size[1] + MARGIN,
                        ),
                    )
                else:  # polygon
                    if selected != index:
                        pen.setColor(line_colour.darker(150))

                    painter.setPen(pen)
                    painter.drawPolygon(QtGui.QPolygonF([
                        QtCore.QPointF(
                            self._window.get_xw(coord[0]) * self._size[0] + MARGIN,
                            self._window.get_yw(coord[1]) * self._size[1] + MARGIN,
                        ) for coord in vertices
                    ]))

        painter.end()
        self.get_viewport_canvas().setPixmap(self.get_canvas())

    def draw_clipping_area(self, painter: QtGui.QPainter) -> None:
        line_colour = QtGui.QColor(QtGui.QColor(79, 79, 79))
        pen = QtGui.QPen(line_colour)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(MARGIN, MARGIN, self._size[0], self._size[1])
