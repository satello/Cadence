# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/scott/Python/Cadence/resources/widget/tools/GaitGeneratorWidget/GaitGeneratorWidget.ui'
#
# Created: Sun Nov 10 00:48:59 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PySideUiFileSetup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(795, 372)
        Form.setBaseSize(QtCore.QSize(580, 360))
        Form.verticalLayout = QtGui.QVBoxLayout(Form)
        Form.verticalLayout.setObjectName("verticalLayout")
        Form.widget = QtGui.QWidget(Form)
        Form.widget.setObjectName("widget")
        Form.verticalLayout_4 = QtGui.QVBoxLayout(Form.widget)
        Form.verticalLayout_4.setSpacing(0)
        Form.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_4.setObjectName("verticalLayout_4")
        Form.label_6 = QtGui.QLabel(Form.widget)
        Form.label_6.setObjectName("label_6")
        Form.verticalLayout_4.addWidget(Form.label_6)
        Form.horizontalLayout = QtGui.QHBoxLayout()
        Form.horizontalLayout.setSpacing(12)
        Form.horizontalLayout.setObjectName("horizontalLayout")
        Form.gadLengthSlider = QtGui.QSlider(Form.widget)
        Form.gadLengthSlider.setMinimum(50)
        Form.gadLengthSlider.setMaximum(1000)
        Form.gadLengthSlider.setSingleStep(10)
        Form.gadLengthSlider.setPageStep(50)
        Form.gadLengthSlider.setProperty("value", 100)
        Form.gadLengthSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.gadLengthSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.gadLengthSlider.setTickInterval(50)
        Form.gadLengthSlider.setObjectName("gadLengthSlider")
        Form.horizontalLayout.addWidget(Form.gadLengthSlider)
        Form.gadLengthLabel = QtGui.QLabel(Form.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.gadLengthLabel.sizePolicy().hasHeightForWidth())
        Form.gadLengthLabel.setSizePolicy(sizePolicy)
        Form.gadLengthLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.gadLengthLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.gadLengthLabel.setFont(font)
        Form.gadLengthLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.gadLengthLabel.setObjectName("gadLengthLabel")
        Form.horizontalLayout.addWidget(Form.gadLengthLabel)
        Form.verticalLayout_4.addLayout(Form.horizontalLayout)
        Form.verticalLayout.addWidget(Form.widget)
        Form.widget_2 = QtGui.QWidget(Form)
        Form.widget_2.setObjectName("widget_2")
        Form.verticalLayout_6 = QtGui.QVBoxLayout(Form.widget_2)
        Form.verticalLayout_6.setSpacing(0)
        Form.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_6.setObjectName("verticalLayout_6")
        Form.label_4 = QtGui.QLabel(Form.widget_2)
        Form.label_4.setObjectName("label_4")
        Form.verticalLayout_6.addWidget(Form.label_4)
        Form.horizontalLayout_3 = QtGui.QHBoxLayout()
        Form.horizontalLayout_3.setSpacing(12)
        Form.horizontalLayout_3.setObjectName("horizontalLayout_3")
        Form.stepLengthSlider = QtGui.QSlider(Form.widget_2)
        Form.stepLengthSlider.setMaximum(500)
        Form.stepLengthSlider.setSingleStep(10)
        Form.stepLengthSlider.setPageStep(50)
        Form.stepLengthSlider.setProperty("value", 50)
        Form.stepLengthSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.stepLengthSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.stepLengthSlider.setTickInterval(20)
        Form.stepLengthSlider.setObjectName("stepLengthSlider")
        Form.horizontalLayout_3.addWidget(Form.stepLengthSlider)
        Form.stepLengthLabel = QtGui.QLabel(Form.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.stepLengthLabel.sizePolicy().hasHeightForWidth())
        Form.stepLengthLabel.setSizePolicy(sizePolicy)
        Form.stepLengthLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.stepLengthLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.stepLengthLabel.setFont(font)
        Form.stepLengthLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.stepLengthLabel.setObjectName("stepLengthLabel")
        Form.horizontalLayout_3.addWidget(Form.stepLengthLabel)
        Form.verticalLayout_6.addLayout(Form.horizontalLayout_3)
        Form.verticalLayout.addWidget(Form.widget_2)
        Form.widget_3 = QtGui.QWidget(Form)
        Form.widget_3.setObjectName("widget_3")
        Form.verticalLayout_7 = QtGui.QVBoxLayout(Form.widget_3)
        Form.verticalLayout_7.setSpacing(0)
        Form.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_7.setObjectName("verticalLayout_7")
        Form.label = QtGui.QLabel(Form.widget_3)
        Form.label.setObjectName("label")
        Form.verticalLayout_7.addWidget(Form.label)
        Form.horizontalLayout_4 = QtGui.QHBoxLayout()
        Form.horizontalLayout_4.setSpacing(12)
        Form.horizontalLayout_4.setObjectName("horizontalLayout_4")
        Form.gaitPhaseSlider = QtGui.QSlider(Form.widget_3)
        Form.gaitPhaseSlider.setMinimum(0)
        Form.gaitPhaseSlider.setMaximum(99)
        Form.gaitPhaseSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.gaitPhaseSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.gaitPhaseSlider.setTickInterval(5)
        Form.gaitPhaseSlider.setObjectName("gaitPhaseSlider")
        Form.horizontalLayout_4.addWidget(Form.gaitPhaseSlider)
        Form.gaitPhaseLabel = QtGui.QLabel(Form.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.gaitPhaseLabel.sizePolicy().hasHeightForWidth())
        Form.gaitPhaseLabel.setSizePolicy(sizePolicy)
        Form.gaitPhaseLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.gaitPhaseLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.gaitPhaseLabel.setFont(font)
        Form.gaitPhaseLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.gaitPhaseLabel.setObjectName("gaitPhaseLabel")
        Form.horizontalLayout_4.addWidget(Form.gaitPhaseLabel)
        Form.verticalLayout_7.addLayout(Form.horizontalLayout_4)
        Form.verticalLayout.addWidget(Form.widget_3)
        Form.widget_4 = QtGui.QWidget(Form)
        Form.widget_4.setObjectName("widget_4")
        Form.verticalLayout_8 = QtGui.QVBoxLayout(Form.widget_4)
        Form.verticalLayout_8.setSpacing(0)
        Form.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_8.setObjectName("verticalLayout_8")
        Form.label_2 = QtGui.QLabel(Form.widget_4)
        Form.label_2.setObjectName("label_2")
        Form.verticalLayout_8.addWidget(Form.label_2)
        Form.horizontalLayout_5 = QtGui.QHBoxLayout()
        Form.horizontalLayout_5.setSpacing(12)
        Form.horizontalLayout_5.setObjectName("horizontalLayout_5")
        Form.dutyFactorHindSlider = QtGui.QSlider(Form.widget_4)
        Form.dutyFactorHindSlider.setMinimum(10)
        Form.dutyFactorHindSlider.setMaximum(90)
        Form.dutyFactorHindSlider.setProperty("value", 50)
        Form.dutyFactorHindSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.dutyFactorHindSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.dutyFactorHindSlider.setTickInterval(5)
        Form.dutyFactorHindSlider.setObjectName("dutyFactorHindSlider")
        Form.horizontalLayout_5.addWidget(Form.dutyFactorHindSlider)
        Form.dutyFactorHindLabel = QtGui.QLabel(Form.widget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.dutyFactorHindLabel.sizePolicy().hasHeightForWidth())
        Form.dutyFactorHindLabel.setSizePolicy(sizePolicy)
        Form.dutyFactorHindLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.dutyFactorHindLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.dutyFactorHindLabel.setFont(font)
        Form.dutyFactorHindLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.dutyFactorHindLabel.setObjectName("dutyFactorHindLabel")
        Form.horizontalLayout_5.addWidget(Form.dutyFactorHindLabel)
        Form.verticalLayout_8.addLayout(Form.horizontalLayout_5)
        Form.verticalLayout.addWidget(Form.widget_4)
        Form.widget_5 = QtGui.QWidget(Form)
        Form.widget_5.setObjectName("widget_5")
        Form.verticalLayout_9 = QtGui.QVBoxLayout(Form.widget_5)
        Form.verticalLayout_9.setSpacing(0)
        Form.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_9.setObjectName("verticalLayout_9")
        Form.label_3 = QtGui.QLabel(Form.widget_5)
        Form.label_3.setObjectName("label_3")
        Form.verticalLayout_9.addWidget(Form.label_3)
        Form.horizontalLayout_6 = QtGui.QHBoxLayout()
        Form.horizontalLayout_6.setSpacing(12)
        Form.horizontalLayout_6.setObjectName("horizontalLayout_6")
        Form.dutyFactorForeSlider = QtGui.QSlider(Form.widget_5)
        Form.dutyFactorForeSlider.setMinimum(10)
        Form.dutyFactorForeSlider.setMaximum(90)
        Form.dutyFactorForeSlider.setProperty("value", 50)
        Form.dutyFactorForeSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.dutyFactorForeSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.dutyFactorForeSlider.setTickInterval(5)
        Form.dutyFactorForeSlider.setObjectName("dutyFactorForeSlider")
        Form.horizontalLayout_6.addWidget(Form.dutyFactorForeSlider)
        Form.dutyFactorForeLabel = QtGui.QLabel(Form.widget_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.dutyFactorForeLabel.sizePolicy().hasHeightForWidth())
        Form.dutyFactorForeLabel.setSizePolicy(sizePolicy)
        Form.dutyFactorForeLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.dutyFactorForeLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.dutyFactorForeLabel.setFont(font)
        Form.dutyFactorForeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.dutyFactorForeLabel.setObjectName("dutyFactorForeLabel")
        Form.horizontalLayout_6.addWidget(Form.dutyFactorForeLabel)
        Form.verticalLayout_9.addLayout(Form.horizontalLayout_6)
        Form.verticalLayout.addWidget(Form.widget_5)
        Form.widget_6 = QtGui.QWidget(Form)
        Form.widget_6.setObjectName("widget_6")
        Form.verticalLayout_10 = QtGui.QVBoxLayout(Form.widget_6)
        Form.verticalLayout_10.setSpacing(0)
        Form.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_10.setObjectName("verticalLayout_10")
        Form.label_5 = QtGui.QLabel(Form.widget_6)
        Form.label_5.setObjectName("label_5")
        Form.verticalLayout_10.addWidget(Form.label_5)
        Form.horizontalLayout_7 = QtGui.QHBoxLayout()
        Form.horizontalLayout_7.setSpacing(12)
        Form.horizontalLayout_7.setObjectName("horizontalLayout_7")
        Form.cyclesSlider = QtGui.QSlider(Form.widget_6)
        Form.cyclesSlider.setMinimum(1)
        Form.cyclesSlider.setMaximum(50)
        Form.cyclesSlider.setProperty("value", 10)
        Form.cyclesSlider.setOrientation(QtCore.Qt.Horizontal)
        Form.cyclesSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        Form.cyclesSlider.setTickInterval(2)
        Form.cyclesSlider.setObjectName("cyclesSlider")
        Form.horizontalLayout_7.addWidget(Form.cyclesSlider)
        Form.cyclesLabel = QtGui.QLabel(Form.widget_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.cyclesLabel.sizePolicy().hasHeightForWidth())
        Form.cyclesLabel.setSizePolicy(sizePolicy)
        Form.cyclesLabel.setMinimumSize(QtCore.QSize(60, 0))
        Form.cyclesLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.cyclesLabel.setFont(font)
        Form.cyclesLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Form.cyclesLabel.setObjectName("cyclesLabel")
        Form.horizontalLayout_7.addWidget(Form.cyclesLabel)
        Form.verticalLayout_10.addLayout(Form.horizontalLayout_7)
        Form.verticalLayout.addWidget(Form.widget_6)
        Form.widget_7 = QtGui.QWidget(Form)
        Form.widget_7.setObjectName("widget_7")
        Form.horizontalLayout_8 = QtGui.QHBoxLayout(Form.widget_7)
        Form.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem = QtGui.QSpacerItem(675, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_8.addItem(spacerItem)
        Form.runButton = QtGui.QPushButton(Form.widget_7)
        Form.runButton.setObjectName("runButton")
        Form.horizontalLayout_8.addWidget(Form.runButton)
        Form.verticalLayout.addWidget(Form.widget_7)
        spacerItem1 = QtGui.QSpacerItem(20, 34, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(Form.stepLengthSlider, QtCore.SIGNAL("valueChanged(int)"), Form.stepLengthLabel.setNum)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Gait Generator And Visualizer", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_6.setText(QtGui.QApplication.translate("Form", "Gleno-Acetabular Length", None, QtGui.QApplication.UnicodeUTF8))
        Form.gadLengthLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_4.setText(QtGui.QApplication.translate("Form", "Step Length", None, QtGui.QApplication.UnicodeUTF8))
        Form.stepLengthLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.label.setText(QtGui.QApplication.translate("Form", "Gait Phase", None, QtGui.QApplication.UnicodeUTF8))
        Form.gaitPhaseLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_2.setText(QtGui.QApplication.translate("Form", "Duty Factor (Hind)", None, QtGui.QApplication.UnicodeUTF8))
        Form.dutyFactorHindLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_3.setText(QtGui.QApplication.translate("Form", "Duty Factor (Fore)", None, QtGui.QApplication.UnicodeUTF8))
        Form.dutyFactorForeLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_5.setText(QtGui.QApplication.translate("Form", "Cycles", None, QtGui.QApplication.UnicodeUTF8))
        Form.cyclesLabel.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        Form.runButton.setText(QtGui.QApplication.translate("Form", "Run", None, QtGui.QApplication.UnicodeUTF8))
