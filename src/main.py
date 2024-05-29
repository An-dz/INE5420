#!/bin/env python3

import os
import sys

from PyQt6 import QtGui, QtWidgets

from ui.mainWindow import MainWindow


script_dir = os.path.dirname(__file__)
app = QtWidgets.QApplication(sys.argv)

icons = {
    "Point": QtGui.QIcon(os.path.join(script_dir, "assets/point.png")),
    "Point3D": QtGui.QIcon(os.path.join(script_dir, "assets/point.png")),
    "Object3D": QtGui.QIcon(os.path.join(script_dir, "assets/cube.png")),
    "Line": QtGui.QIcon(os.path.join(script_dir, "assets/line.png")),
    "Wireframe": QtGui.QIcon(os.path.join(script_dir, "assets/wireframe.png")),
    "Polygon": QtGui.QIcon(os.path.join(script_dir, "assets/polygon.png")),
    "BezierCurve": QtGui.QIcon(os.path.join(script_dir, "assets/beziercurve.png")),
    "BSplineCurve": QtGui.QIcon(os.path.join(script_dir, "assets/bsplinecurve.png")),
    "BezierSurface": QtGui.QIcon(os.path.join(script_dir, "assets/beziersurface.png")),
    "BSplineSurface": QtGui.QIcon(os.path.join(script_dir, "assets/bsplinesurface.png")),
}

window = MainWindow(icons)
window.show()
app.exec()
