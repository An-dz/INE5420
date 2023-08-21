from PyQt6 import QtWidgets
from ui.generated.mainWindow import Ui_MainWindow
from ui.about import AboutDialog
from viewport import Viewport
from window import Window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionAbout.triggered.connect(self.actionAboutMenu)
        self.actionQuit.triggered.connect(self.actionQuitMenu)

        self._window_obj = Window((0,0), (1,1))
        self._viewport = Viewport(self._window_obj, (self.graphicsView.height() - 2, self.graphicsView.width() - 2))
        self.graphicsView.setScene(self._viewport.getScene())
        self.graphicsView.setSceneRect(0,0,self.graphicsView.height() - 2,self.graphicsView.width() - 2)
        self._viewport.draw()

    def actionAboutMenu(self) -> None:
        dialog = AboutDialog()
        dialog.exec()

    def actionQuitMenu(self) -> None:
        self.close()
