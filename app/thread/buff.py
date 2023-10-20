import enum
import time
from distutils.util import strtobool

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from app.config.config import get_global_value, ProxyConfig, TradeOfferState
from app.config.utils import text_between, getIniValue, setIniValue, writeSaleRecord
from app.error.error import InvalidCredentials
from app.steam.apiEndpoints import TRADE_OFFER_URL, TRADE_OFFER_URL_REFERER
from app.steam.trade import get_trade_offer, confirmationTradeOffer

BASE_API = "https://buff.163.com"


class SignalLevel(enum.IntEnum):
    error = 1
    success = 2
    info = 3


class BuffOrderSignal(object):

    def __init__(self, level: SignalLevel, title: str, msg: str, data):
        self.level = level
        self.title = title
        self.msg = msg
        self.data = data


class BuffThread(QThread):
    _finished = pyqtSignal(BuffOrderSignal)
    _buff_cook_finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.loadSteamDatas = None

    def run(self) -> None:
        while True:
            self.loadSteamDatas = get_global_value('steamDatas')
            for steamData in self.loadSteamDatas:
                if steamData.status is False:
                    continue
                buffCookie = getIniValue(key='buff', section=str(steamData.steamId), default='')
                if buffCookie is None or buffCookie == '':
                    time.sleep(0.1)
                    continue
                # 检查配置，是否需要进行处理
                buff_auto_send = strtobool(
                    getIniValue(key='buff_auto_send', section='tradeOffer', default='False'))
                if not buff_auto_send:
                    time.sleep(1)
                    continue

                buff_auto_verify = strtobool(
                    getIniValue(key='buff_auto_verify', section='tradeOffer', default='False'))
                if not buff_auto_verify:
                    time.sleep(1)
                    continue

                if not buff_auto_verify and not buff_auto_send:
                    continue

                apikey = getIniValue(key='apikey', section=str(steamData.steamId), default='')
                if apikey is None or apikey == '':
                    apikey = steamData.getApiKey()
                    if apikey is None:
                        orderSignal = BuffOrderSignal(level=SignalLevel.success, title='BUFF报价',
                                                      msg=f'steam:{steamData.account}获取apikey失败！', data=None)
                        self._finished.emit(orderSignal)
                        setIniValue(key='buff', section=str(self.steamId), value='')
                    time.sleep(0.1)
                    continue

                if self.checkBuffCookie(steamData, buffCookie) is False:
                    time.sleep(0.1)
                    continue
                print(f'开始处理steam：{steamData.account}的BUFF发货报价')
                try:
                    if buff_auto_verify:
                        self._handlerAcceptTradOffer(cookie=buffCookie, steamData=steamData, apikey=apikey)
                    if buff_auto_send:
                        self._handlerSendTradOffer(cookie=buffCookie, steamData=steamData, apikey=apikey)
                except Exception as e:
                    print(e)
                time.sleep(10)
            time.sleep(10)

    def _handlerSendTradOffer(self, cookie: str, steamData, apikey: str):
        pass

    def _handlerAcceptTradOffer(self, cookie: str, steamData, apikey: str):
        buff_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
            "Cookie": cookie
        }
        respJson = requests.get(url=BASE_API + '/api/market/steam_trade', headers=buff_headers, timeout=10).json()

        try:
            if respJson['code'] == 'OK':
                for item in respJson['data']:
                    bot_name = item['bot_name']
                    tradeofferid = item['tradeofferid']
                    print(f'对方账号：{bot_name},报价id:{tradeofferid}')
                    self._acceptTraderOff(tradeofferid=tradeofferid, steamData=steamData, apikey=apikey,
                                          bot_name=bot_name)
        except Exception as e:
            print(f'确认buff报价出现异常：{e}')

    def _acceptTraderOff(self, tradeofferid, steamData, apikey: str, bot_name: str):

        # 检查一遍，当前报价是不是需要确认了

        try:

            respJson = get_trade_offer(tradeofferid=tradeofferid, apikey=apikey)
            if respJson['response']['offer']['trade_offer_state'] != TradeOfferState.Active:
                return
            item_count = len(respJson['response']['offer']['items_to_give'])
            orderSignal = BuffOrderSignal(level=SignalLevel.success, title='BUFF报价',
                                          msg=f'找到待确认{steamData.account} - BUFF 报价成功,报价id：{tradeofferid}，饰品个数：{item_count}',
                                          data=None)
            self._finished.emit(orderSignal)

            if respJson['response']['offer']['trade_offer_state'] == TradeOfferState.ConfirmationNeed:
                respJson = confirmationTradeOffer(trade_offer_id=tradeofferid, steamData=steamData)
                if respJson['success']:
                    writeSaleRecord(my_account=steamData.account, buy_account=bot_name, plt='BUFF',
                                    tradeId=str(tradeofferid),
                                    time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

                    orderSignal = BuffOrderSignal(level=SignalLevel.success, title='BUFF报价',
                                                  msg=f'确认{steamData.account} - BUFF报价成功,报价id：{tradeofferid}',
                                                  data=None)
                    self._finished.emit(orderSignal)
                return
        except Exception as e:
            if type(e) == InvalidCredentials:
                print('apiKey错误！')

        steamCookies = {
            'steamLoginSecure': steamData.steamLoginSecure,
            'sessionId': steamData.sessionId,
            'Steam_Language': 'english',
            'timezoneOffset': '28800,0',

        }
        steam_headers = {
            "Host": "steamcommunity.com",
            "Origin": "https://steamcommunity.com",
            "Referer": TRADE_OFFER_URL_REFERER.format(tradeofferid),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",

        }

        resp = requests.get(url=TRADE_OFFER_URL_REFERER.format(tradeofferid), cookies=steamCookies,
                            proxies=ProxyConfig.__dict__(), timeout=10,
                            headers=steam_headers)

        partner = text_between(resp.text, "var g_ulTradePartnerSteamID = '", "';")
        if partner is None or partner == "":
            return

        steam_data = {
            "captcha": "",
            "partner": partner,
            "tradeofferid": tradeofferid,
            "serverid": '1',
            "sessionid": steamData.sessionId,
        }
        steam_headers = {
            "Origin": "https://steamcommunity.com",
            "Referer": TRADE_OFFER_URL_REFERER.format(tradeofferid),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "Upgrade-Insecure-Requests": '1',
            "Cookie": "sessionid=" + steamData.sessionId + "; steamCountry=HK%7C7a2a75fe611572ce626bd90c554127a7;" +
                      ("timezoneOffset=28800,0; _ga=GA1.2.1788690905.1641353679; _gid=GA1.2.151171641.1641353679; "
                       "browserid=2418994576823700793; strInventoryLastContext=730_2; ") +
                      "steamLoginSecure=" + steamData.steamLoginSecure + ("; webTradeEligibility=%7B%22allowed%22%3A1"
                                                                          "%2C%22allowed_at_time") +
                      ("%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C"
                       "%22time_checked%22%3A") + str(int(time.time())) + "%7D"
        }
        # 读取一次这个steam交易界面，获取对方的steamid
        acceptJson = requests.post(url=TRADE_OFFER_URL.format(tradeofferid), data=steam_data, cookies=steamCookies,
                                   proxies=ProxyConfig.__dict__(), timeout=10,
                                   headers=steam_headers).json()
        if acceptJson['needs_mobile_confirmation']:
            respJson = confirmationTradeOffer(trade_offer_id=str(tradeofferid), steamData=steamData)
            if respJson['success']:
                writeSaleRecord(my_account=steamData.account, buy_account=bot_name, plt='BUFF',
                                tradeId=str(tradeofferid), time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                orderSignal = BuffOrderSignal(level=SignalLevel.success, title='BUFF报价',
                                              msg=f'确认{steamData.account} - BUFF报价成功,报价id：{tradeofferid}',
                                              data=None)
                self._finished.emit(orderSignal)
            print("确认steam报价返回：{}", respJson)

    def checkBuffCookie(self, steamData, cookie):
        buff_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
            "Cookie": cookie
        }
        try:
            respJson = requests.get(url=BASE_API + '/user-center/profile', timeout=10, headers=buff_headers)
            if "允许买家还价" in respJson.text:
                return True
            else:
                self._buff_cook_finished.emit(steamData.account)

                orderSignal = BuffOrderSignal(level=SignalLevel.error, title='BUFF报价',
                                              msg=f'steam:{steamData.account}关联的BUFFcookie失效！', data=None)
                self._finished.emit(orderSignal)
                return False
        except Exception as e:
            print('检查buff cookie网络异常')
            return True
