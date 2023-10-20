import time

import requests

from app.config.utils import reloadConfig, getIniValue
from app.steam.apiEndpoints import COMMUNITY_BASE
from app.thread.buff import BASE_API

config = reloadConfig()
cookie = getIniValue(key='BUFF', section='76561199238312159', default="")

# buff_headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
#     "Cookie": cookie
# }
# try:
#     respJson = requests.get(url=BASE_API + '/api/message/notification', headers=buff_headers).json()
#     print(respJson)
#     to_deliver_order = respJson["data"]["to_deliver_order"]
#     to_send_offer_order = respJson["data"]["to_send_offer_order"]
#     for item in GameInfo.items():
#         gameName = item[1]
#         if gameName.lower() in to_send_offer_order:
#             print(f'steam: - {gameName} 需要发送的报价个数：{to_deliver_order[gameName.lower()]}')
#         if gameName.lower() in to_deliver_order:
#             print(f'steam: - {gameName} 需要确认的报价个数：{to_deliver_order[gameName.lower()]}')
# except Exception as e:
#     print(e)


buff_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
    "Cookie": cookie
}
try:
    print(BASE_API + '/api/market/steam_trade?_=' + str(int(time.time())))
    respJson = requests.get(url=BASE_API + '/api/market/steam_trade?_=' + str(int(time.time())),
                            headers=buff_headers).json()
    if respJson['code'] == 'OK':
        for item in respJson['data']:
            bot_name = item['bot_name']
            tradeofferid = item['tradeofferid']
            print(f'对方账号：{bot_name},报价id:{tradeofferid}')
            tradeOfferUrl = COMMUNITY_BASE + "/tradeoffer/{}/".format(tradeofferid)


except Exception as e:
    print(e)
