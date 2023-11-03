# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtractWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QtractWindow(object):
    def setupUi(self, QtractWindow):
        QtractWindow.setObjectName("QtractWindow")
        QtractWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(QtractWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_2.addWidget(self.line_5)
        self.select_image_location_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_image_location_button.sizePolicy().hasHeightForWidth())
        self.select_image_location_button.setSizePolicy(sizePolicy)
        self.select_image_location_button.setObjectName("select_image_location_button")
        self.verticalLayout_2.addWidget(self.select_image_location_button, 0, QtCore.Qt.AlignHCenter)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.ocr_image = OCRGraphicsView(self.centralwidget)
        self.ocr_image.setObjectName("ocr_image")
        self.verticalLayout_2.addWidget(self.ocr_image)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.extract_text_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extract_text_button.sizePolicy().hasHeightForWidth())
        self.extract_text_button.setSizePolicy(sizePolicy)
        self.extract_text_button.setObjectName("extract_text_button")
        self.verticalLayout_2.addWidget(self.extract_text_button, 0, QtCore.Qt.AlignHCenter)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.verticalLayout_2.setStretch(4, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.minimal_confidence = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.minimal_confidence.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.minimal_confidence.setMaximum(100.0)
        self.minimal_confidence.setProperty("value", 90.0)
        self.minimal_confidence.setObjectName("minimal_confidence")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.minimal_confidence)
        self.verticalLayout.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.clear_languages_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_languages_button.setObjectName("clear_languages_button")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.clear_languages_button)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(86, 86, 86))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 86, 86))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 109, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.language_list = TesseractLanguageList(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_list.sizePolicy().hasHeightForWidth())
        self.language_list.setSizePolicy(sizePolicy)
        self.language_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.language_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.language_list.setObjectName("language_list")
        self.ocr_text_preview = QtWidgets.QTextBrowser(self.splitter)
        self.ocr_text_preview.setObjectName("ocr_text_preview")
        self.verticalLayout.addWidget(self.splitter)
        self.save_selected_text_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_selected_text_button.setEnabled(False)
        self.save_selected_text_button.setObjectName("save_selected_text_button")
        self.verticalLayout.addWidget(self.save_selected_text_button, 0, QtCore.Qt.AlignHCenter)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout.addWidget(self.line_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        QtractWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QtractWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        QtractWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QtractWindow)
        self.statusbar.setObjectName("statusbar")
        QtractWindow.setStatusBar(self.statusbar)

        self.retranslateUi(QtractWindow)
        QtCore.QMetaObject.connectSlotsByName(QtractWindow)

    def retranslateUi(self, QtractWindow):
        _translate = QtCore.QCoreApplication.translate
        QtractWindow.setWindowTitle(_translate("QtractWindow", "Qtract"))
        self.select_image_location_button.setText(_translate("QtractWindow", "Select image location"))
        self.extract_text_button.setText(_translate("QtractWindow", "Extract text"))
        self.label.setText(_translate("QtractWindow", "Minimal confidence"))
        self.minimal_confidence.setSuffix(_translate("QtractWindow", "%"))
        self.label_2.setText(_translate("QtractWindow", "Languages in the image"))
        self.clear_languages_button.setText(_translate("QtractWindow", "clear"))
        self.label_3.setText(_translate("QtractWindow", "eng is selected by default if no language is specified"))
        self.ocr_text_preview.setPlaceholderText(_translate("QtractWindow", "The selected text can be previewed here"))
        self.save_selected_text_button.setText(_translate("QtractWindow", "Save selected text"))
from OCRGraphicsView import OCRGraphicsView
from TesseractLanguageList import TesseractLanguageList
