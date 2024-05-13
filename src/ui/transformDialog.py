from enum import IntEnum
from typing import Literal

from PyQt6 import QtCore, QtGui, QtWidgets
import numpy as np
from numpy.typing import NDArray

from objects.clipping import ClippingAlgo
from objects.geometricObject import GeometricObject
import transformation as transform
from ui.generated.transformDialog import Ui_TransformDialog
from window import Window


class TransformDialog(QtWidgets.QDialog, Ui_TransformDialog):
    """Dialog for transforming an object"""
    class Tab(IntEnum):
        """Enum to control which tab to start on open"""
        Translate = 0
        Scale = 1
        Rotate = 2

    def __init__(
        self,
        geometric_obj: GeometricObject,
        window: Window,
        clipping_algorithm: ClippingAlgo,
        tab: Tab = Tab.Translate,
        *args,
        **kwargs,
    ) -> None:
        """
        Opens the dialog on the defined tab

        @param geometric_obj: Object being transformed
        @param tab: Which tab to start with on open
        """
        super(TransformDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.checkBoxScaleAspect.stateChanged.connect(self.event_scale_aspect_changed)
        self.inputScaleSx.textChanged.connect(self.event_scale_x_changed)
        self.radioAxisX.toggled.connect(lambda s: self.event_rotate_axis_toggled("x", s))
        self.radioAxisY.toggled.connect(lambda s: self.event_rotate_axis_toggled("y", s))
        self.radioAxisZ.toggled.connect(lambda s: self.event_rotate_axis_toggled("z", s))
        self.radioAxisCenter.toggled.connect(self.event_rotate_center_toggled)
        self.radioAxisArbitrary.toggled.connect(self.event_rotate_arbitrary_toggled)
        self.buttonTransformationAdd.clicked.connect(self.event_transformation_add)
        self.buttonTransformationRemove.clicked.connect(self.event_transformation_remove)
        re = QtCore.QRegularExpression("-?\\d*(\\.\\d*)?")
        self.inputTranslateDx.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputTranslateDy.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputTranslateDz.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputScaleSx.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputScaleSy.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputScaleSz.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationAngle.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointX1.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointY1.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointZ1.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointX2.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointY2.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointZ2.setValidator(QtGui.QRegularExpressionValidator(re))
        self.tabWidgetTransformations.setCurrentIndex(tab)

        self._line_clip = clipping_algorithm
        self._window = window
        self._geometric_obj = geometric_obj
        self._obj_center = self._geometric_obj.get_center()
        self._transform_list: list[NDArray[np.float64]] = []

        self.inputRotationPointX2.setText("1")

    def accept(self) -> None:
        """
        Event fired when the dialog is accepted
        """
        if len(self._transform_list) == 1:
            transform_matrix = self._transform_list[0]
            self._geometric_obj.transform(
                transform_matrix,
                self._window.get_scn_matrix(),
                self._line_clip,
            )
        elif len(self._transform_list) > 1:
            transform_matrix = np.linalg.multi_dot(self._transform_list)
            self._geometric_obj.transform(
                transform_matrix,
                self._window.get_scn_matrix(),
                self._line_clip,
            )
        self.close()

    def event_scale_aspect_changed(self, checked: int) -> None:
        """
        Event fired when the aspect ratio checkbox is checked on scale tab

        @param checked: new state of the checkbox
        """
        self.inputScaleSy.setEnabled(checked == 0)
        self.label_scaleSy.setEnabled(checked == 0)
        self.inputScaleSz.setEnabled(checked == 0)
        self.label_scaleSz.setEnabled(checked == 0)
        # if itś checked we set Y scale equal to X
        if checked > 0:
            self.inputScaleSy.setText(self.inputScaleSx.text())
            self.inputScaleSz.setText(self.inputScaleSx.text())

    def event_scale_x_changed(self, text: str) -> None:
        """
        Event fired when a value is entered for X scale

        @param text: new value for X scaling
        """
        # if the aspect ratio is checked we keep both X & Y equal
        if self.checkBoxScaleAspect.checkState() == QtCore.Qt.CheckState.Checked:
            self.inputScaleSy.setText(text)
            self.inputScaleSz.setText(text)

    def event_rotate_center_toggled(self, state: bool) -> None:
        """
        Event fired when rotate around object center is toggled

        @param state: whether the radio box was selected or not
        """
        # if is's toggled on we set the origin on the object's center
        self.inputRotationPointX2.setEnabled(state)
        self.inputRotationPointY2.setEnabled(state)
        self.inputRotationPointZ2.setEnabled(state)
        self.label_PointX2.setEnabled(state)
        self.label_PointY2.setEnabled(state)
        self.label_PointZ2.setEnabled(state)
        if state:
            self.inputRotationPointX1.setText(str(self._obj_center[0]))
            self.inputRotationPointY1.setText(str(self._obj_center[1]))
            self.inputRotationPointZ1.setText(str(self._obj_center[2]))
            left_align = "QLineEdit { qproperty-cursorPosition: 0; }"
            self.inputRotationPointX1.setStyleSheet(left_align)
            self.inputRotationPointY1.setStyleSheet(left_align)
            self.inputRotationPointZ1.setStyleSheet(left_align)
            self.inputRotationPointX2.setText(None)
            self.inputRotationPointY2.setText(None)
            self.inputRotationPointZ2.setText(None)

    def event_rotate_axis_toggled(
        self,
        axis: Literal["x"] | Literal["y"] | Literal["z"],
        state: bool,
    ) -> None:
        """
        Event fired when rotate around origin is toggled

        @param state: whether the radio box was selected or not
        """
        # if is's toggled on we set the starting point on 0,0
        if state:
            self.inputRotationPointX1.setText(None)
            self.inputRotationPointY1.setText(None)
            self.inputRotationPointZ1.setText(None)
            self.inputRotationPointX2.setText("1" if axis == "x" else "0")
            self.inputRotationPointY2.setText("1" if axis == "y" else "0")
            self.inputRotationPointZ2.setText("1" if axis == "z" else "0")

    def event_rotate_arbitrary_toggled(self, state: bool) -> None:
        """
        Event fired when rotate around custom axis is toggled

        @param state: whether the radio box went to selected or not
        """
        self.inputRotationPointX1.setEnabled(state)
        self.inputRotationPointY1.setEnabled(state)
        self.inputRotationPointZ1.setEnabled(state)
        self.inputRotationPointX2.setEnabled(state)
        self.inputRotationPointY2.setEnabled(state)
        self.inputRotationPointZ2.setEnabled(state)
        self.label_PointX1.setEnabled(state)
        self.label_PointY1.setEnabled(state)
        self.label_PointZ1.setEnabled(state)
        self.label_PointX2.setEnabled(state)
        self.label_PointY2.setEnabled(state)
        self.label_PointZ2.setEnabled(state)
        # if is's toggled on we set the axis to 0,0,0 - 0,0,0
        if state:
            self.inputRotationPointX1.setText(None)
            self.inputRotationPointY1.setText(None)
            self.inputRotationPointZ1.setText(None)
            self.inputRotationPointX2.setText(None)
            self.inputRotationPointY2.setText(None)
            self.inputRotationPointZ2.setText(None)

    def event_transformation_add(self) -> None:
        """
        Event fired when clicking the Add button
        """
        # we check the tab to know what type of transformation to add
        current_tab = self.tabWidgetTransformations.currentIndex()
        if current_tab == 0:
            dx = 0.0
            dy = 0.0
            dz = 0.0
            try:
                dx = float(self.inputTranslateDx.text())
            except Exception:
                pass
            try:
                dy = float(self.inputTranslateDy.text())
            except Exception:
                pass
            try:
                dz = float(self.inputTranslateDz.text())
            except Exception:
                pass
            self._transform_list.append(transform.translate(dx, dy, dz))
            QtWidgets.QListWidgetItem(
                "Translate ({}, {}, {})".format(dx, dy, dz),
                self.listTransformations,
            )
        elif current_tab == 1:
            sx = 0.0
            sy = 0.0
            sz = 0.0
            try:
                sx = float(self.inputScaleSx.text())
            except Exception:
                pass
            try:
                sy = float(self.inputScaleSy.text())
            except Exception:
                pass
            try:
                sz = float(self.inputScaleSz.text())
            except Exception:
                pass
            self._transform_list.append(transform.scale(self._obj_center, sx, sy, sz))
            QtWidgets.QListWidgetItem(
                "Scale ({}, {}, {})".format(sx, sy, sz),
                self.listTransformations,
            )
        elif current_tab == 2:
            try:
                teta = float(self.inputRotationAngle.text())
            except Exception:
                return

            x1 = 0.
            y1 = 0.
            z1 = 0.
            x2 = 0.
            y2 = 0.
            z2 = 0.
            try:
                x1 = float(self.inputRotationPointX1.text())
            except Exception:
                pass
            try:
                y1 = float(self.inputRotationPointY1.text())
            except Exception:
                pass
            try:
                z1 = float(self.inputRotationPointZ1.text())
            except Exception:
                pass
            try:
                x2 = float(self.inputRotationPointX2.text())
            except Exception:
                pass
            try:
                y2 = float(self.inputRotationPointY2.text())
            except Exception:
                pass
            try:
                z2 = float(self.inputRotationPointZ2.text())
            except Exception:
                pass

            axis = [(x1, y1, z1), (x2, y2, z2)]

            if axis[0] == axis[1]:
                background = "background-color: rgba(255, 0, 0, .2)"
                self.inputRotationPointX2.setStyleSheet(background)
                self.inputRotationPointY2.setStyleSheet(background)
                self.inputRotationPointZ2.setStyleSheet(background)
                error_tooltip = "Second point must not be equal to the first"
                self.inputRotationPointX2.setToolTip(error_tooltip)
                self.inputRotationPointY2.setToolTip(error_tooltip)
                self.inputRotationPointZ2.setToolTip(error_tooltip)
                return

            self.inputRotationPointX2.setStyleSheet(None)
            self.inputRotationPointY2.setStyleSheet(None)
            self.inputRotationPointZ2.setStyleSheet(None)
            self.inputRotationPointX2.setToolTip(None)
            self.inputRotationPointY2.setToolTip(None)
            self.inputRotationPointZ2.setToolTip(None)

            if self.radioAxisX.isChecked():
                rotation_type = "X Axis"
            elif self.radioAxisY.isChecked():
                rotation_type = "Y Axis"
            elif self.radioAxisZ.isChecked():
                rotation_type = "Z Axis"
            elif self.radioAxisCenter.isChecked():
                rotation_type = "Center-{} Axis".format(axis[1])
            elif self.radioAxisArbitrary.isChecked():
                rotation_type = "{} Axis".format(axis)
            else:
                return
            self._transform_list.append(
                transform.rotate_around_z(axis, np.pi * teta / 180),
            )
            QtWidgets.QListWidgetItem(
                "Rotate {}° @ {}".format(teta, rotation_type),
                self.listTransformations,
            )

    def event_transformation_remove(self) -> None:
        """
        Event fired when clicking the Delete button
        """
        obj_index = self.listTransformations.currentRow()
        if obj_index > -1 and obj_index < self.listTransformations.count():
            self.listTransformations.takeItem(obj_index)
            self._transform_list.pop(obj_index)
