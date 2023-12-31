# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from qfluentwidgets import ComboBox, SearchLineEdit, TableWidget


# self implementation generated from reading ui file '.\saleRecord.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


class SaleRecordInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.TableWidget = TableWidget(self)
        self.pltComboBox = ComboBox(self)
        self.searchItem = ComboBox(self)
        self.SearchLineEdit = SearchLineEdit(self)
        self.setupUi()

        self._loadSaveRecord()

    def setupUi(self):
        self.TableWidget.setGeometry(QtCore.QRect(20, 110, 1091, 701))
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setColumnCount(6)
        self.TableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setColumnWidth(2, 250)
        self.TableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setColumnWidth(3, 250)
        self.TableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setColumnWidth(4, 200)
        self.TableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableWidget.setColumnWidth(5, 180)
        self.TableWidget.setHorizontalHeaderItem(5, item)
        self.TableWidget.setEnabled(True)
        self.TableWidget.setWordWrap(False)
        self.TableWidget.verticalHeader().hide()

        self.SearchLineEdit.setGeometry(QtCore.QRect(450, 28, 361, 33))
        self.SearchLineEdit.setObjectName("SearchLineEdit")

        self.pltComboBox.setGeometry(QtCore.QRect(10, 20, 181, 41))
        self.pltComboBox.setObjectName("pltComboBox")

        self.searchItem.setGeometry(QtCore.QRect(260, 20, 181, 41))
        self.searchItem.setObjectName("searchItem")
        self.retranslateUi()

        # 事件绑定处理
        self.pltComboBox.currentTextChanged.connect(self._loadSaveRecord)
        self.SearchLineEdit.textChanged.connect(self._loadSaveRecord)
        self.searchItem.currentTextChanged.connect(self._loadSaveRecord)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        item = self.TableWidget.horizontalHeaderItem(0)
        item.setText(_translate("self", "#"))
        item = self.TableWidget.horizontalHeaderItem(1)
        item.setText(_translate("self", "发货平台"))
        item = self.TableWidget.horizontalHeaderItem(2)
        item.setText(_translate("self", "发货账号"))
        item = self.TableWidget.horizontalHeaderItem(3)
        item.setText(_translate("self", "收货账号"))
        item = self.TableWidget.horizontalHeaderItem(4)
        item.setText(_translate("self", "报价ID"))
        item = self.TableWidget.horizontalHeaderItem(5)
        item.setText(_translate("self", "确认报价时间"))

        self.pltComboBox.addItem(text='全部平台')
        self.pltComboBox.addItem(text='BUFF')
        self.pltComboBox.addItem(text="UU")

        self.searchItem.addItem(text='发货账号')
        self.searchItem.addItem(text='收货账号')
        self.searchItem.addItem(text='报价ID')

    def _loadSaveRecord(self):
        pltComboBoxText = self.pltComboBox.text()
        searchItemText = self.searchItem.text()
        SearchLineEditText = self.SearchLineEdit.text()

        i = 0
        with open(os.getcwd() + '\\saleRecord.txt', 'r') as f:
            lines = f.readlines()
            self.TableWidget.clearContents()
            self.TableWidget.setRowCount(0)
            for line in lines:
                sp = line.split('----')
                if sp.__len__() != 5:
                    continue
                if pltComboBoxText != '全部平台' and pltComboBoxText != sp[2]:
                    continue

                saleAccount = sp[0]
                buyAccount = sp[1]
                tradeOfferId = sp[3]
                if SearchLineEditText != '' or SearchLineEditText is not None:

                    #         self.searchItem.addItem(text='发货账号')
                    #         self.searchItem.addItem(text='收货账号')
                    #         self.searchItem.addItem(text='报价ID')
                    if searchItemText == '发货账号' and SearchLineEditText not in saleAccount:
                        continue
                    if searchItemText == '收货账号' and SearchLineEditText not in buyAccount:
                        continue
                    if searchItemText == '报价ID' and SearchLineEditText not in tradeOfferId:
                        continue

                print(f'遍历：{line}')
                self.TableWidget.setRowCount(i + 1)
                # 不要了原生序号，太丑了，自己弄一个
                tItem = QTableWidgetItem(str(i + 1))
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 0, tItem)

                # 平台
                tItem = QTableWidgetItem(sp[2])
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 1, tItem)

                # 发货账号
                tItem = QTableWidgetItem(saleAccount)
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 2, tItem)

                # 收货账号
                tItem = QTableWidgetItem(buyAccount)
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 3, tItem)

                # 报价id
                tItem = QTableWidgetItem(tradeOfferId)
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 4, tItem)

                # 报价id
                tItem = QTableWidgetItem(sp[4])
                tItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, 5, tItem)
                i += 1
