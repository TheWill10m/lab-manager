from PyNUTClient.PyNUT import PyNUTClient

from app.models.enums import UPSStatus


class NutServer(object):
    def __init__(self, host: str, user: str, password: str) -> None:
        self._nut_client = PyNUTClient(host=host, login=user, password=password)

        self.upss: list["UPS"] = []
        ups_names = self._nut_client.GetUPSNames()
        for name in ups_names:
            self.upss.append(UPS(name, self))

    def get_vars(self, ups_name: str) -> dict:
        vars = self._nut_client.GetUPSVars(ups_name)
        decoded_vars = {}
        for key, value in vars.items():
            decoded_vars[key.decode()] = value.decode()
        return decoded_vars


class UPS(object):
    STATUS_MAP = {"OL": UPSStatus.Online}

    def __init__(self, name: str, server: NutServer):
        self.name = name
        self.server = server
        self._vars: dict[str, str] = {}

    def refresh_vars(self) -> None:
        self.server.get_vars(self.name)

    def print_vars(self) -> None:
        for k, v in self._vars.items():
            print(k, v)

    @property
    def charge(self) -> float:
        return float(self._vars["battery.charge"])

    @property
    def status(self) -> UPSStatus:
        return self.STATUS_MAP[self._vars["ups.status"]]
