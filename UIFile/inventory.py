# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\inventory.ui'
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
        self.TableWidget = TableWidget(Form)
        self.TableWidget.setEnabled(True)
        self.TableWidget.setGeometry(QtCore.QRect(0, 70, 1121, 741))
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setColumnCount(5)
        self.TableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(4, item)
        self.canTradecheckBox = CheckBox(Form)
        self.canTradecheckBox.setGeometry(QtCore.QRect(470, 20, 141, 41))
        self.canTradecheckBox.setObjectName("canTradecheckBox")
        self.changeSteamComboBox = ComboBox(Form)
        self.changeSteamComboBox.setGeometry(QtCore.QRect(230, 20, 211, 32))
        self.changeSteamComboBox.setText("")
        self.changeSteamComboBox.setObjectName("changeSteamComboBox")
        self.changeGameCombo = ComboBox(Form)
        self.changeGameCombo.setGeometry(QtCore.QRect(20, 20, 181, 32))
        self.changeGameCombo.setText("")
        self.changeGameCombo.setObjectName("changeGameCombo")
        self.searchProductLineEdit = SearchLineEdit(Form)
        self.searchProductLineEdit.setGeometry(QtCore.QRect(610, 20, 431, 33))
        self.searchProductLineEdit.setObjectName("searchProductLineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.TableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "#"))
        item = self.TableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "中文名"))
        item = self.TableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "英文名"))
        item = self.TableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "ASSET ID"))
        item = self.TableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "可交易"))
        self.canTradecheckBox.setText(_translate("Form", "只显示可交易"))
from qfluentwidgets import CheckBox, ComboBox, SearchLineEdit, TableWidget
