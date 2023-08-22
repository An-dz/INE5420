from PyQt6 import QtWidgets
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
        self.actionAdd_Object.triggered.connect(self.action_create_objectmenu)
        self.actionAbout.triggered.connect(self.action_about_menu)
        self.actionQuit.triggered.connect(self.action_quit_menu)
        self.movementButtonDown.clicked.connect(self.action_move_down)
        self.movementButtonLeft.clicked.connect(self.action_move_left)
        self.movementButtonRight.clicked.connect(self.action_move_right)
        self.movementButtonUp.clicked.connect(self.action_move_up)
        self.movementButtonZoomOut.clicked.connect(self.action_zoom_out)
        self.movementButtonZoomIn.clicked.connect(self.action_zoom_in)
        self.keyboardZoomIn = QShortcut(QKeySequence("+"), self)
        self.keyboardZoomOut = QShortcut(QKeySequence("-"), self)
        self.keyboardZoomIn.activated.connect(self.action_zoom_in)
        self.keyboardZoomOut.activated.connect(self.action_zoom_out)
        self.keyboardDeleteObject = QShortcut(QKeySequence("Del"), self)
        self.keyboardDeleteObject.activated.connect(self.action_delete_object)

        self._display_file = DisplayFile()
        self._window_obj = Window(self._display_file, (-100, -100), (100, 100))
        self._viewport = Viewport(self._window_obj, self.viewportCanvas)

        self._viewport.draw()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:  # noqa: N802
        """
        Listens to keyboard shortcuts so we can have keypad shortcuts just like in Blender
        """
        if event:
            numpad_mod = event.modifiers() & Qt.KeyboardModifier.KeypadModifier
            if numpad_mod:
                if event.key() == Qt.Key.Key_Plus:
                    self.action_zoom_in()
                elif event.key() == Qt.Key.Key_Minus:
                    self.action_zoom_out()
                elif event.key() == Qt.Key.Key_2:
                    self.action_move_down()
                elif event.key() == Qt.Key.Key_4:
                    self.action_move_left()
                elif event.key() == Qt.Key.Key_6:
                    self.action_move_right()
                elif event.key() == Qt.Key.Key_8:
                    self.action_move_up()

    def action_delete_object(self) -> None:
        """
        Deletes an object from the world through the UI list

        @note The deleted object is the currently selected object
        """
        obj_index = self.objectsList.currentRow()
        if obj_index > -1 and obj_index < self.objectsList.count():
            self.objectsList.takeItem(obj_index)
            self._display_file.remove(obj_index)
            self._viewport.draw()

    def action_move_left(self) -> None:
        self._window_obj.move(-0.03, 0)
        self._viewport.draw()

    def action_move_right(self) -> None:
        self._window_obj.move(0.03, 0)
        self._viewport.draw()

    def action_move_up(self) -> None:
        self._window_obj.move(0, 0.03)
        self._viewport.draw()

    def action_move_down(self) -> None:
        self._window_obj.move(0, -0.03)
        self._viewport.draw()

    def action_zoom_out(self) -> None:
        self._window_obj.zoom(1.25)
        self._viewport.draw()

    def action_zoom_in(self) -> None:
        self._window_obj.zoom(0.8)
        self._viewport.draw()

    def action_create_object(self, obj: GeometricObject) -> None:
        """
        Adds a created object into the display file and the object list UI

        @note Used as a callback in the Create Object dialog

        @param obj: The created object
        """
        self._display_file.add(obj)
        QtWidgets.QListWidgetItem(
            "{} [{}]".format(obj.get_name(), obj.get_type()),
            self.objectsList,
        )
        self._viewport.draw()

    def action_create_objectmenu(self) -> None:
        """
        Opens the Create Object dialog
        """
        dialog = CreateObjectDialog(callback=self.action_create_object)
        dialog.exec()

    def action_about_menu(self) -> None:
        """
        Opens the About dialog
        """
        dialog = AboutDialog()
        dialog.exec()

    def action_quit_menu(self) -> None:
        """
        Quits the application
        """
        self.close()
