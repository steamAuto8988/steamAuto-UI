# -*- coding: utf-8 -*-
import json
import os.path

import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QMenu, QFileDialog
from qfluentwidgets import TableWidget, IndeterminateProgressRing, InfoBar, \
    InfoBarPosition, MessageBoxBase, SubtitleLabel, LineEdit, PushButton

from app.config.config import set_global_value
from app.config.utils import getIniValue, setIniValue
from app.steam.Session import SteamSession
from app.thread.GuardUpdateThread import GuardUpdateThread
from app.thread.buff import BuffThread, BuffOrderSignal, SignalLevel


# Form implementation generated from reading ui file 'SteamDataInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


class SteamDataInterface(QWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)

        self.steamDatas = []

        self.spinner = IndeterminateProgressRing(self)

        self.vBoxLayout.addWidget(self.spinner, 0, Qt.AlignHCenter)

        self._initTableUi()
        self.updateGuardCodeThread = GuardUpdateThread(self.steamDatas)
        self.BuffThread = BuffThread()
        # self.tradeHandlerThread = TradeHandlerThread(self.steamDatas)
        # 加载数据到UI，开一个线程，不然主界面会卡顿

        self._loadSteam()

    def _initTableUi(self):
        self.SteamInfoTableWidget = TableWidget()
        # 设置行不可编辑
        self.SteamInfoTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.SteamInfoTableWidget.setGeometry(QtCore.QRect(10, 60, 1101, 761))
        self.SteamInfoTableWidget.setObjectName("SteamInfoTableWidget")
        self.SteamInfoTableWidget.setColumnCount(8)
        self.SteamInfoTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 0, 0))
        self.SteamInfoTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.SteamInfoTableWidget.setHorizontalHeaderItem(7, item)
        self.SteamInfoTableWidget.setWordWrap(False)
        self.SteamInfoTableWidget.verticalHeader().hide()
        self.SteamInfoTableWidget.itemClicked.connect(self.__clickItem)

        # 表格添加右键菜单
        self.SteamInfoTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.SteamInfoTableWidget.customContextMenuRequested.connect(self.tableWidgetMenu)

        self.addSteamInfoButton = PushButton(self)
        self.addSteamInfoButton.setGeometry(QtCore.QRect(30, 20, 101, 41))
        self.addSteamInfoButton.setObjectName("addSteamInfoButton")
        self.addSteamInfoButton.clicked.connect(self._addSteamInfoButtonClick)

        self.translateUi()
        self.vBoxLayout.addWidget(self.SteamInfoTableWidget)

    def tableWidgetMenu(self, pos):
        row = self.SteamInfoTableWidget.rowAt(pos.y())
        col = self.SteamInfoTableWidget.rowAt(pos.x())
        print(f'row:{row},col:{col}')
        menu = QMenu()
        addBuffCookies = menu.addAction("导入BUFF COOKIES")
        addUUCookies = menu.addAction("导入UU COOKIES")
        action = menu.exec_(self.SteamInfoTableWidget.mapToGlobal(pos))
        steamdata = self.steamDatas[row]
        if action == addBuffCookies:
            print('点击添加buff cookie')
            w = saveCookie(plt='BUFF', steamData=steamdata, parent=self)
            w.exec_()
        elif action == addUUCookies:
            print('点击添加uu cookie')
            w = saveCookie(plt='UU', steamData=steamdata, parent=self)
            w.exec_()
        else:
            return

    def translateUi(self):
        _translate = QtCore.QCoreApplication.translate
        item = self.SteamInfoTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "#"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(1)
        self.SteamInfoTableWidget.setColumnWidth(1, 200)
        item.setText(_translate("Form", "账号"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "状态"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(3)
        self.SteamInfoTableWidget.setColumnWidth(3, 180)
        item.setText(_translate("Form", "令牌"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(4)
        self.SteamInfoTableWidget.setColumnWidth(4, 200)
        item.setText(_translate("Form", "STEAM ID"))

        item = self.SteamInfoTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "当前报价个数"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "BUFF状态"))
        item = self.SteamInfoTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "UU状态"))

        self.addSteamInfoButton.setText('导入')

    def _loadSteam(self):
        fileDis = os.getcwd() + '\\mafiles'
        if os.path.exists(fileDis):
            for rs, ds, fs in os.walk(fileDis):
                if len(fs) > 0:
                    for f in fs:
                        with open(f'{fileDis}' + '\\' + f, 'r') as read:
                            content = read.read()
                            if content:
                                jsonData = json.loads(content)
                                sessionData = jsonData.get('Session')
                                if sessionData:
                                    data = {
                                        'account_name': jsonData['account_name'],
                                        'steam_id': jsonData['Session']['SteamID'],
                                        'access_token': sessionData.get('AccessToken'),
                                        'refresh_token': sessionData.get('RefreshToken'),
                                        'shared_secret': jsonData['shared_secret'],
                                        'identity_secret': jsonData['identity_secret'],
                                    }
                                    data['apiKey'] = getIniValue(key='apiKey', section=str(data['steam_id']),
                                                                 default=None)
                                    steamSession = SteamSession(data, jsonData, fileDis + '\\' + f)
                                    self.steamDatas.append(steamSession)
                                    InfoBar.success(
                                        title='加载steam',
                                        content=f"账号{jsonData['account_name']}导入成功！",
                                        orient=Qt.Horizontal,
                                        isClosable=True,
                                        position=InfoBarPosition.TOP_RIGHT,
                                        # position='Custom',   # NOTE: use custom info bar manager
                                        duration=1500,
                                        parent=self
                                    )
                                else:
                                    InfoBar.warning(
                                        title='加载steam',
                                        content=f"账号{jsonData['account_name']}请在最新版SDA中登录后重新导出MAFILE文件！",
                                        orient=Qt.Horizontal,
                                        isClosable=True,
                                        position=InfoBarPosition.TOP_RIGHT,
                                        # position='Custom',   # NOTE: use custom info bar manager
                                        duration=3000,
                                        parent=self
                                    )
                else:
                    InfoBar.warning(
                        title='加载steam',
                        content="未找到可导入数据，请手动导入Steam mafile",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        # position='Custom',   # NOTE: use custom info bar manager
                        duration=3000,
                        parent=self
                    )
        else:
            os.mkdir(fileDis)
            InfoBar.error(
                title='加载steam',
                content="请导入steam mafile文件",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                # position='Custom',   # NOTE: use custom info bar manager
                duration=3000,
                parent=self
            )
        self.SteamInfoTableWidget.setRowCount(len(self.steamDatas))
        # 更新UI
        for i, item in enumerate(self.steamDatas):
            # 不要了原生序号，太丑了，自己弄一个
            item.index = i
            tItem = QTableWidgetItem(str(i + 1))
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 0, tItem)
            # 显示账号
            tItem = QTableWidgetItem(item.account)
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 1, tItem)
            # 不显示密码了
            statusMsg = '异常'
            if item.status:
                statusMsg = '正常'
            tItem = QTableWidgetItem(statusMsg)
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 2, tItem)
            # 令牌默认空，让子线程去刷新
            tItem = QTableWidgetItem('321')
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 3, tItem)
            # 显示steamId
            tItem = QTableWidgetItem(str(item.steamId))
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 4, tItem)

            # 报价个数
            tItem = QTableWidgetItem('0')
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 5, tItem)

            # BUFFCookies
            cookie = getIniValue(key='buff', section=str(item.steamId), default='')
            value = '已导入'
            if cookie == '':
                value = 'BUFF未导入'
            tItem = QTableWidgetItem(value)
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 6, tItem)

            # UUCookies
            # BUFFCookies
            cookie = getIniValue(key='uu', section=str(item.steamId), default='')
            value = '已导入'
            if cookie == '':
                value = 'UU未导入'
            tItem = QTableWidgetItem(value)
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(i, 7, tItem)

        # 关闭loading
        self.spinner.stop()
        if len(self.steamDatas) > 0:
            # 更新令牌 槽函数链接，收到信号调用方法
            self.updateGuardCodeThread._finished.connect(self._updateGuardCode)
            self.updateGuardCodeThread.start()

            self.BuffThread.start()
            self.BuffThread._finished.connect(self.BuffThreadSignal)
            self.BuffThread._buff_cook_finished.connect(self._buff_cook_finished_error)
            # 更新报价列表
            # self.tradeHandlerThread._finished.connect(self._updateOffreReps)
            # self.tradeHandlerThread.start()

        set_global_value('steamDatas', self.steamDatas)

    def _buff_cook_finished_error(self, account):
        items = self.SteamInfoTableWidget.findItems(account, Qt.MatchExactly)
        if items.__len__() > 0:
            row = items[0].row()
            tItem = QTableWidgetItem('cookie失效')
            tItem.setTextAlignment(Qt.AlignCenter)
            self.SteamInfoTableWidget.setItem(row, 6, tItem)

    def BuffThreadSignal(self, info: BuffOrderSignal):
        print(f'收到信号{info.msg}')
        if info.level == SignalLevel.success:
            InfoBar.success(
                title=info.title,
                content=info.msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                # position='Custom',   # NOTE: use custom info bar manager
                duration=10000,
                parent=self
            )
        if info.level == SignalLevel.error:
            InfoBar.error(
                title=info.title,
                content=info.msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                # position='Custom',   # NOTE: use custom info bar manager
                duration=10000,
                parent=self
            )

    def __clickItem(self, item):

        if item is not None:
            print(item.row())
            if item.column() == 3:
                tmp = self.SteamInfoTableWidget.item(item.row(), 1)
                pyperclip.copy(item.text())
                InfoBar.success(
                    title='复制令牌',
                    content=f"账号：{tmp.text()} 复制令牌成功",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    # position='Custom',   # NOTE: use custom info bar manager
                    duration=1000,
                    parent=self
                )

    def _updateGuardCode(self, steamData):
        item = self.SteamInfoTableWidget.item(steamData.index, 3)
        item.setText(steamData.guardCode)

    def _updateOffreReps(self, offerResp):
        item = self.SteamInfoTableWidget.item(offerResp.index, 5)
        item.setText(str(offerResp.activeNum))

    def _addSteamInfoButtonClick(self):
        fileDialog = QFileDialog(self)
        fileDialog.setDirectory(os.getcwd())
        fileDialog.setNameFilter('*.mafile')
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_path = fileDialog.exec_()
        if file_path and fileDialog.selectedFiles():
            for selectFile in fileDialog.selectedFiles():
                split = selectFile.split('/')
                fileName = split[len(split) - 1]
                if os.path.exists(os.getcwd() + '\\mafiles\\' + fileName):
                    InfoBar.warning(
                        title=f'导入steam',
                        content=f'{fileName} 已存在，无需再次导入',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        # position='Custom',   # NOTE: use custom info bar manager
                        duration=3000,
                        parent=self.parent()
                    )
                    continue
                with open(selectFile, 'r') as f:
                    with open(os.getcwd() + '\\mafiles\\' + fileName, 'w+') as newF:
                        newF.write(f.read())
                        newF.flush()

                InfoBar.success(
                    title=f'导入steam',
                    content=f'{fileName} 导入成功！',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    # position='Custom',   # NOTE: use custom info bar manager
                    duration=3000,
                    parent=self.parent()
                )


