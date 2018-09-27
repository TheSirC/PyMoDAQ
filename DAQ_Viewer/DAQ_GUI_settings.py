# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DAQ_GUI_settings.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(451, 518)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.setObjectName("settings_layout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 3, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.do_bkg_cb = QtWidgets.QCheckBox(self.groupBox)
        self.do_bkg_cb.setObjectName("do_bkg_cb")
        self.horizontalLayout.addWidget(self.do_bkg_cb)
        self.take_bkg_cb = QtWidgets.QCheckBox(self.groupBox)
        self.take_bkg_cb.setObjectName("take_bkg_cb")
        self.horizontalLayout.addWidget(self.take_bkg_cb)
        self.gridLayout_3.addWidget(self.groupBox, 13, 0, 1, 2)
        self.title_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.gridLayout_3.addWidget(self.title_label, 0, 0, 1, 2)
        self.Ini_state_LED = QLED(Form)
        self.Ini_state_LED.setObjectName("Ini_state_LED")
        self.gridLayout_3.addWidget(self.Ini_state_LED, 5, 1, 3, 1)
        self.Quit_pb = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/close2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Quit_pb.setIcon(icon)
        self.Quit_pb.setObjectName("Quit_pb")
        self.gridLayout_3.addWidget(self.Quit_pb, 8, 0, 3, 2)
        self.IniDet_pb = QtWidgets.QPushButton(Form)
        self.IniDet_pb.setCheckable(True)
        self.IniDet_pb.setChecked(False)
        self.IniDet_pb.setObjectName("IniDet_pb")
        self.gridLayout_3.addWidget(self.IniDet_pb, 5, 0, 3, 1)
        self.Detector_type_combo = QtWidgets.QComboBox(Form)
        self.Detector_type_combo.setObjectName("Detector_type_combo")
        self.gridLayout_3.addWidget(self.Detector_type_combo, 2, 1, 3, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 17, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.grab_pb = QtWidgets.QPushButton(Form)
        self.grab_pb.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/run2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grab_pb.setIcon(icon1)
        self.grab_pb.setCheckable(True)
        self.grab_pb.setObjectName("grab_pb")
        self.horizontalLayout_2.addWidget(self.grab_pb)
        self.single_pb = QtWidgets.QPushButton(Form)
        self.single_pb.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/snap.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.single_pb.setIcon(icon2)
        self.single_pb.setCheckable(False)
        self.single_pb.setObjectName("single_pb")
        self.horizontalLayout_2.addWidget(self.single_pb)
        self.stop_pb = QtWidgets.QPushButton(Form)
        self.stop_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_pb.setIcon(icon3)
        self.stop_pb.setCheckable(False)
        self.stop_pb.setObjectName("stop_pb")
        self.horizontalLayout_2.addWidget(self.stop_pb)
        self.save_current_pb = QtWidgets.QPushButton(Form)
        self.save_current_pb.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/SaveAs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_current_pb.setIcon(icon4)
        self.save_current_pb.setObjectName("save_current_pb")
        self.horizontalLayout_2.addWidget(self.save_current_pb)
        self.save_new_pb = QtWidgets.QPushButton(Form)
        self.save_new_pb.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/Snap&Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_new_pb.setIcon(icon5)
        self.save_new_pb.setObjectName("save_new_pb")
        self.horizontalLayout_2.addWidget(self.save_new_pb)
        self.load_data_pb = QtWidgets.QPushButton(Form)
        self.load_data_pb.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_data_pb.setIcon(icon6)
        self.load_data_pb.setObjectName("load_data_pb")
        self.horizontalLayout_2.addWidget(self.load_data_pb)
        self.settings_pb = QtWidgets.QPushButton(Form)
        self.settings_pb.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/HLM.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_pb.setIcon(icon7)
        self.settings_pb.setCheckable(True)
        self.settings_pb.setObjectName("settings_pb")
        self.horizontalLayout_2.addWidget(self.settings_pb)
        self.update_com_pb = QtWidgets.QPushButton(Form)
        self.update_com_pb.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/Refresh2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_com_pb.setIcon(icon8)
        self.update_com_pb.setCheckable(False)
        self.update_com_pb.setObjectName("update_com_pb")
        self.horizontalLayout_2.addWidget(self.update_com_pb)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 11, 0, 2, 2)
        self.save_settings_pb = QtWidgets.QPushButton(Form)
        self.save_settings_pb.setIcon(icon4)
        self.save_settings_pb.setObjectName("save_settings_pb")
        self.gridLayout_3.addWidget(self.save_settings_pb, 14, 1, 3, 1)
        self.load_settings_pb = QtWidgets.QPushButton(Form)
        self.load_settings_pb.setIcon(icon6)
        self.load_settings_pb.setObjectName("load_settings_pb")
        self.gridLayout_3.addWidget(self.load_settings_pb, 14, 0, 3, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.DAQ_type_combo = QtWidgets.QComboBox(Form)
        self.DAQ_type_combo.setObjectName("DAQ_type_combo")
        self.DAQ_type_combo.addItem("")
        self.DAQ_type_combo.addItem("")
        self.DAQ_type_combo.addItem("")
        self.gridLayout_3.addWidget(self.DAQ_type_combo, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.settings_layout.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.settings_layout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Detector:"))
        self.do_bkg_cb.setText(_translate("Form", "Do Bkg sub."))
        self.take_bkg_cb.setText(_translate("Form", "Take Bkg"))
        self.title_label.setText(_translate("Form", "DAQ Title"))
        self.Ini_state_LED.setText(_translate("Form", "TextLabel"))
        self.Quit_pb.setText(_translate("Form", "Quit"))
        self.IniDet_pb.setText(_translate("Form", "Ini. Det."))
        self.Detector_type_combo.setToolTip(_translate("Form", "Stage Type"))
        self.grab_pb.setToolTip(_translate("Form", "Grab"))
        self.single_pb.setToolTip(_translate("Form", "Single Grab"))
        self.stop_pb.setToolTip(_translate("Form", "Single Grab"))
        self.save_current_pb.setToolTip(_translate("Form", "Save Current Data"))
        self.save_new_pb.setToolTip(_translate("Form", "Save New Data"))
        self.settings_pb.setToolTip(_translate("Form", "Open Settings"))
        self.update_com_pb.setToolTip(_translate("Form", "Refresh Hardware"))
        self.save_settings_pb.setText(_translate("Form", "Sett."))
        self.load_settings_pb.setText(_translate("Form", "Sett."))
        self.label_4.setText(_translate("Form", "DAQ type:"))
        self.DAQ_type_combo.setToolTip(_translate("Form", "Stage Type"))
        self.DAQ_type_combo.setItemText(0, _translate("Form", "DAQ0D"))
        self.DAQ_type_combo.setItemText(1, _translate("Form", "DAQ1D"))
        self.DAQ_type_combo.setItemText(2, _translate("Form", "DAQ2D"))

from PyMoDAQ import QLED
import QtDesigner_ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

