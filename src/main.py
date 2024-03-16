import sys
from PyQt6 import QtWidgets

from ui.mainWindow import MainWindow


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
