from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QKeySequence, QShortcut
from displayFile import DisplayFile
from objects.geometricObject import GeometricObject
from ui.createObject import CreateObjectDialog
from ui.generated.mainWindow import Ui_MainWindow
from ui.about import AboutDialog
from viewport import Viewport
from window import Window

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # set actions
        self.actionAdd_Object.triggered.connect(self.actionCreateObjectMenu)
        self.actionAbout.triggered.connect(self.actionAboutMenu)
        self.actionQuit.triggered.connect(self.actionQuitMenu)
        self.movementButtonDown.clicked.connect(self.actionMoveDown)
        self.movementButtonLeft.clicked.connect(self.actionMoveLeft)
        self.movementButtonRight.clicked.connect(self.actionMoveRight)
        self.movementButtonUp.clicked.connect(self.actionMoveUp)
        self.movementButtonZoomOut.clicked.connect(self.actionZoomOut)
        self.movementButtonZoomIn.clicked.connect(self.actionZoomIn)
        self.keyboardZoomIn = QShortcut(QKeySequence("+"), self)
        self.keyboardZoomOut = QShortcut(QKeySequence("-"), self)
        self.keyboardZoomIn.activated.connect(self.actionZoomIn)
        self.keyboardZoomOut.activated.connect(self.actionZoomOut)
        self.keyboardDeleteObject = QShortcut(QKeySequence("Del"), self)
        self.keyboardDeleteObject.activated.connect(self.actionDeleteObject)

        self._display_file = DisplayFile()
        self._window_obj = Window(self._display_file, (-100,-100), (100,100))
        self._viewport = Viewport(self._window_obj, (self.graphicsView.height() - 2, self.graphicsView.width() - 2))
        self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(61, 61, 61)))
        self.graphicsView.setScene(self._viewport.getScene())
        self.graphicsView.setSceneRect(0,0,self.graphicsView.height() - 2,self.graphicsView.width() - 2)
        self._viewport.draw()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """
        Listens to keyboard shortcuts so we can have keypad shortcuts just like in Blender
        """
        if event:
            numpad_mod = event.modifiers() & Qt.KeyboardModifier.KeypadModifier
            if numpad_mod:
                if event.key() == Qt.Key.Key_Plus:
                    self.actionZoomIn()
                elif event.key() == Qt.Key.Key_Minus:
                    self.actionZoomOut()
                elif event.key() == Qt.Key.Key_2:
                    self.actionMoveDown()
                elif event.key() == Qt.Key.Key_4:
                    self.actionMoveLeft()
                elif event.key() == Qt.Key.Key_6:
                    self.actionMoveRight()
                elif event.key() == Qt.Key.Key_8:
                    self.actionMoveUp()

    def actionDeleteObject(self) -> None:
        """
        Deletes an object from the world through the UI list

        @note The deleted object is the currently selected object
        """
        obj_index = self.objectsList.currentRow()
        if obj_index > -1 and obj_index < self.objectsList.count():
            self.objectsList.takeItem(obj_index)
            self._display_file.remove(obj_index)
            self._viewport.draw()

    def actionMoveLeft(self) -> None:
        self._window_obj.move(-0.03, 0)
        self._viewport.draw()

    def actionMoveRight(self) -> None:
        self._window_obj.move(0.03, 0)
        self._viewport.draw()

    def actionMoveUp(self) -> None:
        self._window_obj.move(0, 0.03)
        self._viewport.draw()

    def actionMoveDown(self) -> None:
        self._window_obj.move(0, -0.03)
        self._viewport.draw()

    def actionZoomOut(self) -> None:
        self._window_obj.zoom(1.25)
        self._viewport.draw()

    def actionZoomIn(self) -> None:
        self._window_obj.zoom(0.8)
        self._viewport.draw()

    def actionCreateObject(self, obj: GeometricObject) -> None:
        """
        Adds a created object into the display file and the object list UI

        @note Used as a callback in the Create Object dialog

        @param obj: The created object
        """
        self._display_file.add(obj)
        QtWidgets.QListWidgetItem("{} [{}]".format(obj.getName(), obj.getType()), self.objectsList)
        self._viewport.draw()

    def actionCreateObjectMenu(self) -> None:
        """
        Opens the Create Object dialog
        """
        dialog = CreateObjectDialog(callback=self.actionCreateObject)
        dialog.exec()

    def actionAboutMenu(self) -> None:
        """
        Opens the About dialog
        """
        dialog = AboutDialog()
        dialog.exec()

    def actionQuitMenu(self) -> None:
        """
        Quits the application
        """
        self.close()
