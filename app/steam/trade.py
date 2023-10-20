import requests

from app.config.config import SteamUrl, ProxyConfig
from app.error.error import InvalidCredentials
from app.steam.Session import SteamSession
from app.steam.confirmation import ConfirmationExecutor

"""
报价相关请求接口
"""


# 请求获取报价列表
def getTradeOffers(apiKey: str):
    params = {'key': apiKey,
              'get_sent_offers': 1,
              'get_received_offers': 1,
              'get_descriptions': 1,
              'language': 'english',
              'active_only': 1,
              'historical_only': 0,
              'time_historical_cutoff': ''}
    response = api_call('GET', 'IEconService', 'GetTradeOffers', 'v1', params).json()
    return response


def api_call(request_method: str, interface: str, api_method: str, version: str,
             params: dict = None) -> requests.Response:
    url = '/'.join([SteamUrl.API_URL, interface, api_method, version])
    if request_method == 'GET':
        response = requests.get(url, params=params, proxies=ProxyConfig.__dict__())
    else:
        response = requests.post(url, data=params, proxies=ProxyConfig.__dict__())
    if __is_invalid_api_key(response):
        raise InvalidCredentials('Invalid API key')
    return response


def get_trade_offer(tradeofferid, apikey):
    params = {'key': apikey,
              'tradeofferid': tradeofferid,
              'language': 'english'}
    return api_call('GET', 'IEconService', 'GetTradeOffer', 'v1', params).json()


def __is_invalid_api_key(response: requests.Response) -> bool:
    msg = 'Access is denied. Retrying will not help. Please verify your <pre>key=</pre> parameter'
    return msg in response.text


def confirmationTradeOffer(trade_offer_id, steamData: SteamSession):
    confirmation_executor = ConfirmationExecutor(steamData)
    return confirmation_executor.send_trade_allow_request(trade_offer_id)
