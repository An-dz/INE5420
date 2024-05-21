from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from displayFile import DisplayFile
from io_files.wavefront_obj import WavefrontDescriptor
from objects.clipping import ClippingAlgo
from objects.geometricObject import GeometricObject
from objects.line import Line
from objects.wireframe import Wireframe
from ui.createObjectDialog import CreateObjectDialog
from ui.generated.mainWindow import Ui_MainWindow
from ui.aboutDialog import AboutDialog
from ui.transformDialog import TransformDialog
from viewport import Viewport
from window import Window


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main UI window"""

    def __init__(self, icons: dict[str, QtGui.QIcon], *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # set actions
        ## menu actions
        self.actionAdd_Object.triggered.connect(self.action_create_objectmenu)
        self.actionAbout.triggered.connect(self.action_about_menu)
        self.actionQuit.triggered.connect(self.action_quit_menu)
        self.actionWavefrontImport.triggered.connect(self.action_import_obj)
        self.actionWavefrontExport.triggered.connect(self.action_export_obj)
        self.actionWavefrontImport.setShortcut("Ctrl+O")
        self.actionWavefrontExport.setShortcut("Ctrl+S")

        ## movement buttons
        self.movementButtonDown.clicked.connect(self.action_move_down)
        self.movementButtonLeft.clicked.connect(self.action_move_left)
        self.movementButtonRight.clicked.connect(self.action_move_right)
        self.movementButtonUp.clicked.connect(self.action_move_up)
        self.movementButtonZoomOut.clicked.connect(self.action_zoom_out)
        self.movementButtonZoomIn.clicked.connect(self.action_zoom_in)
        self.movementButtonRotateClockwise.clicked.connect(self.action_rotate_clockwise)
        self.movementButtonRotateAntiClockwise.clicked.connect(
            self.action_rotate_anticlockwise,
        )

        ## zoom shortcut
        self.keyboardZoomIn = QtGui.QShortcut(QtGui.QKeySequence("+"), self)
        self.keyboardZoomOut = QtGui.QShortcut(QtGui.QKeySequence("-"), self)
        self.keyboardZoomIn.activated.connect(self.action_zoom_in)
        self.keyboardZoomOut.activated.connect(self.action_zoom_out)

        ## rotation shortcuts
        self.keyboardResetRotateXZF = QtGui.QShortcut(QtGui.QKeySequence("1"), self)
        self.keyboardResetRotateYZF = QtGui.QShortcut(QtGui.QKeySequence("3"), self)
        self.keyboardResetRotateXYF = QtGui.QShortcut(QtGui.QKeySequence("7"), self)
        self.keyboardResetRotateXZB = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+1"), self)
        self.keyboardResetRotateYZB = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+3"), self)
        self.keyboardResetRotateXYB = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+7"), self)
        self.keyboardRotateYawLeft = QtGui.QShortcut(QtGui.QKeySequence("6"), self)
        self.keyboardRotateYawRight = QtGui.QShortcut(QtGui.QKeySequence("4"), self)
        self.keyboardRotatePitchUp = QtGui.QShortcut(QtGui.QKeySequence("8"), self)
        self.keyboardRotatePitchDown = QtGui.QShortcut(QtGui.QKeySequence("2"), self)
        self.keyboardRotateRollClockwise = QtGui.QShortcut(
            QtGui.QKeySequence("Shift+6"), self,
        )
        self.keyboardRotateRollAntiClockwise = QtGui.QShortcut(
            QtGui.QKeySequence("Shift+4"), self,
        )
        self.keyboardMoveRight = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+6"), self)
        self.keyboardMoveLeft = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+4"), self)
        self.keyboardMoveUp = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+8"), self)
        self.keyboardMoveDown = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+2"), self)
        self.keyboardResetRotateXZF.activated.connect(
            lambda: self.action_rotate_reset(-90, 0),  # xz y->out
        )
        self.keyboardResetRotateYZF.activated.connect(
            lambda: self.action_rotate_reset(0, 90),  # yz x->out
        )
        self.keyboardResetRotateXYF.activated.connect(
            lambda: self.action_rotate_reset(0, 0),  # xy z->out
        )
        self.keyboardResetRotateXZB.activated.connect(
            lambda: self.action_rotate_reset(90, 0),  # xz y->in
        )
        self.keyboardResetRotateYZB.activated.connect(
            lambda: self.action_rotate_reset(0, -90),  # yz x->in
        )
        self.keyboardResetRotateXYB.activated.connect(
            lambda: self.action_rotate_reset(0, 180),  # xy z->in
        )
        self.keyboardRotateYawLeft.activated.connect(self.action_yaw_left)
        self.keyboardRotateYawRight.activated.connect(self.action_yaw_right)
        self.keyboardRotatePitchUp.activated.connect(self.action_pitch_up)
        self.keyboardRotatePitchDown.activated.connect(self.action_pitch_down)
        self.keyboardRotateRollClockwise.activated.connect(self.action_rotate_clockwise)
        self.keyboardRotateRollAntiClockwise.activated.connect(
            self.action_rotate_anticlockwise,
        )
        self.keyboardMoveLeft.activated.connect(self.action_move_left)
        self.keyboardMoveRight.activated.connect(self.action_move_right)
        self.keyboardMoveUp.activated.connect(self.action_move_up)
        self.keyboardMoveDown.activated.connect(self.action_move_down)

        ##
        self.projectionRadioParallel.toggled.connect(self.action_projection_parallel)
        self.projectionRadioPerspective.toggled.connect(
            self.action_projection_perspective,
        )
        self.keyboardProjectionToggle = QtGui.QShortcut(QtGui.QKeySequence("5"), self)
        self.keyboardProjectionToggle.activated.connect(self.action_projection_toggle)

        ##
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

        self._clipping_algorithm = ClippingAlgo.LiangBarsky
        self.actionLiang_Barsky.setChecked(True)
        self._clipping_status = QtWidgets.QLabel()
        self._clipping_status.setText(
            "Clipping: {}".format(self._clipping_algorithm.name),
        )
        self.statusbar.addPermanentWidget(self._clipping_status)
        clipping_group = QtGui.QActionGroup(self)
        clipping_group.addAction(self.actionPoints)
        clipping_group.addAction(self.actionCohen_Sutherland)
        clipping_group.addAction(self.actionLiang_Barsky)
        clipping_group.addAction(self.actionNicholl_Lee_Nicholl)
        self.actionNicholl_Lee_Nicholl.setVisible(False)
        self.actionPoints.triggered.connect(
            lambda: self.action_set_clipping_algorithm(
                ClippingAlgo.Points,
            ),
        )
        self.actionCohen_Sutherland.triggered.connect(
            lambda: self.action_set_clipping_algorithm(
                ClippingAlgo.CohenSutherland,
            ),
        )
        self.actionLiang_Barsky.triggered.connect(
            lambda: self.action_set_clipping_algorithm(
                ClippingAlgo.LiangBarsky,
            ),
        )
        self.actionNicholl_Lee_Nicholl.triggered.connect(
            lambda: self.action_set_clipping_algorithm(
                ClippingAlgo.NichollLeeNicholl,
            ),
        )

        re = QtCore.QRegularExpression("-?\\d*\\.\\d*")
        self.rotationAngleField.setValidator(QtGui.QRegularExpressionValidator(re))

        self._icons = icons

        self.objectsList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.objectsList.customContextMenuRequested.connect(self.context_menu_event)

        self._display_file = DisplayFile(self._clipping_algorithm)
        self._window_obj = Window(self._display_file, (0, 0, 0), (200, 200, 0))
        self._viewport = Viewport(self._window_obj, self.viewportCanvas)
        self._mouse_coordinate: QtCore.QPointF | None = None
        self._mouse_modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier
        self.viewportCanvas.wheelEvent = self.mouse_scroll_event
        self.viewportCanvas.mouseMoveEvent = self.mouse_move_event
        self.viewportCanvas.mousePressEvent = self.mouse_press_event
        self.viewportCanvas.mouseReleaseEvent = self.mouse_release_event

        self.action_create_object(Line("x", (255, 0, 0), (0, 0, 0, 1), (50, 0, 0, 1)))
        self.action_create_object(Line("y", (0, 255, 0), (0, 0, 0, 1), (0, 50, 0, 1)))
        self.action_create_object(Line("z", (0, 0, 255), (0, 0, 0, 1), (0, 0, 50, 1)))
        self.action_create_object(Wireframe(
            "obj",
            (255, 255, 0),
            [(0, 0, 0, 1), (50, 50, 50, 1), (50, 79.929, 0, 1)],
            [((0, 0, 0, 1), (50, 50, 50, 1)), ((50, 50, 50, 1), (50, 79.929, 0, 1))],
        ))
        self.action_create_object(Wireframe(
            "cube",
            (255, 0, 255),
            [
                (60, 60, 0, 1), (-60, -60, 0, 1), (60, -60, 0, 1), (-60, 60, 0, 1),
                (60, 60, 60, 1), (-60, -60, 60, 1), (60, -60, 60, 1), (-60, 60, 60, 1),
            ],
            [
                ((60, 60, 0, 1), (60, -60, 0, 1)),
                ((60, -60, 0, 1), (-60, -60, 0, 1)),
                ((-60, -60, 0, 1), (-60, 60, 0, 1)),
                ((-60, 60, 0, 1), (60, 60, 0, 1)),
                ((60, 60, 60, 1), (60, -60, 60, 1)),
                ((60, -60, 60, 1), (-60, -60, 60, 1)),
                ((-60, -60, 60, 1), (-60, 60, 60, 1)),
                ((-60, 60, 60, 1), (60, 60, 60, 1)),
                ((60, 60, 0, 1), (60, 60, 60, 1)),
                ((60, -60, 0, 1), (60, -60, 60, 1)),
                ((-60, -60, 0, 1), (-60, -60, 60, 1)),
                ((-60, 60, 0, 1), (-60, 60, 60, 1)),
            ],
        ))
        self.action_create_object(Wireframe(
            "cube_back",
            (0, 255, 255),
            [
                (60, 60, 60, 1), (-60, -60, 60, 1), (60, -60, 60, 1), (-60, 60, 60, 1),
            ],
            [
                ((60, 60, 60, 1), (60, -60, 60, 1)),
                ((60, -60, 60, 1), (-60, -60, 60, 1)),
                ((-60, -60, 60, 1), (-60, 60, 60, 1)),
                ((-60, 60, 60, 1), (60, 60, 60, 1)),
            ],
        ))
        self._viewport.draw(-1)

        self.objectsList.currentRowChanged.connect(lambda row: self._viewport.draw(row))

    def context_menu_event(self, click_position: QtCore.QPoint) -> None:
        """
        Listens to right-click event on object list

        This allows adding options only on list items

        @param click_position: Position that is being right-clicked relative to widget
        """
        menu = QtWidgets.QMenu()
        menu.addAction(self.actionAdd_Object)
        item = self.objectsList.itemAt(click_position)
        if item:
            menu.addSeparator()
            action_transform = menu.addAction("Transform")
            if action_transform:
                action_transform.triggered.connect(
                    self.action_window_transform_object_translate,
                )
                action_transform.setShortcut("N")
            action_delete = menu.addAction("Delete")
            if action_delete:
                action_delete.triggered.connect(self.action_delete_object)
                action_delete.setShortcut("Del")
        menu.exec(self.objectsList.mapToGlobal(click_position))

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_move_event(self, ev: QtGui.QMouseEvent | None) -> None:
        """
        Listens to mouse movement events on viewport

        @note Only runs after `mouse_click_event` is run

        @param ev: Mouse event object
        """
        if ev and self._mouse_coordinate is not None:
            delta = self._mouse_coordinate - ev.position()
            if self._mouse_modifiers & Qt.KeyboardModifier.ShiftModifier:
                self._window_obj.pan(
                    delta.x() / (self.viewportCanvas.width() - 2),
                    delta.y() / (self.viewportCanvas.height() - 2),
                )
            elif self._mouse_modifiers & Qt.KeyboardModifier.ControlModifier:
                self._window_obj.zoom(
                    1 - (2 * delta.y() / (self.viewportCanvas.height() - 2)),
                )
            self._viewport.draw(self.objectsList.currentRow())
            self._mouse_coordinate = ev.position()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_release_event(self, ev: QtGui.QMouseEvent | None) -> None:
        """
        Listens to mouse button release events on viewport

        @note Stops listening to click'n'hold gestures

        @param ev: Mouse event object
        """
        if ev and ev.button() == Qt.MouseButton.MiddleButton:
            self._mouse_coordinate = None

    @QtCore.pyqtSlot(QtCore.QPoint)
    def mouse_press_event(self, ev: QtGui.QMouseEvent | None) -> None:
        """
        Listens to mouse button press events on viewport

        @note Starts listening to click'n'hold gestures

        @param ev: Mouse event object
        """
        if (
            ev
            and ev.button() == Qt.MouseButton.MiddleButton
        ):
            self._mouse_modifiers = ev.modifiers()
            if (
                self._mouse_modifiers & Qt.KeyboardModifier.ShiftModifier
                or self._mouse_modifiers & Qt.KeyboardModifier.ControlModifier
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
            print(event)
            numpad_mod = event.modifiers() & Qt.KeyboardModifier.KeypadModifier
            shift_mod = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ctrl_mod = event.modifiers() & Qt.KeyboardModifier.ControlModifier
            print(numpad_mod, shift_mod, ctrl_mod)
            if numpad_mod:
                if event.key() == Qt.Key.Key_Plus:
                    self.action_zoom_in()
                elif event.key() == Qt.Key.Key_Minus:
                    self.action_zoom_out()
                elif event.key() == Qt.Key.Key_1:
                    if ctrl_mod:
                        self.action_rotate_reset(90, 0)  # xz y->in
                    else:
                        self.action_rotate_reset(-90, 0)  # xz y->out
                elif event.key() == Qt.Key.Key_2:
                    if ctrl_mod:
                        self.action_move_down()
                    else:
                        self.action_pitch_down()
                elif event.key() == Qt.Key.Key_3:
                    if ctrl_mod:
                        self.action_rotate_reset(0, 90)  # yz x->out
                    else:
                        self.action_rotate_reset(0, -90)  # yz x->in
                elif event.key() == Qt.Key.Key_4:
                    if ctrl_mod:
                        self.action_move_left()
                    elif shift_mod:
                        self.action_rotate_anticlockwise()
                    else:
                        self.action_yaw_right()
                elif event.key() == Qt.Key.Key_5:
                    self.action_projection_toggle()
                elif event.key() == Qt.Key.Key_6:
                    if ctrl_mod:
                        self.action_move_right()
                    elif shift_mod:
                        self.action_rotate_clockwise()
                    else:
                        self.action_yaw_left()
                elif event.key() == Qt.Key.Key_7:
                    if ctrl_mod:
                        self.action_rotate_reset(0, 0)  # xy z->out
                    else:
                        self.action_rotate_reset(0, 180)  # xy z->in
                elif event.key() == Qt.Key.Key_8:
                    if ctrl_mod:
                        self.action_move_up()
                    else:
                        self.action_pitch_up()

    def action_delete_object(self) -> None:
        """
        Deletes an object from the world through the UI list

        @note The deleted object is the currently selected object
        """
        obj_index = self.objectsList.currentRow()
        if obj_index > -1 and obj_index < self.objectsList.count():
            self.objectsList.takeItem(obj_index)
            self._display_file.remove(obj_index)
            self._viewport.draw(self.objectsList.currentRow())

    def action_move_left(self) -> None:
        """
        Click on move left button
        """
        self._window_obj.move(-0.03, 0)
        self._viewport.draw(self.objectsList.currentRow())

    def action_move_right(self) -> None:
        """
        Click on move right button
        """
        self._window_obj.move(0.03, 0)
        self._viewport.draw(self.objectsList.currentRow())

    def action_move_up(self) -> None:
        """
        Click on move up button
        """
        self._window_obj.move(0, 0.03)
        self._viewport.draw(self.objectsList.currentRow())

    def action_move_down(self) -> None:
        """
        Click on move down button
        """
        self._window_obj.move(0, -0.03)
        self._viewport.draw(self.objectsList.currentRow())

    def action_zoom_out(self) -> None:
        """
        Click on zoom out button
        """
        self._window_obj.zoom(1.25)
        self._viewport.draw(self.objectsList.currentRow())

    def action_zoom_in(self) -> None:
        """
        Click on zoom in button
        """
        self._window_obj.zoom(0.8)
        self._viewport.draw(self.objectsList.currentRow())

    def action_rotate_clockwise(self) -> None:
        """
        Rotate the world clockwise

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = float(self.rotationAngleField.text())
            self._window_obj.roll(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_rotate_anticlockwise(self) -> None:
        """
        Rotate the world anti-clockwise

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = -float(self.rotationAngleField.text())
            self._window_obj.roll(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_yaw_left(self) -> None:
        """
        Yaw the camera left

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = float(self.rotationAngleField.text())
            self._window_obj.yaw(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_yaw_right(self) -> None:
        """
        Yaw the camera right

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = -float(self.rotationAngleField.text())
            self._window_obj.yaw(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_pitch_up(self) -> None:
        """
        Rotate the world clockwise

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = float(self.rotationAngleField.text())
            self._window_obj.pitch(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_pitch_down(self) -> None:
        """
        Rotate the world anti-clockwise

        @note Angle is set on the interface and is loaded on the fly
        """
        try:
            angle = -float(self.rotationAngleField.text())
            self._window_obj.pitch(angle)
            self._viewport.draw(self.objectsList.currentRow())
        except Exception:
            pass

    def action_projection_parallel(self, state: bool) -> None:
        if state:
            self._window_obj.set_projection_parallel()
            self._viewport.draw(self.objectsList.currentRow())

    def action_projection_perspective(self, state: bool) -> None:
        if state:
            self._window_obj.set_projection_perspective()
            self._viewport.draw(self.objectsList.currentRow())

    def action_projection_toggle(self) -> None:
        d = self._window_obj.get_z_clip()
        if d == 1:
            self._window_obj.set_projection_perspective()
        else:
            self._window_obj.set_projection_parallel()
        self._viewport.draw(self.objectsList.currentRow())

    def action_rotate_reset(self, x: float, y: float) -> None:
        """
        Resets the rotation back to Y and V being aligned
        """
        self._window_obj.set_angles(x, y, 0)
        self._viewport.draw(self.objectsList.currentRow())

    def action_set_clipping_algorithm(
        self,
        clipping_algorithm: ClippingAlgo,
    ) -> None:
        """
        Sets the current clipping algorithm

        @paraam checked: Whether the button was checked or unchecked
        """
        self._clipping_algorithm = clipping_algorithm
        self._display_file.set_clipping_algorithm(clipping_algorithm)
        self._viewport.draw(self.objectsList.currentRow())
        self._clipping_status.setText(
            "Clipping: {}".format(self._clipping_algorithm.name),
        )

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
        self._viewport.draw(self.objectsList.currentRow())

    def action_window_transform_object_translate(self) -> None:
        """
        Opens the Transform Object dialog on translate tab
        """
        self.action_window_transform_object_tab(TransformDialog.Tab.Translate)

    def action_window_transform_object_scale(self) -> None:
        """
        Opens the Transform Object dialog on scale tab
        """
        self.action_window_transform_object_tab(TransformDialog.Tab.Scale)

    def action_window_transform_object_rotate(self) -> None:
        """
        Opens the Transform Object dialog on rotate tab
        """
        self.action_window_transform_object_tab(TransformDialog.Tab.Rotate)

    def action_window_transform_object_tab(self, tab: TransformDialog.Tab) -> None:
        """
        Opens the Transform Object dialog

        @param tab: Which tab to open the dialog on
        """
        obj_index = self.objectsList.currentRow()
        if obj_index > -1 and obj_index < self.objectsList.count():
            obj = self._display_file.at(obj_index)
            dialog = TransformDialog(
                geometric_obj=obj,
                window=self._window_obj,
                tab=tab,
                clipping_algorithm=self._clipping_algorithm,
            )
            dialog.exec()
            self._viewport.draw(self.objectsList.currentRow())

    def action_import_obj(self) -> None:
        """
        Import a Wavefront OBJ scene

        @note Will open a dialog for choosing the file
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Wavefront (.obj)",
            ".",
            "Wavefront (*.obj)",
        )
        for obj in WavefrontDescriptor.import_file(file_name[0]):
            self.action_create_object(obj)

    def action_export_obj(self) -> None:
        """
        Export a scene in Wavefront OBJ format with MTL

        @note Will open a dialog for choosing the save file
        """
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Wavefront (.obj)",
            ".",
            "Wavefront (*.obj)",
        )
        WavefrontDescriptor.export_file(file_name[0], self._display_file)

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
