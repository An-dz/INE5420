from typing import Callable
from PyQt6 import QtWidgets
from objects.factory import Factory
from objects.geometricObject import Coordinate, GeometricObject

from ui.generated.createObject import Ui_CreateObjectDialog


class CreateObjectDialog(QtWidgets.QDialog, Ui_CreateObjectDialog):
    """A simple about screen just to show who made this"""
    def __init__(self, callback: Callable[[GeometricObject], None], *args, **kwargs) -> None:
        super(CreateObjectDialog, self).__init__(*args, **kwargs)
        self._callback = callback
        self.setupUi(self)

    def accept(self) -> None:
        name: str = self.nameInput.text()
        points: tuple[Coordinate, ...] = tuple(eval(self.coordinatesInput.text() + ","))
        self._callback(Factory.createObject(name, points))
        self.close()
