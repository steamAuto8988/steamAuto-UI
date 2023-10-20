import sys
import traceback

import pyperclip
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (FluentWindow, MessageBox, NavigationItemPosition)

from .SettingInterface import SettingInterface
from .inventory_interface import InventoryInterface
from .sale_record_interface import SaleRecordInterface
from .steam_info_interface import SteamDataInterface
from ..common.config import cfg


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface

        # crate listener

        self.rankInfo = {}
        self.games = {}
        # 创建子界面
        self.steamDataInterface = SteamDataInterface()
        self.settingInterface = SettingInterface()
        self.inventoryInterface = InventoryInterface()
        self.saleRecordInterface = SaleRecordInterface()

        self.__initInterface()
        self.__initNavigation()
        self.__initWindow()

    def __lockInterface(self):
        pass

    def __initNavigation(self):
        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(
            self.steamDataInterface, QIcon('./app/resource/images/steam.png'), 'STEAM账号', pos)
        self.addSubInterface(
            self.inventoryInterface, QIcon('./app/resource/images/inventory.png'), '库存查询', pos)

        self.addSubInterface(
            self.saleRecordInterface, QIcon('./app/resource/images/inventory.png'), '订单记录', pos)

        self.addSubInterface(
            self.settingInterface, QIcon('./app/resource/images/setting.png'), '设置', NavigationItemPosition.BOTTOM)
        self.navigationInterface.addSeparator()

    def __initInterface(self):
        self.__lockInterface()
        self.steamDataInterface.setObjectName('steamDataInterface')
        self.inventoryInterface.setObjectName('inventoryInterface')
        self.settingInterface.setObjectName('settingInterface')
        self.saleRecordInterface.setObjectName('saleRecordInterface')

    def __initWindow(self):
        self.resize(1134, 826)
        self.setMaximumSize(1134, 826)
        self.setMinimumSize(1134, 826)
        self.setWindowIcon(QIcon("app/resource/images/logo.png"))
        self.setWindowTitle("STEAM AUTO ✌")

        self.titleBar.titleLabel.setStyleSheet(
            "QLabel {font: 13px 'Segoe UI', 'Microsoft YaHei';}")
        self.titleBar.hBoxLayout.insertSpacing(0, 10)

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # self.splashScreen = SplashScreen(self.windowIcon(), self)
        # self.splashScreen.setIconSize(QSize(106, 106))
        # self.splashScreen.raise_()
        cfg.themeChanged.connect(
            lambda: self.setMicaEffectEnabled(self.isMicaEffectEnabled()))

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # self.show()
        # QApplication.processEvents()

        self.oldHook = sys.excepthook
        sys.excepthook = self.exceptHook

    def exceptHook(self, ty, value, tb):
        pass
        # tracebackFormat = traceback.format_exception(ty, value, tb)
        # title = self.tr('Exception occurred 😥')
        # content = "".join(tracebackFormat)
        #
        # w = MessageBox(title, content, self.window())
        #
        # w.yesButton.setText(self.tr('Copy to clipboard'))
        # w.cancelButton.setText(self.tr('Cancel'))
        #
        # if w.exec():
        #     pyperclip.copy(content)

        # self.oldHook(ty, value, tb)
