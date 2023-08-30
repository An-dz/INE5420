from enum import IntEnum
from PyQt6 import QtGui, QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import numpy as np
from numpy.typing import NDArray
from objects.geometricObject import GeometricObject
import transformation as transform

from ui.generated.transform import Ui_TransformDialog


class TransformDialog(QtWidgets.QDialog, Ui_TransformDialog):
    class Tab(IntEnum):
        Translate = 0
        Scale = 1
        Rotate = 2

    """A simple about screen just to show who made this"""
    def __init__(
        self,
        geometric_obj: GeometricObject,
        tab: Tab = Tab.Translate,
        *args,
        **kwargs,
    ) -> None:
        super(TransformDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.checkBoxScaleAspect.stateChanged.connect(self.event_scale_aspect_changed)
        self.inputScaleSx.textChanged.connect(self.event_scale_x_changed)
        self.radioRotateCenter.toggled.connect(self.event_rotate_center_toggled)
        self.radioRotateOrigin.toggled.connect(self.event_rotate_origin_toggled)
        self.radioRotatePoint.toggled.connect(self.event_rotate_point_toggled)
        self.buttonTransformationAdd.clicked.connect(self.event_transformation_add)
        self.buttonTransformationRemove.clicked.connect(self.event_transformation_remove)
        re = QtCore.QRegularExpression("-?\\d*(\\.\\d*)?")
        self.inputTranslateDx.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputTranslateDy.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputScaleSx.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputScaleSy.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationAngle.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointX.setValidator(QtGui.QRegularExpressionValidator(re))
        self.inputRotationPointY.setValidator(QtGui.QRegularExpressionValidator(re))
        self.tabWidgetTransformations.setCurrentIndex(tab)

        self._geometric_obj = geometric_obj
        self._obj_center = self._geometric_obj.get_center()
        self._transform_list: list[NDArray[np.float64]] = []

        self.inputRotationPointX.setText(str(self._obj_center[0]))
        self.inputRotationPointY.setText(str(self._obj_center[1]))

    def accept(self) -> None:
        """
        Event fired when the dialog is accepted
        """
        if len(self._transform_list) == 1:
            transform_matrix = self._transform_list[0]
            self._geometric_obj.transform(transform_matrix)
        elif len(self._transform_list) > 1:
            transform_matrix = np.linalg.multi_dot(self._transform_list)
            self._geometric_obj.transform(transform_matrix)
        self.close()

    def event_scale_aspect_changed(self, checked: int) -> None:
        self.inputScaleSy.setEnabled(checked == 0)
        self.label_scaleSy.setEnabled(checked == 0)
        if checked > 0:
            self.inputScaleSy.setText(self.inputScaleSx.text())

    def event_scale_x_changed(self, text: str) -> None:
        if self.checkBoxScaleAspect.checkState() == Qt.CheckState.Checked:
            self.inputScaleSy.setText(text)

    def event_rotate_center_toggled(self, state: bool) -> None:
        if state:
            self.inputRotationPointX.setText(str(self._obj_center[0]))
            self.inputRotationPointY.setText(str(self._obj_center[1]))

    def event_rotate_origin_toggled(self, state: bool) -> None:
        if state:
            self.inputRotationPointX.setText(None)
            self.inputRotationPointY.setText(None)

    def event_rotate_point_toggled(self, state: bool) -> None:
        self.groupBoxRotationPoint.setEnabled(state)
        if state:
            self.inputRotationPointX.setText(None)
            self.inputRotationPointY.setText(None)

    def event_transformation_add(self) -> None:
        current_tab = self.tabWidgetTransformations.currentIndex()
        if current_tab == 0:
            dx = 0.0
            dy = 0.0
            try:
                dx = float(self.inputTranslateDx.text())
            except Exception:
                return
            try:
                dy = float(self.inputTranslateDy.text())
            except Exception:
                return
            self._transform_list.append(transform.translate(dx, dy))
            QtWidgets.QListWidgetItem(
                "Translate ({}, {})".format(dx, dy),
                self.listTransformations,
            )
        elif current_tab == 1:
            sx = 0.0
            sy = 0.0
            try:
                sx = float(self.inputScaleSx.text())
            except Exception:
                return
            try:
                sy = float(self.inputScaleSy.text())
            except Exception:
                return
            self._transform_list.append(transform.scale(self._obj_center, sx, sy))
            QtWidgets.QListWidgetItem(
                "Scale ({}, {})".format(sx, sy),
                self.listTransformations,
            )
        elif current_tab == 2:
            teta = 0.0
            try:
                teta = float(self.inputRotationAngle.text())
            except Exception:
                return
            center = np.array([0, 0])
            rotation_type = "origin"
            if self.radioRotateCenter.isChecked():
                rotation_type = "object"
                center = self._obj_center
            elif self.radioRotatePoint.isChecked():
                try:
                    center = np.array([
                        float(self.inputRotationPointX.text()),
                        float(self.inputRotationPointY.text()),
                    ])
                except Exception:
                    return
                rotation_type = "({}, {})".format(center[0], center[1])
            self._transform_list.append(
                transform.rotate_around(center, np.pi * teta / 180),
            )
            QtWidgets.QListWidgetItem(
                "Rotate {}° @ {}".format(teta, rotation_type),
                self.listTransformations,
            )

    def event_transformation_remove(self) -> None:
        obj_index = self.listTransformations.currentRow()
        if obj_index > -1 and obj_index < self.listTransformations.count():
            self.listTransformations.takeItem(obj_index)
            self._transform_list.pop(obj_index)
