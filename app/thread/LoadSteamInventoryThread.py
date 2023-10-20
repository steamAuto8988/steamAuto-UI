from PyQt5.QtCore import QThread, pyqtSignal

from app.steam.Session import SteamSession
from app.steam.inventory import getInventory, Descriptions, Asset, InventoryResp, InventoryCode


class LoadSteamInventoryThread(QThread):
    _finished = pyqtSignal(InventoryResp)

    def __init__(self, loadSteamData: SteamSession):
        super().__init__()
        self.loadSteamData = loadSteamData

    def run(self) -> None:
        inventoryResp = InventoryResp(account=self.loadSteamData.account, steamId=self.loadSteamData.steamId,
                                      code=InventoryCode.success, assets=[])
        steamId = self.loadSteamData.steamId

        resp = getInventory(steamId, '730', 'schinese')

        if resp is None:
            inventoryResp.code = InventoryCode.retry
        elif resp == 'null':
            inventoryResp.code = InventoryCode.notOpen
        elif resp.status_code == 429:
            inventoryResp.code = InventoryCode.toolManyRequest
        else:
            inventoryJson = resp.json()
            total_inventory_count = inventoryJson['total_inventory_count']
            if total_inventory_count > 0:
                for assetItem in inventoryJson['assets']:
                    for desc in inventoryJson['descriptions']:
                        if assetItem['instanceid'] == desc['instanceid'] and assetItem['classid'] == desc[
                            'classid']:
                            descriptions = Descriptions(desc)
                            if 'AK' in desc['market_name']:
                                descriptions.canTrade = False
                            asset = Asset(assetItem, descriptions=descriptions)
                            inventoryResp.assets.append(asset)
                inventoryResp.code = InventoryCode.success
            else:
                inventoryResp.code = InventoryCode.inventoryIsZero

        self._finished.emit(inventoryResp)
