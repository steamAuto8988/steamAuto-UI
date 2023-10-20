import threading
import time

from PyQt5.QtCore import QThread, pyqtSignal

from app.config.config import TradeOfferState
from app.error.error import InvalidCredentials
from app.steam.TradeOffer import OffersResponse
from app.steam.trade import getTradeOffers


class TradeHandlerThread(QThread):
    _finished = pyqtSignal(OffersResponse)

    def __init__(self, steamDatas: list):
        super().__init__()
        self.steamDatas = steamDatas

    def run(self) -> None:
        self._getTradeOffer()

    def _getTradeOffer(self):
        while True:
            for steamData in self.steamDatas:
                if steamData.status is False:
                    continue
                if steamData.apiKey == None or steamData.apiKey == '':
                    steamData.getApiKey()
                print(f'账号：{steamData.account} steamApiKey：{steamData.apiKey}')
                if steamData.apiKey is not None:
                    try:
                        respJson = getTradeOffers(steamData.apiKey)
                        activeNum = 0
                        if respJson['response']:
                            if respJson['response'].get("trade_offers_sent"):
                                for offer in respJson['response']['trade_offers_sent']:
                                    if offer['trade_offer_state'] == TradeOfferState.Active:
                                        activeNum += 1
                            if respJson['response'].get("trade_offers_received"):
                                for offer in respJson['response']['trade_offers_received']:
                                    if offer['trade_offer_state'] == TradeOfferState.Active:
                                        activeNum += 1
                        offerResp = OffersResponse(steamData.index, steamData.steamId, activeNum)
                        # 通知UI线程
                        self._finished.emit(offerResp)
                    except InvalidCredentials as e:
                        print(f'steam:{steamData.account} apiKey失效，重新获取！')
                        steamData.getApiKey()
                        print(e)
                    except ConnectionError as e:
                        pass
                    time.sleep(10)

            time.sleep(10)
