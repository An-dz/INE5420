from typing import Any, Callable

from PyQt6 import QtCore, QtGui, QtWidgets
import numpy as np

from objects.bezier_surface import BezierSurface
from objects.bspline_surface import BSplineSurface
from objects.factory import Factory
from objects.geometricObject import (
    Colour,
    GeometricObject,
    ObjectsList,
    VerticesList,
)
from ui.generated.createObjectDialog import Ui_CreateObjectDialog


class CreateObjectDialog(QtWidgets.QDialog, Ui_CreateObjectDialog):
    """The dialog box responsible for allowing the user to add objects into the world"""
    def __init__(
        self,
        callback: Callable[[GeometricObject], None],
        *args,
        **kwargs,
    ) -> None:
        """
        Creates the dialog

        @param callback: A callback function where the dialog will send the created object
        """
        super(CreateObjectDialog, self).__init__(*args, **kwargs)
        self._callback = callback
        self.setupUi(self)

        self._valid_input = {
            "coords": False,
            "colour": True,
        }
        self._error_msgs = {
            "polygon": "Polygons need at least 3 vertices and must start and end on the "
            + "same vertex",
            "bezier_curve": "Bézier curves requires a minimum of 4 points and then 3 "
            + "more per segment",
            "bspline_curve": "B-Spline curves requires a minimum of 4 points",
            "bezier_surface": "Bézier surfaces require a 4x4 matriz of points, separate "
            + "lines of the matrix with semicolon (;)",
            "bspline_surface": "B-Spline surfaces require a minimum 4x4 matriz of points,"
            + " up to 20x20, separate lines of the matrix with semicolon (;)",
            "bad_coords": "Coordinates are not in the expected format",
            "bad_colour": "Colour is not in the expected format",
        }
        self.checkboxPolygon.setToolTip(self._error_msgs["polygon"])
        self.checkBoxBezier.setToolTip(self._error_msgs["bezier_curve"])
        self.checkBoxBSpline.setToolTip(self._error_msgs["bspline_curve"])
        self.checkBoxBezierSurface.setToolTip(self._error_msgs["bezier_surface"])
        self.checkBoxBSplineSurface.setToolTip(self._error_msgs["bspline_surface"])

        re = QtCore.QRegularExpression("[0-9(),. ;-]+")
        self.inputCoordinates.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputCoordinates.textChanged.connect(self.check_coordinates)
        re = QtCore.QRegularExpression("#[0-9a-fA-F]{6}")
        self.inputColour.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputColour.textChanged.connect(self.check_colour)
        self._checkboxes = [
            self.checkBoxBezier,
            self.checkBoxBSpline,
            self.checkboxPolygon,
        ]
        self.checkBoxBezier.toggled.connect(
            lambda s: self.exclusive_checkbox(self.checkBoxBezier, s),
        )
        self.checkBoxBSpline.toggled.connect(
            lambda s: self.exclusive_checkbox(self.checkBoxBSpline, s),
        )
        self.checkboxPolygon.toggled.connect(
            lambda s: self.exclusive_checkbox(self.checkboxPolygon, s),
        )
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        if ok_button:
            ok_button.setEnabled(False)

    def exclusive_checkbox(
        self,
        self_checkbox: QtWidgets.QCheckBox,
        state: bool,
    ) -> None:
        if state:
            for checkbox in self._checkboxes:
                if checkbox != self_checkbox:
                    checkbox.setChecked(False)
                    checkbox.setEnabled(False)
        else:
            self.check_coordinates(self.inputCoordinates.text())

    def check_vertices(self, vertices: tuple[Any, ...]) -> None:
        """
        Input is only valid for tuples of coordinates
        """
        for vertex in vertices:
            if (
                len(vertex) != 3 or not (
                    isinstance(vertex[0], float) or isinstance(vertex[0], int)
                ) or not (
                    isinstance(vertex[1], float) or isinstance(vertex[1], int)
                ) or not (
                    isinstance(vertex[2], float) or isinstance(vertex[2], int)
                )
            ):
                raise

    def check_coordinates(self, text: str) -> None:
        """
        Validate input for the coordinates input

        @param text: Current text of the input element
        """
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)

        if ok_button:
            try:
                vertices_matrix = text.split(";")
                vertices: tuple[Any, ...] = ()
                bezier_surface = False
                bspline_surface = False

                if len(vertices_matrix) == 1:
                    vertices = tuple(eval(text + ","))
                    self.check_vertices(vertices)
                elif len(vertices_matrix) > 3:
                    bezier_surface = len(vertices_matrix) == 4
                    bspline_surface = True
                    vertices_count: int | None = None

                    for vertices_line_text in vertices_matrix:
                        vertices_line = tuple(eval(vertices_line_text + ","))
                        self.check_vertices(vertices_line)

                        if vertices_count and vertices_count != len(vertices_line):
                            bspline_surface = False

                        if len(vertices_line) != 4:
                            bezier_surface = False

                        vertices_count = len(vertices_line)

                if bezier_surface:
                    self.checkBoxBezierSurface.setChecked(True)
                    self.checkBoxBezierSurface.setEnabled(True)
                    self.checkBoxBezierSurface.setToolTip(
                        "Create a Bézier Surface with 16 control points",
                    )
                else:
                    self.checkBoxBezierSurface.setChecked(False)
                    self.checkBoxBezierSurface.setEnabled(False)
                    self.checkBoxBezierSurface.setToolTip(
                        self._error_msgs["bezier_surface"],
                    )

                if bspline_surface:
                    self.checkBoxBSplineSurface.setChecked(True)
                    self.checkBoxBSplineSurface.setEnabled(True)
                    self.checkBoxBSplineSurface.setToolTip(
                        "Create a B-Spline Surface with multiple control points",
                    )
                else:
                    self.checkBoxBSplineSurface.setChecked(False)
                    self.checkBoxBSplineSurface.setEnabled(False)
                    self.checkBoxBSplineSurface.setToolTip(
                        self._error_msgs["bspline_surface"],
                    )

                if len(vertices) > 3 and len(vertices) % 3 == 1:
                    self.checkBoxBezier.setEnabled(True)
                    self.checkBoxBezier.setToolTip(
                        "Create a colection of Bézier curves instead of a "
                        + "wireframe object",
                    )
                else:
                    self.checkBoxBezier.setEnabled(False)
                    self.checkBoxBezier.setChecked(False)
                    self.checkBoxBezier.setToolTip(self._error_msgs["bezier_curve"])

                if len(vertices) > 3:
                    self.checkBoxBSpline.setEnabled(True)
                    self.checkBoxBSpline.setToolTip(
                        "Create a B-Spline curve with any amount of points instead of"
                        + " a wireframe object",
                    )
                else:
                    self.checkBoxBSpline.setEnabled(False)
                    self.checkBoxBSpline.setChecked(False)
                    self.checkBoxBSpline.setToolTip(self._error_msgs["bspline_curve"])

                self._valid_input["coords"] = True
                ok_button.setEnabled(self._valid_input["colour"])
                ok_button.setToolTip(
                    self._error_msgs["bad_colour"] if self._valid_input["colour"]
                    else None,
                )
                if len(vertices) > 2 and vertices[0] == vertices[-1]:
                    self.checkboxPolygon.setEnabled(True)
                    self.checkboxPolygon.setToolTip(
                        "Create the object as a polygon that is filled instead "
                        + "of a wireframe object that only draws edges",
                    )
                else:
                    self.checkboxPolygon.setChecked(False)
                    self.checkboxPolygon.setEnabled(False)
                    self.checkboxPolygon.setToolTip(self._error_msgs["polygon"])
            except Exception:
                self._valid_input["coords"] = False
                ok_button.setEnabled(False)
                ok_button.setToolTip(self._error_msgs["bad_coords"])

    def check_colour(self, text: str) -> None:
        """
        Validate input for the colour input

        @param text: Current text of the input element
        """
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)

        if ok_button:
            if len(text) == 0 or len(text) == 4 or len(text) == 7:
                self._valid_input["colour"] = True
                ok_button.setEnabled(self._valid_input["coords"])
                ok_button.setToolTip(
                    self._error_msgs["bad_coords"] if self._valid_input["coords"]
                    else None,
                )
                return

            self._valid_input["colour"] = False
            ok_button.setEnabled(False)
            ok_button.setToolTip(self._error_msgs["bad_colour"])

    def accept(self) -> None:
        """
        Event fired when the dialog is accepted
        """
        name: str = self.inputName.text()
        colour: Colour = (204, 204, 204)
        colour_hex = self.inputColour.text()

        if len(colour_hex) == 4:
            colour = (
                int(colour_hex[1] * 2, 16),
                int(colour_hex[2] * 2, 16),
                int(colour_hex[3] * 2, 16),
            )
        elif len(colour_hex) == 7:
            colour = (
                int(colour_hex[1:3], 16),
                int(colour_hex[3:5], 16),
                int(colour_hex[5:7], 16),
            )

        try:
            text = self.inputCoordinates.text()
            vertices_matrix = text.split(";")

            if len(vertices_matrix) > 1:
                vertices_tuples: list[tuple[tuple[float, float, float], ...]] = [
                    eval(vertices_str) for vertices_str in vertices_matrix
                ]
                vertices: VerticesList = []

                if self.checkBoxBezierSurface.isChecked():
                    for vertices_list in vertices_tuples:
                        for v in vertices_list:
                            vertices.append((*v, 1))

                    self._callback(BezierSurface(name, colour, vertices))
                elif self.checkBoxBSplineSurface.isChecked():
                    matrix = np.array(
                        [
                            [(*v, 1) for v in vertices_list]
                            for vertices_list in vertices_tuples
                        ],
                    )
                    self._callback(BSplineSurface(name, colour, matrix))
                return

            vertices_tuple: tuple[tuple[float, float, float], ...] = tuple(
                eval(text + ","),
            )
            vertices_normal: VerticesList = [(*v, 1) for v in vertices_tuple]
            object_list: ObjectsList = []

            if len(vertices_normal) == 1:
                object_list = [tuple(vertices_normal)]
            elif self.checkboxPolygon.isChecked():
                vertices_normal.pop()
                object_list = [tuple(vertices_normal)]
            elif (
                not self.checkBoxBezier.isChecked()
                and not self.checkBoxBSpline.isChecked()
            ):
                vertices_iter = iter(vertices_normal)
                last_vertex = next(vertices_iter)
                for vertex in vertices_iter:
                    object_list.append((last_vertex, vertex))
                    last_vertex = vertex

            self._callback(Factory.create_object_new(
                name,
                colour,
                vertices_normal,
                object_list,
                self.checkBoxBSpline.isChecked(),
            ))
            self.close()
        except Exception as e:
            print(e)
            return
