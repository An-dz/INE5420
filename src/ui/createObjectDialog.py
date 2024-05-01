from typing import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from objects.factory import Factory
from objects.geometricObject import (
    Colour,
    Coordinate,
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

        re = QtCore.QRegularExpression("[0-9(),. -]+")
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

    def check_coordinates(self, text: str) -> None:
        """
        Validate input for the coordinates input

        @param text: Current text of the input element
        """
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)

        if ok_button:
            error_msg = "Coordinates are not in the expected format"

            try:
                vertices: tuple = tuple(eval(text + ","))

                # input is only valid for tuples of coordinates
                for vertex in vertices:
                    if (
                        len(vertex) != 2 or not (
                            isinstance(vertex[0], float) or isinstance(vertex[0], int)
                        ) or not (
                            isinstance(vertex[1], float) or isinstance(vertex[1], int)
                        )
                    ):
                        raise

                error_msg = (
                    "Polygons need at least 3 vertices and "
                    + "must start and end on the same vertex"
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
                    self.checkBoxBezier.setToolTip(
                        "Bézier curves requires a minimum of 4 points and "
                        + "then 3 more per segment",
                    )

                if len(vertices) > 3:
                    self.checkBoxBSpline.setEnabled(True)
                    self.checkBoxBSpline.setToolTip(
                        "Create a B-Spline curve with any amount of points instead of"
                        + " a wireframe object",
                    )
                else:
                    self.checkBoxBSpline.setEnabled(False)
                    self.checkBoxBSpline.setChecked(False)
                    self.checkBoxBSpline.setToolTip(
                        "B-Spline curves requires a minimum of 4 points",
                    )

                self._valid_input["coords"] = True
                ok_button.setEnabled(self._valid_input["colour"])
                if len(vertices) > 3 and vertices[0] == vertices[-1]:
                    self.checkboxPolygon.setEnabled(True)
                    self.checkboxPolygon.setToolTip(
                        "Create the object as polygon that is filled instead "
                        + "of a wireframe object that only draws edges",
                    )
                    return
            except Exception:
                error_msg = "Coordinates are not in the expected format"
                self._valid_input["coords"] = False
                ok_button.setEnabled(False)

            self.checkboxPolygon.setChecked(False)
            self.checkboxPolygon.setEnabled(False)
            self.checkboxPolygon.setToolTip(error_msg)

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
                return

            self._valid_input["colour"] = False
            ok_button.setEnabled(False)

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
            vertices_tuple: tuple[Coordinate, ...] = tuple(
                eval(self.inputCoordinates.text() + ","),
            )
            vertices_normal: VerticesList = [(*v, 1) for v in vertices_tuple]
            object_list: ObjectsList = []

            if len(vertices_normal) == 1:
                object_list = [tuple(vertices_normal)]
            elif self.checkboxPolygon.isChecked():
                vertices_normal.pop()
                object_list = [tuple(vertices_normal)]
            elif not self.checkBoxBezier.isChecked() and not self.checkBoxBSpline.isChecked():
                vertices_iter = iter(vertices_normal)
                last_vertex = next(vertices_iter)
                for vertex in vertices_iter:
                    object_list.append((last_vertex, vertex))
                    last_vertex = vertex

            self._callback(Factory.create_object(
                name,
                colour,
                vertices_normal,
                object_list,
                self.checkBoxBSpline.isChecked(),
            ))
            self.close()
        except Exception:
            return
