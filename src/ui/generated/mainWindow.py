# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 654)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.controlsSide = QtWidgets.QVBoxLayout()
        self.controlsSide.setObjectName("controlsSide")
        self.objectsGroupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.objectsGroupBox.setMaximumSize(QtCore.QSize(230, 16777215))
        self.objectsGroupBox.setObjectName("objectsGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.objectsGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.objectsList = QtWidgets.QListWidget(parent=self.objectsGroupBox)
        self.objectsList.setObjectName("objectsList")
        self.horizontalLayout_2.addWidget(self.objectsList)
        self.controlsSide.addWidget(self.objectsGroupBox)
        self.windowGroupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.windowGroupBox.sizePolicy().hasHeightForWidth())
        self.windowGroupBox.setSizePolicy(sizePolicy)
        self.windowGroupBox.setMaximumSize(QtCore.QSize(230, 16777215))
        self.windowGroupBox.setObjectName("windowGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.windowGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.movementGroupBox = QtWidgets.QGroupBox(parent=self.windowGroupBox)
        self.movementGroupBox.setMinimumSize(QtCore.QSize(0, 150))
        self.movementGroupBox.setObjectName("movementGroupBox")
        self.movementButtonDown = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonDown.setGeometry(QtCore.QRect(50, 110, 31, 31))
        self.movementButtonDown.setObjectName("movementButtonDown")
        self.movementButtonLeft = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonLeft.setGeometry(QtCore.QRect(20, 80, 31, 31))
        self.movementButtonLeft.setObjectName("movementButtonLeft")
        self.movementButtonRight = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonRight.setGeometry(QtCore.QRect(80, 80, 31, 31))
        self.movementButtonRight.setObjectName("movementButtonRight")
        self.movementButtonUp = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonUp.setGeometry(QtCore.QRect(50, 50, 31, 31))
        self.movementButtonUp.setObjectName("movementButtonUp")
        self.movementButtonZoomOut = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonZoomOut.setGeometry(QtCore.QRect(150, 110, 31, 31))
        self.movementButtonZoomOut.setObjectName("movementButtonZoomOut")
        self.movementButtonZoomIn = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonZoomIn.setGeometry(QtCore.QRect(150, 50, 31, 31))
        self.movementButtonZoomIn.setObjectName("movementButtonZoomIn")
        self.movementPositionLabel = QtWidgets.QLabel(parent=self.movementGroupBox)
        self.movementPositionLabel.setGeometry(QtCore.QRect(10, 30, 111, 18))
        self.movementPositionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movementPositionLabel.setObjectName("movementPositionLabel")
        self.movementZoomLabel = QtWidgets.QLabel(parent=self.movementGroupBox)
        self.movementZoomLabel.setGeometry(QtCore.QRect(130, 30, 71, 18))
        self.movementZoomLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movementZoomLabel.setObjectName("movementZoomLabel")
        self.verticalLayout_3.addWidget(self.movementGroupBox)
        self.rotationGroupBox = QtWidgets.QGroupBox(parent=self.windowGroupBox)
        self.rotationGroupBox.setEnabled(False)
        self.rotationGroupBox.setObjectName("rotationGroupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.rotationGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.rotationAngleConf = QtWidgets.QHBoxLayout()
        self.rotationAngleConf.setObjectName("rotationAngleConf")
        self.rotationAngleLabel = QtWidgets.QLabel(parent=self.rotationGroupBox)
        self.rotationAngleLabel.setObjectName("rotationAngleLabel")
        self.rotationAngleConf.addWidget(self.rotationAngleLabel)
        self.rotationAngleField = QtWidgets.QLineEdit(parent=self.rotationGroupBox)
        self.rotationAngleField.setObjectName("rotationAngleField")
        self.rotationAngleConf.addWidget(self.rotationAngleField)
        self.verticalLayout_5.addLayout(self.rotationAngleConf)
        self.rotationButtons = QtWidgets.QHBoxLayout()
        self.rotationButtons.setObjectName("rotationButtons")
        self.rotationButtonX = QtWidgets.QPushButton(parent=self.rotationGroupBox)
        self.rotationButtonX.setObjectName("rotationButtonX")
        self.rotationButtons.addWidget(self.rotationButtonX)
        self.rotationButtonY = QtWidgets.QPushButton(parent=self.rotationGroupBox)
        self.rotationButtonY.setObjectName("rotationButtonY")
        self.rotationButtons.addWidget(self.rotationButtonY)
        self.rotationButtonZ = QtWidgets.QPushButton(parent=self.rotationGroupBox)
        self.rotationButtonZ.setObjectName("rotationButtonZ")
        self.rotationButtons.addWidget(self.rotationButtonZ)
        self.verticalLayout_5.addLayout(self.rotationButtons)
        self.verticalLayout_3.addWidget(self.rotationGroupBox)
        self.projectionGroupBox = QtWidgets.QGroupBox(parent=self.windowGroupBox)
        self.projectionGroupBox.setEnabled(False)
        self.projectionGroupBox.setObjectName("projectionGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.projectionGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.projectionRadioParallel = QtWidgets.QRadioButton(parent=self.projectionGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectionRadioParallel.sizePolicy().hasHeightForWidth())
        self.projectionRadioParallel.setSizePolicy(sizePolicy)
        self.projectionRadioParallel.setMaximumSize(QtCore.QSize(16777215, 15))
        self.projectionRadioParallel.setObjectName("projectionRadioParallel")
        self.verticalLayout_4.addWidget(self.projectionRadioParallel)
        self.projectionRadioPerspective = QtWidgets.QRadioButton(parent=self.projectionGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectionRadioPerspective.sizePolicy().hasHeightForWidth())
        self.projectionRadioPerspective.setSizePolicy(sizePolicy)
        self.projectionRadioPerspective.setMaximumSize(QtCore.QSize(16777215, 15))
        self.projectionRadioPerspective.setObjectName("projectionRadioPerspective")
        self.verticalLayout_4.addWidget(self.projectionRadioPerspective)
        self.verticalLayout_3.addWidget(self.projectionGroupBox)
        self.controlsSide.addWidget(self.windowGroupBox)
        self.horizontalLayout.addLayout(self.controlsSide)
        self.mainSide = QtWidgets.QVBoxLayout()
        self.mainSide.setObjectName("mainSide")
        self.viewportBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.viewportBox.setMinimumSize(QtCore.QSize(400, 0))
        self.viewportBox.setObjectName("viewportBox")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.viewportBox)
        self.graphicsView.setGeometry(QtCore.QRect(10, 30, 441, 441))
        self.graphicsView.setAutoFillBackground(True)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setObjectName("graphicsView")
        self.mainSide.addWidget(self.viewportBox)
        self.logsScrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.logsScrollArea.setMaximumSize(QtCore.QSize(16777215, 100))
        self.logsScrollArea.setWidgetResizable(True)
        self.logsScrollArea.setObjectName("logsScrollArea")
        self.logsArea = QtWidgets.QWidget()
        self.logsArea.setGeometry(QtCore.QRect(0, 0, 540, 98))
        self.logsArea.setObjectName("logsArea")
        self.logsScrollArea.setWidget(self.logsArea)
        self.mainSide.addWidget(self.logsScrollArea)
        self.horizontalLayout.addLayout(self.mainSide)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuObjects = QtWidgets.QMenu(parent=self.menubar)
        self.menuObjects.setObjectName("menuObjects")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(parent=self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Object = QtGui.QAction(parent=MainWindow)
        self.actionAdd_Object.setObjectName("actionAdd_Object")
        self.actionQuit = QtGui.QAction(parent=MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuObjects.addAction(self.actionAdd_Object)
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuObjects.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bländär"))
        self.objectsGroupBox.setTitle(_translate("MainWindow", "Objects"))
        self.windowGroupBox.setTitle(_translate("MainWindow", "Window"))
        self.movementGroupBox.setTitle(_translate("MainWindow", "Movement"))
        self.movementButtonDown.setText(_translate("MainWindow", "⯆"))
        self.movementButtonLeft.setText(_translate("MainWindow", "⯇"))
        self.movementButtonRight.setText(_translate("MainWindow", "⯈"))
        self.movementButtonUp.setText(_translate("MainWindow", "⯅"))
        self.movementButtonZoomOut.setText(_translate("MainWindow", "-"))
        self.movementButtonZoomIn.setText(_translate("MainWindow", "+"))
        self.movementPositionLabel.setText(_translate("MainWindow", "Position"))
        self.movementZoomLabel.setText(_translate("MainWindow", "Zoom"))
        self.rotationGroupBox.setTitle(_translate("MainWindow", "Rotation"))
        self.rotationAngleLabel.setText(_translate("MainWindow", "Angle:"))
        self.rotationAngleField.setText(_translate("MainWindow", "15"))
        self.rotationButtonX.setText(_translate("MainWindow", "X"))
        self.rotationButtonY.setText(_translate("MainWindow", "Y"))
        self.rotationButtonZ.setText(_translate("MainWindow", "Z"))
        self.projectionGroupBox.setTitle(_translate("MainWindow", "Projection"))
        self.projectionRadioParallel.setText(_translate("MainWindow", "Parallel"))
        self.projectionRadioPerspective.setText(_translate("MainWindow", "Perspective"))
        self.viewportBox.setTitle(_translate("MainWindow", "Viewport"))
        self.menuObjects.setTitle(_translate("MainWindow", "Edit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionAdd_Object.setText(_translate("MainWindow", "Add Object..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
