class offer(object):
    def __init__(self):
        pass


class OffersResponse(object):
    def __init__(self, index: int, steamId: str,activeNum:int):
        self.index = index
        self.steamId = steamId
        self.activeNum = activeNum
