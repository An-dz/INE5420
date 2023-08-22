from typing import Callable
from PyQt6 import QtWidgets
from objects.factory import Factory
from objects.geometricObject import Coordinate, GeometricObject

from ui.generated.createObject import Ui_CreateObjectDialog


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

    def accept(self) -> None:
        """
        Event fired when the dialog is accepted
        """
        name: str = self.nameInput.text()
        points: tuple[Coordinate, ...] = tuple(eval(self.coordinatesInput.text() + ","))
        self._callback(Factory.create_object(name, points))
        self.close()
