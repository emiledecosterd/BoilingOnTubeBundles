# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulationWindowGUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1142, 697)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -186, 451, 896))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.fluidTypeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.fluidTypeComboBox.setObjectName("fluidTypeComboBox")
        self.fluidTypeComboBox.addItem("")
        self.fluidTypeComboBox.addItem("")
        self.fluidTypeComboBox.addItem("")
        self.gridLayout_2.addWidget(self.fluidTypeComboBox, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        self.mfr_hLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mfr_hLineEdit.sizePolicy().hasHeightForWidth())
        self.mfr_hLineEdit.setSizePolicy(sizePolicy)
        self.mfr_hLineEdit.setObjectName("mfr_hLineEdit")
        self.gridLayout_2.addWidget(self.mfr_hLineEdit, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)
        self.mfr_cLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.mfr_cLineEdit.setText("")
        self.mfr_cLineEdit.setObjectName("mfr_cLineEdit")
        self.gridLayout_2.addWidget(self.mfr_cLineEdit, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 3, 1, 1, 1)
        self.tubeMatComboBox = QtWidgets.QComboBox(self.groupBox)
        self.tubeMatComboBox.setObjectName("tubeMatComboBox")
        self.tubeMatComboBox.addItem("")
        self.tubeMatComboBox.addItem("")
        self.tubeMatComboBox.addItem("")
        self.tubeMatComboBox.addItem("")
        self.gridLayout_2.addWidget(self.tubeMatComboBox, 3, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 3, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 4, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 4, 1, 1, 1)
        self.tubeThermalConductivityLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tubeThermalConductivityLineEdit.setText("")
        self.tubeThermalConductivityLineEdit.setObjectName("tubeThermalConductivityLineEdit")
        self.gridLayout_2.addWidget(self.tubeThermalConductivityLineEdit, 4, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 3, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 0, 1, 1, 1)
        self.DsLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.DsLineEdit.setObjectName("DsLineEdit")
        self.gridLayout_3.addWidget(self.DsLineEdit, 0, 2, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 4, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 1, 1, 1, 1)
        self.DLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.DLineEdit.setObjectName("DLineEdit")
        self.gridLayout_3.addWidget(self.DLineEdit, 1, 2, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 4, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(100, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem9, 2, 1, 1, 2)
        self.NtSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.NtSpinBox.setObjectName("NtSpinBox")
        self.gridLayout_3.addWidget(self.NtSpinBox, 2, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 2, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 3, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(100, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem11, 3, 1, 1, 2)
        self.Nt_colSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.Nt_colSpinBox.setObjectName("Nt_colSpinBox")
        self.gridLayout_3.addWidget(self.Nt_colSpinBox, 3, 3, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem12, 3, 4, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 4, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 4, 1, 1, 1)
        self.LLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.LLineEdit.setObjectName("LLineEdit")
        self.gridLayout_3.addWidget(self.LLineEdit, 4, 2, 1, 2)
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 4, 4, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_2)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 5, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 5, 1, 1, 1)
        self.sLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sLineEdit.setObjectName("sLineEdit")
        self.gridLayout_3.addWidget(self.sLineEdit, 5, 2, 1, 2)
        self.label_19 = QtWidgets.QLabel(self.groupBox_2)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 5, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_2)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 6, 0, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem15, 6, 1, 1, 1)
        self.shLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.shLineEdit.setText("")
        self.shLineEdit.setObjectName("shLineEdit")
        self.gridLayout_3.addWidget(self.shLineEdit, 6, 2, 1, 2)
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 6, 4, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox_2)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 7, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 7, 1, 1, 1)
        self.tLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.tLineEdit.setObjectName("tLineEdit")
        self.gridLayout_3.addWidget(self.tLineEdit, 7, 2, 1, 2)
        self.label_23 = QtWidgets.QLabel(self.groupBox_2)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 7, 4, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox_2)
        self.label_24.setObjectName("label_24")
        self.gridLayout_3.addWidget(self.label_24, 8, 0, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem17, 8, 1, 1, 1)
        self.layoutComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.layoutComboBox.setObjectName("layoutComboBox")
        self.layoutComboBox.addItem("")
        self.layoutComboBox.addItem("")
        self.gridLayout_3.addWidget(self.layoutComboBox, 8, 2, 1, 2)
        spacerItem18 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem18, 8, 4, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.groupBox_2)
        self.label_26.setObjectName("label_26")
        self.gridLayout_3.addWidget(self.label_26, 9, 0, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem19, 9, 1, 1, 1)
        self.e_iLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.e_iLineEdit.setText("")
        self.e_iLineEdit.setObjectName("e_iLineEdit")
        self.gridLayout_3.addWidget(self.e_iLineEdit, 9, 2, 1, 2)
        self.label_25 = QtWidgets.QLabel(self.groupBox_2)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 9, 4, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.groupBox_2)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 10, 0, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem20, 10, 1, 1, 1)
        self.e_oLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.e_oLineEdit.setObjectName("e_oLineEdit")
        self.gridLayout_3.addWidget(self.e_oLineEdit, 10, 2, 1, 2)
        self.label_27 = QtWidgets.QLabel(self.groupBox_2)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 10, 4, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.groupBox_2)
        self.label_29.setObjectName("label_29")
        self.gridLayout_3.addWidget(self.label_29, 11, 0, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem21, 11, 1, 1, 2)
        self.nSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.nSpinBox.setObjectName("nSpinBox")
        self.gridLayout_3.addWidget(self.nSpinBox, 11, 3, 1, 1)
        spacerItem22 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem22, 11, 4, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox_2)
        self.label_30.setObjectName("label_30")
        self.gridLayout_3.addWidget(self.label_30, 12, 0, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem23, 12, 1, 1, 1)
        self.corrComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.corrComboBox.setObjectName("corrComboBox")
        self.corrComboBox.addItem("")
        self.corrComboBox.addItem("")
        self.corrComboBox.addItem("")
        self.gridLayout_3.addWidget(self.corrComboBox, 12, 2, 1, 2)
        spacerItem24 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem24, 12, 4, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox_2)
        self.label_31.setObjectName("label_31")
        self.gridLayout_3.addWidget(self.label_31, 13, 0, 1, 1)
        spacerItem25 = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem25, 13, 1, 1, 1)
        self.corrPDComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.corrPDComboBox.setObjectName("corrPDComboBox")
        self.corrPDComboBox.addItem("")
        self.corrPDComboBox.addItem("")
        self.gridLayout_3.addWidget(self.corrPDComboBox, 13, 2, 1, 2)
        spacerItem26 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem26, 13, 4, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_33 = QtWidgets.QLabel(self.groupBox_3)
        self.label_33.setObjectName("label_33")
        self.gridLayout_4.addWidget(self.label_33, 0, 0, 1, 1)
        spacerItem27 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem27, 0, 1, 1, 2)
        self.xcLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.xcLineEdit.setObjectName("xcLineEdit")
        self.gridLayout_4.addWidget(self.xcLineEdit, 0, 3, 1, 1)
        spacerItem28 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem28, 0, 4, 1, 1)
        self.paramCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.paramCheckBox.setObjectName("paramCheckBox")
        self.gridLayout_4.addWidget(self.paramCheckBox, 1, 0, 1, 1)
        spacerItem29 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem29, 1, 1, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.groupBox_3)
        self.label_34.setObjectName("label_34")
        self.gridLayout_4.addWidget(self.label_34, 1, 2, 1, 1)
        self.paraSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.paraSpinBox.setObjectName("paraSpinBox")
        self.gridLayout_4.addWidget(self.paraSpinBox, 1, 3, 1, 1)
        spacerItem30 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem30, 1, 4, 1, 1)
        self.TcCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.TcCheckBox.setObjectName("TcCheckBox")
        self.gridLayout_4.addWidget(self.TcCheckBox, 2, 0, 1, 1)
        spacerItem31 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem31, 2, 1, 1, 1)
        self.TcStartLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.TcStartLineEdit.setObjectName("TcStartLineEdit")
        self.gridLayout_4.addWidget(self.TcStartLineEdit, 2, 2, 1, 1)
        self.TcEndLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.TcEndLineEdit.setObjectName("TcEndLineEdit")
        self.gridLayout_4.addWidget(self.TcEndLineEdit, 2, 3, 1, 1)
        spacerItem32 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem32, 2, 4, 1, 1)
        self.ThCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.ThCheckBox.setObjectName("ThCheckBox")
        self.gridLayout_4.addWidget(self.ThCheckBox, 3, 0, 1, 1)
        spacerItem33 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem33, 3, 1, 1, 1)
        self.ThStartLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.ThStartLineEdit.setObjectName("ThStartLineEdit")
        self.gridLayout_4.addWidget(self.ThStartLineEdit, 3, 2, 1, 1)
        self.ThEndLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.ThEndLineEdit.setObjectName("ThEndLineEdit")
        self.gridLayout_4.addWidget(self.ThEndLineEdit, 3, 3, 1, 1)
        spacerItem34 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem34, 3, 4, 1, 1)
        self.PhCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.PhCheckBox.setObjectName("PhCheckBox")
        self.gridLayout_4.addWidget(self.PhCheckBox, 4, 0, 1, 1)
        spacerItem35 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem35, 4, 1, 1, 1)
        self.PhStartLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.PhStartLineEdit.setObjectName("PhStartLineEdit")
        self.gridLayout_4.addWidget(self.PhStartLineEdit, 4, 2, 1, 1)
        self.PhEndLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.PhEndLineEdit.setObjectName("PhEndLineEdit")
        self.gridLayout_4.addWidget(self.PhEndLineEdit, 4, 3, 1, 1)
        spacerItem36 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem36, 4, 4, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 4, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.showPlotsButton = QtWidgets.QPushButton(self.centralwidget)
        self.showPlotsButton.setObjectName("showPlotsButton")
        self.horizontalLayout_2.addWidget(self.showPlotsButton)
        spacerItem37 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem37)
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_2.addWidget(self.label_32)
        self.chosenResultComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.chosenResultComboBox.setObjectName("chosenResultComboBox")
        self.chosenResultComboBox.addItem("")
        self.chosenResultComboBox.addItem("")
        self.chosenResultComboBox.addItem("")
        self.chosenResultComboBox.addItem("")
        self.chosenResultComboBox.addItem("")
        self.chosenResultComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.chosenResultComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.graphicsView = QClickableGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setObjectName("console")
        self.verticalLayout.addWidget(self.console)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 60)
        self.verticalLayout.setStretch(3, 10)
        self.gridLayout.addLayout(self.verticalLayout, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1142, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Operating conditions"))
        self.label_2.setText(_translate("MainWindow", "Working fluid"))
        self.fluidTypeComboBox.setItemText(0, _translate("MainWindow", "R134a"))
        self.fluidTypeComboBox.setItemText(1, _translate("MainWindow", "Propane"))
        self.fluidTypeComboBox.setItemText(2, _translate("MainWindow", "Ammonia"))
        self.label_4.setText(_translate("MainWindow", "Mass flow rate hot fluid"))
        self.label_5.setText(_translate("MainWindow", "[kg/s]"))
        self.label_6.setText(_translate("MainWindow", "Mass flow rate working fluid"))
        self.label_7.setText(_translate("MainWindow", "[kg/s]"))
        self.label_3.setText(_translate("MainWindow", "Tube material"))
        self.tubeMatComboBox.setItemText(0, _translate("MainWindow", "copper"))
        self.tubeMatComboBox.setItemText(1, _translate("MainWindow", "aluminium"))
        self.tubeMatComboBox.setItemText(2, _translate("MainWindow", "steel"))
        self.tubeMatComboBox.setItemText(3, _translate("MainWindow", "other"))
        self.label_8.setText(_translate("MainWindow", "Tube thermal conductivity"))
        self.label_9.setText(_translate("MainWindow", "[W/mK]"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Geometry"))
        self.label_10.setText(_translate("MainWindow", "Shell diameter"))
        self.label_12.setText(_translate("MainWindow", "[m]"))
        self.label_11.setText(_translate("MainWindow", "Tube diameter"))
        self.label_13.setText(_translate("MainWindow", "[m]"))
        self.label_14.setText(_translate("MainWindow", "Number of rows"))
        self.label_15.setText(_translate("MainWindow", "Number of columns"))
        self.label_16.setText(_translate("MainWindow", "Tube length"))
        self.label_17.setText(_translate("MainWindow", "[m]"))
        self.label_18.setText(_translate("MainWindow", "Vertical tube pitch"))
        self.label_19.setText(_translate("MainWindow", "[m]"))
        self.label_20.setText(_translate("MainWindow", "Horizontal tube pitch"))
        self.label_21.setText(_translate("MainWindow", "[m]"))
        self.label_22.setText(_translate("MainWindow", "Tube thickness"))
        self.label_23.setText(_translate("MainWindow", "[m]"))
        self.label_24.setText(_translate("MainWindow", "Layout"))
        self.layoutComboBox.setItemText(0, _translate("MainWindow", "Inline"))
        self.layoutComboBox.setItemText(1, _translate("MainWindow", "Staggered"))
        self.label_26.setText(_translate("MainWindow", "Inside tube rugosity"))
        self.label_25.setText(_translate("MainWindow", "[m]"))
        self.label_28.setText(_translate("MainWindow", "Outside tube rugosity"))
        self.label_27.setText(_translate("MainWindow", "[m]"))
        self.label_29.setText(_translate("MainWindow", "Number of cells "))
        self.label_30.setText(_translate("MainWindow", "Correlation for heat \n"
" transfer coefficient"))
        self.corrComboBox.setItemText(0, _translate("MainWindow", "Mostinski"))
        self.corrComboBox.setItemText(1, _translate("MainWindow", "Cooper"))
        self.corrComboBox.setItemText(2, _translate("MainWindow", "Gorenflo"))
        self.label_31.setText(_translate("MainWindow", "Correlation for\n"
" pressure drop"))
        self.corrPDComboBox.setItemText(0, _translate("MainWindow", "Gaddis"))
        self.corrPDComboBox.setItemText(1, _translate("MainWindow", "Zukauskas"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Flow inputs"))
        self.label_33.setText(_translate("MainWindow", "Working fluid \n"
"inlet vapor quality"))
        self.paramCheckBox.setText(_translate("MainWindow", "Parametrization"))
        self.label_34.setText(_translate("MainWindow", "# values"))
        self.TcCheckBox.setText(_translate("MainWindow", "Working fluid \n"
"inlet temperature"))
        self.ThCheckBox.setText(_translate("MainWindow", "Hot fluid \n"
"inlet temperature"))
        self.PhCheckBox.setText(_translate("MainWindow", "Hot fluid \n"
"inletpressure"))
        self.showPlotsButton.setText(_translate("MainWindow", "Show plots"))
        self.label_32.setText(_translate("MainWindow", "Field to display"))
        self.chosenResultComboBox.setItemText(0, _translate("MainWindow", "Hot fluid temperature"))
        self.chosenResultComboBox.setItemText(1, _translate("MainWindow", "Hot fluid pressure"))
        self.chosenResultComboBox.setItemText(2, _translate("MainWindow", "Working fluid temperature"))
        self.chosenResultComboBox.setItemText(3, _translate("MainWindow", "Working fluid pressure"))
        self.chosenResultComboBox.setItemText(4, _translate("MainWindow", "Working fluid vapor quality"))
        self.chosenResultComboBox.setItemText(5, _translate("MainWindow", "Working fluid void fraction"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.label.setText(_translate("MainWindow", "Boiling on tube bundles"))

from clickableGraphicsView import QClickableGraphicsView
