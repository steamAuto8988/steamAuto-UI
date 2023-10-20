import enum

import requests

from app.config.config import ProxyConfig
from app.steam.apiEndpoints import COMMUNITY_BASE, INVENTORY_BY_STEAM_ID


def getInventory(steamId, appId, lang):
    try:
        url = INVENTORY_BY_STEAM_ID.format(steamId, appId, lang)

        resp = requests.get(url=url, headers={'Referer': COMMUNITY_BASE},
                            proxies=ProxyConfig.__dict__(), timeout=10)
        return resp
    except Exception as e:
        print(e)
        return None


class Descriptions:
    def __init__(self, source: dict):
        self.appid = source['appid']
        self.classid = source['classid']
        self.instanceid = source['instanceid']
        self.market_name = source['market_name']
        self.market_hash_name = source['market_hash_name']
        if source['tradable'] == 1:
            self.canTrade = True
        else:
            self.canTrade = False



class Asset(object):
    def __init__(self, source: dict, descriptions):
        self.appid = source['appid']
        self.contextid = source['contextid']
        self.amount = source['amount']
        self.assetid = source['assetid']
        self.classid = source['classid']
        self.instanceid = source['instanceid']
        self.descriptions = descriptions

    def __str__(self) -> str:
        return super().__str__()


class InventoryCode(enum.IntEnum):
    success = 1
    notOpen = 2
    inventoryIsZero = 3
    toolManyRequest = 4
    retry = 5


class InventoryResp(object):
    def __init__(self, account: str, steamId: str, code: InventoryCode, assets: list):
        self.account = account
        self.steamId = steamId
        self.code = code
        self.assets = assets
