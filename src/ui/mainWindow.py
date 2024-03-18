from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from ui.generated.mainWindow import Ui_MainWindow
from ui.about import AboutDialog
from viewport import Viewport
from window import Window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # set actions
        self.actionAbout.triggered.connect(self.actionAboutMenu)
        self.actionQuit.triggered.connect(self.actionQuitMenu)
        self.movementButtonDown.clicked.connect(self.actionMoveDown)
        self.movementButtonLeft.clicked.connect(self.actionMoveLeft)
        self.movementButtonRight.clicked.connect(self.actionMoveRight)
        self.movementButtonUp.clicked.connect(self.actionMoveUp)
        self.movementButtonZoomOut.clicked.connect(self.actionMoveLeft)
        self.movementButtonZoomIn.clicked.connect(self.actionMoveLeft)

        self._window_obj = Window((-100,-100), (100,100))
        self._viewport = Viewport(self._window_obj, (self.graphicsView.height() - 2, self.graphicsView.width() - 2))
        self.graphicsView.setScene(self._viewport.getScene())
        self.graphicsView.setSceneRect(0,0,self.graphicsView.height() - 2,self.graphicsView.width() - 2)
        self._viewport.draw()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event:
            numpad_mod = event.modifiers() & Qt.KeyboardModifier.KeypadModifier
            if numpad_mod:
                if event.key() == Qt.Key.Key_2:
                    self.actionMoveDown()
                elif event.key() == Qt.Key.Key_4:
                    self.actionMoveLeft()
                elif event.key() == Qt.Key.Key_6:
                    self.actionMoveRight()
                elif event.key() == Qt.Key.Key_8:
                    self.actionMoveUp()

    def actionMoveLeft(self) -> None:
        self._window_obj.move(-20, 0)
        self._viewport.draw()

    def actionMoveRight(self) -> None:
        self._window_obj.move(20, 0)
        self._viewport.draw()

    def actionMoveUp(self) -> None:
        self._window_obj.move(0, 20)
        self._viewport.draw()

    def actionMoveDown(self) -> None:
        self._window_obj.move(0, -20)
        self._viewport.draw()

    def actionAboutMenu(self) -> None:
        dialog = AboutDialog()
        dialog.exec()

    def actionQuitMenu(self) -> None:
        self.close()
