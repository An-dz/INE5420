#!/bin/env python3

import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon

from ui.mainWindow import MainWindow


script_dir = os.path.dirname(__file__)
app = QtWidgets.QApplication(sys.argv)

icons = {
    "Point": QIcon(os.path.join(script_dir, "assets/point.png")),
    "Line": QIcon(os.path.join(script_dir, "assets/line.png")),
    "Wireframe": QIcon(os.path.join(script_dir, "assets/wireframe.png")),
}

window = MainWindow(icons)
window.show()
app.exec()
