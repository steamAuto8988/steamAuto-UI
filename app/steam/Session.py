import base64
import json
import re
import secrets
import time

import requests
from requests.exceptions import ProxyError

from app.config.config import ProxyConfig
from app.config.utils import setIniValue
from app.steam.apiEndpoints import *


def _random_hex_number():
    buffer = secrets.token_bytes(16)
    hexStr = ''
    for e in buffer:
        hexStr += hex(e)
    return hexStr


def _generateSessionID():
    return _random_hex_number()


class SteamSession(object):
    """
    @:param data 程序需要的数据
    @:param originData 原始的文本数据 这里要保留
    """

    def __init__(self, data: dict, originData: json, filePath: str):
        self.apiKey = data['apiKey']
        self.index = None
        self.account = data['account_name']
        self.steamId = data['steam_id']
        self.accessToken = data['access_token']
        self.refreshToken = data['refresh_token']
        self.sharedSecret = data['shared_secret']
        self.identitySecret = data['identity_secret']
        self.sessionId = _generateSessionID()
        self.guardCode = None
        self.uuCookies = None
        self.buffCookies = None
        self.activeTreadNum = None
        self.status = self.refreshToken is not None
        self.originData = originData,
        self.filePath = filePath

    def _generateLoginSecure(self):
        if self._is_token_expired():
            self._refreshSession()

        return str(self.steamId) + '%7C%7C' + self.accessToken

    @property
    def steamLoginSecure(self):
        return self._generateLoginSecure()

    def _is_token_expired(self):
        try:
            if not self.accessToken:
                print(f"Steam:{self.account}, token不存在！")
                return False
            tokenComponents = self.accessToken.split(".")
            base64Str = tokenComponents[1].replace('-', '+').replace('_', '/')

            padding = len(base64Str) % 4
            if padding != 0:
                base64Str += '=' * (4 - padding)
            decodedBytes = base64.urlsafe_b64decode(base64Str)
            payload = decodedBytes.decode('utf-8')
            jsonObject = json.loads(payload)
            epochSecond = int(time.time())
            exp = jsonObject["exp"]

            return epochSecond + 1 * 60 * 60 > exp

        except Exception as e:
            raise Exception("Failed to decode JWT token") from e

    def _refreshSession(self):
        data = {
            "refresh_token": self.refreshToken,
            "steamid": self.steamId
        }

        try:
            resp = requests.post(url=GENERATE_ACCESS_TOKEN_FOR_APP, data=data, headers={'Referer': COMMUNITY_BASE},
                                 proxies=ProxyConfig.__dict__())
            if resp.status_code == 200 and resp.text is not None:
                body = resp.json()
                self.accessToken = body['response']['access_token']
        except ProxyError as e:

            return

    def getApiKey(self):
        if self.apiKey is not None:
            return self.apiKey
        headers = {
            'Host': 'steamcommunity.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-'
        }

        cookies = {
            'steamLoginSecure': self.steamLoginSecure,
            'sessionId': self.sessionId,
            'Steam_Language': 'english',
            'timezoneOffset': '28800,0',
            '_ga': 'GA1.2.234547838.1688523763',
            'browserid': '2685889387687629642',
            'strInventoryLastContext': '2504460_2',
        }

        proxy = {'https': 'http://127.0.0.1:10809'}
        resp = requests.get("https://steamcommunity.com/dev/apikey", cookies=cookies, headers=headers, proxies=proxy)
        pattern = "Key: [A-Z0-9]{20,33}"
        match = re.search(pattern=pattern, string=resp.text)
        if match:
            result = match.group().split(': ')[1]
            self.apiKey = result
            setIniValue(key='apiKey', section=str(self.steamId), value=result)
        print(f'{self.account}获取apiKey结果:{self.apiKey}')
        return self.apiKey
