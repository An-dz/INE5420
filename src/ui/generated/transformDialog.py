# Form implementation generated from reading ui file 'ui/transform.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TransformDialog(object):
    def setupUi(self, TransformDialog):
        TransformDialog.setObjectName("TransformDialog")
        TransformDialog.resize(540, 393)
        self.verticalLayout = QtWidgets.QVBoxLayout(TransformDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidgetTransformations = QtWidgets.QTabWidget(parent=TransformDialog)
        self.tabWidgetTransformations.setMinimumSize(QtCore.QSize(288, 0))
        self.tabWidgetTransformations.setObjectName("tabWidgetTransformations")
        self.tab_translate = QtWidgets.QWidget()
        self.tab_translate.setObjectName("tab_translate")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_translate)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBoxTranslate = QtWidgets.QGroupBox(parent=self.tab_translate)
        self.groupBoxTranslate.setObjectName("groupBoxTranslate")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBoxTranslate)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_Dx = QtWidgets.QLabel(parent=self.groupBoxTranslate)
        self.label_Dx.setObjectName("label_Dx")
        self.horizontalLayout_6.addWidget(self.label_Dx)
        self.inputTranslateDx = QtWidgets.QLineEdit(parent=self.groupBoxTranslate)
        self.inputTranslateDx.setInputMask("")
        self.inputTranslateDx.setObjectName("inputTranslateDx")
        self.horizontalLayout_6.addWidget(self.inputTranslateDx)
        self.label_Dy = QtWidgets.QLabel(parent=self.groupBoxTranslate)
        self.label_Dy.setObjectName("label_Dy")
        self.horizontalLayout_6.addWidget(self.label_Dy)
        self.inputTranslateDy = QtWidgets.QLineEdit(parent=self.groupBoxTranslate)
        self.inputTranslateDy.setObjectName("inputTranslateDy")
        self.horizontalLayout_6.addWidget(self.inputTranslateDy)
        self.verticalLayout_6.addWidget(self.groupBoxTranslate)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.tabWidgetTransformations.addTab(self.tab_translate, "")
        self.tab_scale = QtWidgets.QWidget()
        self.tab_scale.setObjectName("tab_scale")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_scale)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBoxScale = QtWidgets.QGroupBox(parent=self.tab_scale)
        self.groupBoxScale.setObjectName("groupBoxScale")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBoxScale)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_scaleSx = QtWidgets.QLabel(parent=self.groupBoxScale)
        self.label_scaleSx.setObjectName("label_scaleSx")
        self.horizontalLayout_5.addWidget(self.label_scaleSx)
        self.inputScaleSx = QtWidgets.QLineEdit(parent=self.groupBoxScale)
        self.inputScaleSx.setObjectName("inputScaleSx")
        self.horizontalLayout_5.addWidget(self.inputScaleSx)
        self.checkBoxScaleAspect = QtWidgets.QCheckBox(parent=self.groupBoxScale)
        self.checkBoxScaleAspect.setText("")
        self.checkBoxScaleAspect.setChecked(True)
        self.checkBoxScaleAspect.setObjectName("checkBoxScaleAspect")
        self.horizontalLayout_5.addWidget(self.checkBoxScaleAspect)
        self.label_scaleSy = QtWidgets.QLabel(parent=self.groupBoxScale)
        self.label_scaleSy.setEnabled(False)
        self.label_scaleSy.setObjectName("label_scaleSy")
        self.horizontalLayout_5.addWidget(self.label_scaleSy)
        self.inputScaleSy = QtWidgets.QLineEdit(parent=self.groupBoxScale)
        self.inputScaleSy.setEnabled(False)
        self.inputScaleSy.setObjectName("inputScaleSy")
        self.horizontalLayout_5.addWidget(self.inputScaleSy)
        self.verticalLayout_7.addWidget(self.groupBoxScale)
        spacerItem1 = QtWidgets.QSpacerItem(20, 211, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.tabWidgetTransformations.addTab(self.tab_scale, "")
        self.tab_rotate = QtWidgets.QWidget()
        self.tab_rotate.setObjectName("tab_rotate")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_rotate)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBoxRotationType = QtWidgets.QGroupBox(parent=self.tab_rotate)
        self.groupBoxRotationType.setObjectName("groupBoxRotationType")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxRotationType)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioRotateCenter = QtWidgets.QRadioButton(parent=self.groupBoxRotationType)
        self.radioRotateCenter.setChecked(True)
        self.radioRotateCenter.setObjectName("radioRotateCenter")
        self.verticalLayout_3.addWidget(self.radioRotateCenter)
        self.radioRotateOrigin = QtWidgets.QRadioButton(parent=self.groupBoxRotationType)
        self.radioRotateOrigin.setObjectName("radioRotateOrigin")
        self.verticalLayout_3.addWidget(self.radioRotateOrigin)
        self.radioRotatePoint = QtWidgets.QRadioButton(parent=self.groupBoxRotationType)
        self.radioRotatePoint.setObjectName("radioRotatePoint")
        self.verticalLayout_3.addWidget(self.radioRotatePoint)
        self.verticalLayout_5.addWidget(self.groupBoxRotationType)
        self.groupBoxRotationAngle = QtWidgets.QGroupBox(parent=self.tab_rotate)
        self.groupBoxRotationAngle.setObjectName("groupBoxRotationAngle")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxRotationAngle)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_rotationDegrees = QtWidgets.QLabel(parent=self.groupBoxRotationAngle)
        self.label_rotationDegrees.setObjectName("label_rotationDegrees")
        self.horizontalLayout_3.addWidget(self.label_rotationDegrees)
        self.inputRotationAngle = QtWidgets.QLineEdit(parent=self.groupBoxRotationAngle)
        self.inputRotationAngle.setObjectName("inputRotationAngle")
        self.horizontalLayout_3.addWidget(self.inputRotationAngle)
        self.verticalLayout_5.addWidget(self.groupBoxRotationAngle)
        self.groupBoxRotationPoint = QtWidgets.QGroupBox(parent=self.tab_rotate)
        self.groupBoxRotationPoint.setEnabled(False)
        self.groupBoxRotationPoint.setObjectName("groupBoxRotationPoint")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBoxRotationPoint)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_PointX = QtWidgets.QLabel(parent=self.groupBoxRotationPoint)
        self.label_PointX.setObjectName("label_PointX")
        self.horizontalLayout_4.addWidget(self.label_PointX)
        self.inputRotationPointX = QtWidgets.QLineEdit(parent=self.groupBoxRotationPoint)
        self.inputRotationPointX.setObjectName("inputRotationPointX")
        self.horizontalLayout_4.addWidget(self.inputRotationPointX)
        self.label_PointY = QtWidgets.QLabel(parent=self.groupBoxRotationPoint)
        self.label_PointY.setObjectName("label_PointY")
        self.horizontalLayout_4.addWidget(self.label_PointY)
        self.inputRotationPointY = QtWidgets.QLineEdit(parent=self.groupBoxRotationPoint)
        self.inputRotationPointY.setObjectName("inputRotationPointY")
        self.horizontalLayout_4.addWidget(self.inputRotationPointY)
        self.verticalLayout_5.addWidget(self.groupBoxRotationPoint)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.tabWidgetTransformations.addTab(self.tab_rotate, "")
        self.horizontalLayout.addWidget(self.tabWidgetTransformations)
        self.groupBox_TransformationList = QtWidgets.QGroupBox(parent=TransformDialog)
        self.groupBox_TransformationList.setObjectName("groupBox_TransformationList")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_TransformationList)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonTransformationAdd = QtWidgets.QPushButton(parent=self.groupBox_TransformationList)
        self.buttonTransformationAdd.setObjectName("buttonTransformationAdd")
        self.horizontalLayout_2.addWidget(self.buttonTransformationAdd)
        self.buttonTransformationRemove = QtWidgets.QPushButton(parent=self.groupBox_TransformationList)
        self.buttonTransformationRemove.setObjectName("buttonTransformationRemove")
        self.horizontalLayout_2.addWidget(self.buttonTransformationRemove)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.listTransformations = QtWidgets.QListWidget(parent=self.groupBox_TransformationList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTransformations.sizePolicy().hasHeightForWidth())
        self.listTransformations.setSizePolicy(sizePolicy)
        self.listTransformations.setMinimumSize(QtCore.QSize(200, 0))
        self.listTransformations.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listTransformations.setObjectName("listTransformations")
        self.verticalLayout_2.addWidget(self.listTransformations)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addWidget(self.groupBox_TransformationList)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=TransformDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TransformDialog)
        self.tabWidgetTransformations.setCurrentIndex(0)
        self.buttonBox.accepted.connect(TransformDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(TransformDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TransformDialog)

    def retranslateUi(self, TransformDialog):
        _translate = QtCore.QCoreApplication.translate
        TransformDialog.setWindowTitle(_translate("TransformDialog", "Transform"))
        self.groupBoxTranslate.setTitle(_translate("TransformDialog", "Translate amount"))
        self.label_Dx.setText(_translate("TransformDialog", "DX:"))
        self.inputTranslateDx.setPlaceholderText(_translate("TransformDialog", "0"))
        self.label_Dy.setText(_translate("TransformDialog", "DY:"))
        self.inputTranslateDy.setPlaceholderText(_translate("TransformDialog", "0"))
        self.tabWidgetTransformations.setTabText(self.tabWidgetTransformations.indexOf(self.tab_translate), _translate("TransformDialog", "Translate"))
        self.groupBoxScale.setTitle(_translate("TransformDialog", "Scale amount"))
        self.label_scaleSx.setText(_translate("TransformDialog", "SX:"))
        self.inputScaleSx.setPlaceholderText(_translate("TransformDialog", "0"))
        self.checkBoxScaleAspect.setToolTip(_translate("TransformDialog", "Keep aspect"))
        self.label_scaleSy.setText(_translate("TransformDialog", "SY:"))
        self.inputScaleSy.setPlaceholderText(_translate("TransformDialog", "0"))
        self.tabWidgetTransformations.setTabText(self.tabWidgetTransformations.indexOf(self.tab_scale), _translate("TransformDialog", "Scale"))
        self.groupBoxRotationType.setTitle(_translate("TransformDialog", "Rotation type"))
        self.radioRotateCenter.setText(_translate("TransformDialog", "Rotate around the object center"))
        self.radioRotateOrigin.setText(_translate("TransformDialog", "Rotate around origin"))
        self.radioRotatePoint.setText(_translate("TransformDialog", "Rotate around a defined point"))
        self.groupBoxRotationAngle.setTitle(_translate("TransformDialog", "Rotation angle"))
        self.label_rotationDegrees.setText(_translate("TransformDialog", "Degrees:"))
        self.inputRotationAngle.setPlaceholderText(_translate("TransformDialog", "0"))
        self.groupBoxRotationPoint.setTitle(_translate("TransformDialog", "Rotation point"))
        self.label_PointX.setText(_translate("TransformDialog", "X:"))
        self.inputRotationPointX.setPlaceholderText(_translate("TransformDialog", "0"))
        self.label_PointY.setText(_translate("TransformDialog", "Y:"))
        self.inputRotationPointY.setPlaceholderText(_translate("TransformDialog", "0"))
        self.tabWidgetTransformations.setTabText(self.tabWidgetTransformations.indexOf(self.tab_rotate), _translate("TransformDialog", "Rotate"))
        self.groupBox_TransformationList.setTitle(_translate("TransformDialog", "Transformations"))
        self.buttonTransformationAdd.setText(_translate("TransformDialog", "Add"))
        self.buttonTransformationRemove.setText(_translate("TransformDialog", "Remove"))
