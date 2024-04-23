# Form implementation generated from reading ui file 'ui/createObject.ui'
#
# Created by: PyQt6 UI code generator 6.7.0.dev2404081550
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CreateObjectDialog(object):
    def setupUi(self, CreateObjectDialog):
        CreateObjectDialog.setObjectName("CreateObjectDialog")
        CreateObjectDialog.resize(467, 242)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateObjectDialog.sizePolicy().hasHeightForWidth())
        CreateObjectDialog.setSizePolicy(sizePolicy)
        CreateObjectDialog.setMinimumSize(QtCore.QSize(200, 242))
        CreateObjectDialog.setMaximumSize(QtCore.QSize(16777215, 242))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CreateObjectDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_name = QtWidgets.QLabel(parent=CreateObjectDialog)
        self.label_name.setObjectName("label_name")
        self.verticalLayout_2.addWidget(self.label_name)
        self.inputName = QtWidgets.QLineEdit(parent=CreateObjectDialog)
        self.inputName.setObjectName("inputName")
        self.verticalLayout_2.addWidget(self.inputName)
        self.label_coords = QtWidgets.QLabel(parent=CreateObjectDialog)
        self.label_coords.setObjectName("label_coords")
        self.verticalLayout_2.addWidget(self.label_coords)
        self.inputCoordinates = QtWidgets.QLineEdit(parent=CreateObjectDialog)
        self.inputCoordinates.setObjectName("inputCoordinates")
        self.verticalLayout_2.addWidget(self.inputCoordinates)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkboxPolygon = QtWidgets.QCheckBox(parent=CreateObjectDialog)
        self.checkboxPolygon.setEnabled(False)
        self.checkboxPolygon.setObjectName("checkboxPolygon")
        self.horizontalLayout_4.addWidget(self.checkboxPolygon)
        self.checkBoxBezier = QtWidgets.QCheckBox(parent=CreateObjectDialog)
        self.checkBoxBezier.setEnabled(False)
        self.checkBoxBezier.setObjectName("checkBoxBezier")
        self.horizontalLayout_4.addWidget(self.checkBoxBezier)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.label_colour = QtWidgets.QLabel(parent=CreateObjectDialog)
        self.label_colour.setObjectName("label_colour")
        self.verticalLayout_2.addWidget(self.label_colour)
        self.inputColour = QtWidgets.QLineEdit(parent=CreateObjectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputColour.sizePolicy().hasHeightForWidth())
        self.inputColour.setSizePolicy(sizePolicy)
        self.inputColour.setMinimumSize(QtCore.QSize(0, 0))
        self.inputColour.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.inputColour.setInputMask("")
        self.inputColour.setMaxLength(7)
        self.inputColour.setObjectName("inputColour")
        self.verticalLayout_2.addWidget(self.inputColour)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=CreateObjectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(CreateObjectDialog)
        self.buttonBox.accepted.connect(CreateObjectDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(CreateObjectDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CreateObjectDialog)

    def retranslateUi(self, CreateObjectDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateObjectDialog.setWindowTitle(_translate("CreateObjectDialog", "Create Object"))
        self.label_name.setText(_translate("CreateObjectDialog", "Name"))
        self.label_coords.setText(_translate("CreateObjectDialog", "Coordinates"))
        self.inputCoordinates.setPlaceholderText(_translate("CreateObjectDialog", "(x1,y1),(x2,y2),..."))
        self.checkboxPolygon.setText(_translate("CreateObjectDialog", "Fill Polygon"))
        self.checkBoxBezier.setText(_translate("CreateObjectDialog", "Bézier Curve"))
        self.label_colour.setText(_translate("CreateObjectDialog", "Colour"))
        self.inputColour.setPlaceholderText(_translate("CreateObjectDialog", "#000000"))
