# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SteamDataInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1134, 826)
        self.StaemInfoTableWidget = TableWidget(Form)
        self.StaemInfoTableWidget.setGeometry(QtCore.QRect(10, 60, 1011, 761))
        self.StaemInfoTableWidget.setObjectName("StaemInfoTableWidget")
        self.StaemInfoTableWidget.setColumnCount(8)
        self.StaemInfoTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 0, 0))
        self.StaemInfoTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.StaemInfoTableWidget.setHorizontalHeaderItem(7, item)
        self.addSteamInfoButton = PushButton(Form)
        self.addSteamInfoButton.setGeometry(QtCore.QRect(30, 10, 101, 41))
        self.addSteamInfoButton.setObjectName("addSteamInfoButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "#"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "账号"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "密码"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "令牌"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "STEAM ID"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "当前报价个数"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "BUFF状态"))
        item = self.StaemInfoTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "UU状态"))
        self.addSteamInfoButton.setText(_translate("Form", "添加新账号"))
from qfluentwidgets import PushButton, TableWidget