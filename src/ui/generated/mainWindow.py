# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt6 UI code generator 6.7.0.dev2404081550
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
        self.movementButtonDown.setGeometry(QtCore.QRect(90, 110, 31, 31))
        self.movementButtonDown.setObjectName("movementButtonDown")
        self.movementButtonLeft = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonLeft.setGeometry(QtCore.QRect(60, 80, 31, 31))
        self.movementButtonLeft.setObjectName("movementButtonLeft")
        self.movementButtonRight = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonRight.setGeometry(QtCore.QRect(120, 80, 31, 31))
        self.movementButtonRight.setObjectName("movementButtonRight")
        self.movementButtonUp = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonUp.setGeometry(QtCore.QRect(90, 50, 31, 31))
        self.movementButtonUp.setObjectName("movementButtonUp")
        self.movementButtonZoomOut = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonZoomOut.setGeometry(QtCore.QRect(160, 110, 31, 31))
        self.movementButtonZoomOut.setObjectName("movementButtonZoomOut")
        self.movementButtonZoomIn = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonZoomIn.setGeometry(QtCore.QRect(160, 50, 31, 31))
        self.movementButtonZoomIn.setObjectName("movementButtonZoomIn")
        self.movementPositionLabel = QtWidgets.QLabel(parent=self.movementGroupBox)
        self.movementPositionLabel.setGeometry(QtCore.QRect(90, 30, 31, 20))
        self.movementPositionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movementPositionLabel.setObjectName("movementPositionLabel")
        self.movementZoomLabel = QtWidgets.QLabel(parent=self.movementGroupBox)
        self.movementZoomLabel.setGeometry(QtCore.QRect(155, 30, 41, 20))
        self.movementZoomLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movementZoomLabel.setObjectName("movementZoomLabel")
        self.movementButtonRotateAntiClockwise = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonRotateAntiClockwise.setGeometry(QtCore.QRect(20, 110, 31, 31))
        self.movementButtonRotateAntiClockwise.setObjectName("movementButtonRotateAntiClockwise")
        self.movementRotateLabel = QtWidgets.QLabel(parent=self.movementGroupBox)
        self.movementRotateLabel.setGeometry(QtCore.QRect(10, 30, 51, 20))
        self.movementRotateLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movementRotateLabel.setObjectName("movementRotateLabel")
        self.movementButtonRotateClockwise = QtWidgets.QPushButton(parent=self.movementGroupBox)
        self.movementButtonRotateClockwise.setGeometry(QtCore.QRect(20, 50, 31, 31))
        self.movementButtonRotateClockwise.setObjectName("movementButtonRotateClockwise")
        self.rotationAngleField = QtWidgets.QLineEdit(parent=self.movementGroupBox)
        self.rotationAngleField.setGeometry(QtCore.QRect(20, 80, 31, 31))
        self.rotationAngleField.setObjectName("rotationAngleField")
        self.verticalLayout_3.addWidget(self.movementGroupBox)
        self.projectionGroupBox = QtWidgets.QGroupBox(parent=self.windowGroupBox)
        self.projectionGroupBox.setEnabled(True)
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
        self.projectionRadioParallel.setChecked(False)
        self.projectionRadioParallel.setObjectName("projectionRadioParallel")
        self.verticalLayout_4.addWidget(self.projectionRadioParallel)
        self.projectionRadioPerspective = QtWidgets.QRadioButton(parent=self.projectionGroupBox)
        self.projectionRadioPerspective.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectionRadioPerspective.sizePolicy().hasHeightForWidth())
        self.projectionRadioPerspective.setSizePolicy(sizePolicy)
        self.projectionRadioPerspective.setMaximumSize(QtCore.QSize(16777215, 15))
        self.projectionRadioPerspective.setChecked(True)
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
        self.viewportCanvas = QtWidgets.QLabel(parent=self.viewportBox)
        self.viewportCanvas.setGeometry(QtCore.QRect(10, 30, 441, 441))
        self.viewportCanvas.setStyleSheet("border: 1px solid #333;")
        self.viewportCanvas.setText("")
        self.viewportCanvas.setObjectName("viewportCanvas")
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
        self.menuTransform = QtWidgets.QMenu(parent=self.menuObjects)
        self.menuTransform.setObjectName("menuTransform")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuImport = QtWidgets.QMenu(parent=self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuExport = QtWidgets.QMenu(parent=self.menuFile)
        self.menuExport.setObjectName("menuExport")
        self.menuAbout = QtWidgets.QMenu(parent=self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuClipping = QtWidgets.QMenu(parent=self.menuView)
        self.menuClipping.setObjectName("menuClipping")
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
        self.actionTranslate = QtGui.QAction(parent=MainWindow)
        self.actionTranslate.setObjectName("actionTranslate")
        self.actionScale = QtGui.QAction(parent=MainWindow)
        self.actionScale.setObjectName("actionScale")
        self.actionRotate = QtGui.QAction(parent=MainWindow)
        self.actionRotate.setObjectName("actionRotate")
        self.actionWavefrontImport = QtGui.QAction(parent=MainWindow)
        self.actionWavefrontImport.setObjectName("actionWavefrontImport")
        self.actionWavefrontExport = QtGui.QAction(parent=MainWindow)
        self.actionWavefrontExport.setObjectName("actionWavefrontExport")
        self.actionLogs_Panel = QtGui.QAction(parent=MainWindow)
        self.actionLogs_Panel.setCheckable(True)
        self.actionLogs_Panel.setChecked(True)
        self.actionLogs_Panel.setObjectName("actionLogs_Panel")
        self.actionPoints = QtGui.QAction(parent=MainWindow)
        self.actionPoints.setCheckable(True)
        self.actionPoints.setObjectName("actionPoints")
        self.actionCohen_Sutherland = QtGui.QAction(parent=MainWindow)
        self.actionCohen_Sutherland.setCheckable(True)
        self.actionCohen_Sutherland.setObjectName("actionCohen_Sutherland")
        self.actionLiang_Barsky = QtGui.QAction(parent=MainWindow)
        self.actionLiang_Barsky.setCheckable(True)
        self.actionLiang_Barsky.setObjectName("actionLiang_Barsky")
        self.actionNicholl_Lee_Nicholl = QtGui.QAction(parent=MainWindow)
        self.actionNicholl_Lee_Nicholl.setCheckable(True)
        self.actionNicholl_Lee_Nicholl.setObjectName("actionNicholl_Lee_Nicholl")
        self.menuTransform.addAction(self.actionTranslate)
        self.menuTransform.addAction(self.actionScale)
        self.menuTransform.addAction(self.actionRotate)
        self.menuObjects.addAction(self.actionAdd_Object)
        self.menuObjects.addSeparator()
        self.menuObjects.addAction(self.menuTransform.menuAction())
        self.menuImport.addAction(self.actionWavefrontImport)
        self.menuExport.addAction(self.actionWavefrontExport)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuClipping.addAction(self.actionPoints)
        self.menuClipping.addAction(self.actionCohen_Sutherland)
        self.menuClipping.addAction(self.actionLiang_Barsky)
        self.menuClipping.addAction(self.actionNicholl_Lee_Nicholl)
        self.menuView.addAction(self.actionLogs_Panel)
        self.menuView.addAction(self.menuClipping.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuObjects.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
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
        self.movementPositionLabel.setText(_translate("MainWindow", "Move"))
        self.movementZoomLabel.setText(_translate("MainWindow", "Zoom"))
        self.movementButtonRotateAntiClockwise.setText(_translate("MainWindow", "↺"))
        self.movementRotateLabel.setText(_translate("MainWindow", "Rotate"))
        self.movementButtonRotateClockwise.setText(_translate("MainWindow", "↻"))
        self.rotationAngleField.setToolTip(_translate("MainWindow", "Rotation steps in degrees"))
        self.rotationAngleField.setText(_translate("MainWindow", "15"))
        self.projectionGroupBox.setTitle(_translate("MainWindow", "Projection"))
        self.projectionRadioParallel.setText(_translate("MainWindow", "Parallel"))
        self.projectionRadioPerspective.setText(_translate("MainWindow", "Perspective"))
        self.viewportBox.setTitle(_translate("MainWindow", "Viewport"))
        self.menuObjects.setTitle(_translate("MainWindow", "Edit"))
        self.menuTransform.setTitle(_translate("MainWindow", "Transform"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuClipping.setTitle(_translate("MainWindow", "Clipping"))
        self.actionAdd_Object.setText(_translate("MainWindow", "Add Object..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionTranslate.setText(_translate("MainWindow", "Translate"))
        self.actionScale.setText(_translate("MainWindow", "Scale"))
        self.actionRotate.setText(_translate("MainWindow", "Rotate"))
        self.actionWavefrontImport.setText(_translate("MainWindow", "Wavefront (.obj)"))
        self.actionWavefrontExport.setText(_translate("MainWindow", "Wavefront (.obj)"))
        self.actionLogs_Panel.setText(_translate("MainWindow", "Logs Panel"))
        self.actionPoints.setText(_translate("MainWindow", "Points"))
        self.actionCohen_Sutherland.setText(_translate("MainWindow", "Cohen-Sutherland"))
        self.actionLiang_Barsky.setText(_translate("MainWindow", "Liang-Barsky"))
        self.actionNicholl_Lee_Nicholl.setText(_translate("MainWindow", "Nicholl-Lee-Nicholl"))
