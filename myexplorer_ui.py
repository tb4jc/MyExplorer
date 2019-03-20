# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myexplorer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(849, 254)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myexplorer/resources/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFileCopy = QtWidgets.QWidget()
        self.tabFileCopy.setObjectName("tabFileCopy")
        self.gridLayout = QtWidgets.QGridLayout(self.tabFileCopy)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(1, 1))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.srcDirSel = QtWidgets.QPushButton(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srcDirSel.sizePolicy().hasHeightForWidth())
        self.srcDirSel.setSizePolicy(sizePolicy)
        self.srcDirSel.setMinimumSize(QtCore.QSize(1, 1))
        self.srcDirSel.setObjectName("srcDirSel")
        self.gridLayout.addWidget(self.srcDirSel, 1, 1, 1, 1)
        self.dstDir = QtWidgets.QLineEdit(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dstDir.sizePolicy().hasHeightForWidth())
        self.dstDir.setSizePolicy(sizePolicy)
        self.dstDir.setMinimumSize(QtCore.QSize(5, 1))
        self.dstDir.setObjectName("dstDir")
        self.gridLayout.addWidget(self.dstDir, 1, 0, 1, 1)
        self.yearOrdering = QtWidgets.QCheckBox(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yearOrdering.sizePolicy().hasHeightForWidth())
        self.yearOrdering.setSizePolicy(sizePolicy)
        self.yearOrdering.setMinimumSize(QtCore.QSize(1, 0))
        self.yearOrdering.setObjectName("yearOrdering")
        self.gridLayout.addWidget(self.yearOrdering, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(1, 1))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.srcDir = QtWidgets.QLineEdit(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srcDir.sizePolicy().hasHeightForWidth())
        self.srcDir.setSizePolicy(sizePolicy)
        self.srcDir.setMinimumSize(QtCore.QSize(5, 1))
        self.srcDir.setObjectName("srcDir")
        self.gridLayout.addWidget(self.srcDir, 3, 0, 1, 1)
        self.dstDirSel = QtWidgets.QPushButton(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dstDirSel.sizePolicy().hasHeightForWidth())
        self.dstDirSel.setSizePolicy(sizePolicy)
        self.dstDirSel.setMinimumSize(QtCore.QSize(1, 1))
        self.dstDirSel.setObjectName("dstDirSel")
        self.gridLayout.addWidget(self.dstDirSel, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tabFileCopy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(2, 1))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        self.tabWidget.addTab(self.tabFileCopy, "")
        self.tabSpare = QtWidgets.QWidget()
        self.tabSpare.setObjectName("tabSpare")
        self.tabWidget.addTab(self.tabSpare, "")
        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MyExplorer"))
        self.label_2.setText(_translate("mainWindow", "Destination Path"))
        self.srcDirSel.setText(_translate("mainWindow", "..."))
        self.yearOrdering.setText(_translate("mainWindow", "Year Ordering"))
        self.label.setText(_translate("mainWindow", "Source Path"))
        self.dstDirSel.setText(_translate("mainWindow", "..."))
        self.pushButton.setText(_translate("mainWindow", "Copy Files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFileCopy), _translate("mainWindow", "Copy Files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSpare), _translate("mainWindow", "Spare"))

# import myexplorer_rc
