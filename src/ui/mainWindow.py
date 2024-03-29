from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from displayFile import DisplayFile
from objects.geometricObject import GeometricObject
from ui.createObject import CreateObjectDialog
from ui.generated.mainWindow import Ui_MainWindow
from ui.about import AboutDialog
from ui.transform import TransformDialog
from viewport import Viewport
from window import Window
from objects.line import Line


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, icons: dict[str, QtGui.QIcon], *args, **kwargs) -> None:
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
        self.keyboardZoomIn = QtGui.QShortcut(QtGui.QKeySequence("+"), self)
        self.keyboardZoomOut = QtGui.QShortcut(QtGui.QKeySequence("-"), self)
        self.keyboardZoomIn.activated.connect(self.action_zoom_in)
        self.keyboardZoomOut.activated.connect(self.action_zoom_out)
        self.keyboardDeleteObject = QtGui.QShortcut(QtGui.QKeySequence("Del"), self)
        self.keyboardDeleteObject.activated.connect(self.action_delete_object)
        self.actionAdd_Object.setShortcut("Shift+A")
        self.actionTranslate.triggered.connect(
            self.action_window_transform_object_translate,
        )
        self.actionScale.triggered.connect(self.action_window_transform_object_scale)
        self.actionRotate.triggered.connect(self.action_window_transform_object_rotate)
        self.actionTranslate.setShortcuts(("G", "N"))
        self.actionScale.setShortcut("S")
        self.actionRotate.setShortcut("R")

        self._icons = icons

        self.objectsList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.objectsList.customContextMenuRequested.connect(self.context_menu_event)

        self._display_file = DisplayFile()
        self._window_obj = Window(self._display_file, (-100, -100), (100, 100))
        self._viewport = Viewport(self._window_obj, self.viewportCanvas)
        self._mouse_coordinate: QtCore.QPointF | None = None
        self.viewportCanvas.wheelEvent = self.mouse_scroll_event
        self.viewportCanvas.mouseMoveEvent = self.mouse_move_event
        self.viewportCanvas.mousePressEvent = self.mouse_press_event
        self.viewportCanvas.mouseReleaseEvent = self.mouse_release_event

        self._viewport.draw()
        # REMOVE: For testing purpose
        self.action_create_object(Line("test", (246, 158, 67), (-33, -33), (66, 66)))

    def context_menu_event(self, click_position: QtCore.QPoint) -> None:
        menu = QtWidgets.QMenu()
        menu.addAction(self.actionAdd_Object)
        item = self.objectsList.itemAt(click_position)
        if item:
            action_transform = menu.addAction("Transform")
            if action_transform:
                action_transform.triggered.connect(self.action_window_transform_object_translate)
                action_transform.setShortcut("N")
            action_delete = menu.addAction("Delete")
            if action_delete:
                action_delete.triggered.connect(self.action_delete_object)
                action_delete.setShortcut("Del")
        action = menu.exec(self.objectsList.mapToGlobal(click_position))

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_move_event(self, ev: QtGui.QMouseEvent | None) -> None:
        if ev and self._mouse_coordinate is not None:
            delta = self._mouse_coordinate - ev.position()
            self._window_obj.pan(
                delta.x() / (self.viewportCanvas.width() - 2),
                delta.y() / (self.viewportCanvas.height() - 2),
            )
            self._viewport.draw()
            self._mouse_coordinate = ev.position()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_release_event(self, ev: QtGui.QMouseEvent | None) -> None:
        if ev and ev.button() == Qt.MouseButton.MiddleButton:
            self._mouse_coordinate = None

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_press_event(self, ev: QtGui.QMouseEvent | None) -> None:
        if (
            ev
            and ev.button() == Qt.MouseButton.MiddleButton
            and ev.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            self._mouse_coordinate = ev.position()

    def mouse_scroll_event(self, a0: QtGui.QWheelEvent | None) -> None:
        """
        Listen to mouse scrolling events to allow zoooming with the mouse

        @param a0: The QWheelEvent object that will contain info about the scroll
        """
        if a0:
            if (a0.angleDelta().y() > 0):
                self.action_zoom_in()
            elif (a0.angleDelta().y() < 0):
                self.action_zoom_out()
            else:
                a0.ignore()

    def keyPressEvent(self, event: QtGui.QKeyEvent | None) -> None:  # noqa: N802
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
            self._icons[obj.get_type()],
            "{} [{}]".format(obj.get_name(), obj.get_type()),
            self.objectsList,
        )
        self._viewport.draw()

    def action_window_transform_object_translate(self) -> None:
        self.action_window_transform_object_tab(TransformDialog.Tab.Translate)

    def action_window_transform_object_scale(self) -> None:
        self.action_window_transform_object_tab(TransformDialog.Tab.Scale)

    def action_window_transform_object_rotate(self) -> None:
        self.action_window_transform_object_tab(TransformDialog.Tab.Rotate)

    def action_window_transform_object_tab(self, tab: TransformDialog.Tab) -> None:
        """
        Opens the Transform Object dialog
        """
        obj_index = self.objectsList.currentRow()
        if obj_index > -1 and obj_index < self.objectsList.count():
            obj = self._display_file.at(obj_index)
            dialog = TransformDialog(geometric_obj=obj, tab=tab)
            dialog.exec()
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
