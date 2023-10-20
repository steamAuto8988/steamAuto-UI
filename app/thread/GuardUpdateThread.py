import time

from PyQt5.QtCore import QThread, pyqtSignal


from app.steam.Session import SteamSession
from app.steam.guard import generate_one_time_code


class GuardUpdateThread(QThread):
    _finished = pyqtSignal(SteamSession)

    def __init__(self, steamData: list):
        super().__init__()
        self.steamData = steamData

    def run(self) -> None:
        self._updateGuardCode()

    def _updateGuardCode(self):
        while True:
            try:
                for steam in self.steamData:
                    code = generate_one_time_code(steam.sharedSecret)
                    steam.guardCode = code
                    self._finished.emit(steam)
            except Exception as e:
                print(e)
            time.sleep(10)
