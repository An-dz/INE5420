from PyQt6 import QtWidgets

from .generated.mainWindow import Ui_MainWindow
from .about import AboutDialog

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionAbout.triggered.connect(self.actionAboutMenu)
        self.actionQuit.triggered.connect(self.actionQuitMenu)

    def actionAboutMenu(self):
        dialog = AboutDialog()
        dialog.exec()

    def actionQuitMenu(self):
        self.close()
