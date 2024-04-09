from typing import Callable
from PyQt6 import QtCore, QtGui, QtWidgets
from objects.factory import Factory
from objects.geometricObject import Colour, Coordinate, GeometricObject

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

        re = QtCore.QRegularExpression(
            "(\\(-?\\d*(\\.\\d*)?\\s*,\\s*-?\\d*(\\.\\d*)?\\),)*\\(-?\\d*(\\.\\d*)?\\s*,\\s*-?\\d*(\\.\\d*)?\\)",  # noqa: E501
        )
        self.inputCoordinates.setValidator(QtGui.QRegularExpressionValidator(re))
        re = QtCore.QRegularExpression("#[0-9a-fA-F]{6}")
        self.inputColour.setValidator(QtGui.QRegularExpressionValidator(re))

    def accept(self) -> None:
        """
        Event fired when the dialog is accepted
        """
        name: str = self.inputName.text()
        colour: Colour = (0, 0, 0)
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
            points: tuple[Coordinate, ...] = tuple(
                eval(self.inputCoordinates.text() + ","),
            )
            self._callback(Factory.create_object(name, colour, points))
            self.close()
        except Exception:
            return