class saveCookie(MessageBoxBase):
    def __init__(self, plt: str, steamData: SteamSession, parent=None):
        super().__init__(parent)

        self.plt = plt
        self.steamData = steamData

        self.titleLabel = SubtitleLabel(f'STEAM:{self.steamData.account}-{self.plt} Cookies', self)
        self.cookieEdit = LineEdit(self)

        self.cookieEdit.setPlaceholderText(f'请输入:{self.plt} cookies')
        self.cookieEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.cookieEdit)

        # change the text of button
        self.yesButton.setText('保存')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.yesButton.clicked.connect(self._clickYesButton)
        self.cookieEdit.textChanged.connect(self._textChanged)

    # self.hideYesButton()

    def _clickYesButton(self):
        setIniValue(key=self.plt, section=str(self.steamData.steamId), value=str(self.cookieEdit.text()))
        InfoBar.success(
            title=f'{self.plt} Cookies 保存成功',
            content=f'STEAM:{self.steamData.account}-{self.plt} Cookies 保存成功!',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=3000,
            parent=self.parent()
        )

    def _textChanged(self, text):
        if len(text) > 0:
            self.yesButton.setDisabled(False)
        else:
            self.yesButton.setDisabled(True)

    @property
    def getLoadSteamInfo(self):
        return self.steamData
