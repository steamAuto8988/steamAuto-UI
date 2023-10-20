import enum
from distutils.util import strtobool

from app.config.utils import getIniValue


class TradeOfferState(enum.IntEnum):
    Invalid = 1
    Active = 2
    Accepted = 3
    Countered = 4
    Expired = 5
    Canceled = 6
    Declined = 7
    InvalidItems = 8
    ConfirmationNeed = 9
    CanceledBySecondaryFactor = 10
    StateInEscrow = 11


class SteamUrl:
    API_URL = "https://api.steampowered.com"
    COMMUNITY_URL = "https://steamcommunity.com"
    STORE_URL = 'https://store.steampowered.com'


class Endpoints:
    CHAT_LOGIN = SteamUrl.API_URL + "/ISteamWebUserPresenceOAuth/Logon/v1"
    SEND_MESSAGE = SteamUrl.API_URL + "/ISteamWebUserPresenceOAuth/Message/v1"
    CHAT_LOGOUT = SteamUrl.API_URL + "/ISteamWebUserPresenceOAuth/Logoff/v1"
    CHAT_POLL = SteamUrl.API_URL + "/ISteamWebUserPresenceOAuth/Poll/v1"


class Proxy(object):
    def __init__(self, prot: str, address: str, useProxy: bool):
        self.port = prot
        self.address = address
        self.useProxy = useProxy

    def __dict__(self):
        if useproxy:
            return {
                'https': f'http://{self.address}:{self.port}'
            }
        else:
            return None


GameInfo = {
    '730': 'CSGO',
    "540": 'DOTA'
}





def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_global_value(key, value):
    """ 定义一个全局变量 """

    _global_dict[key] = value


def get_global_value(key, defValue=None):
    # """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except:
        _global_dict[key] = defValue


_init()
port = getIniValue(key='proxyport', section='proxyConfig', default='')
address = getIniValue(key='proxyaddress', section='proxyConfig', default='')
useproxy = getIniValue(key='useproxy', section='proxyConfig', default='False')
ProxyConfig = Proxy(prot=port, address=address, useProxy=bool(strtobool(useproxy)))
