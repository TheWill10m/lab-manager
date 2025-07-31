import requests

from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import TYPE_CHECKING
from urllib.parse import urljoin

if TYPE_CHECKING:
    from app.models.guests import _Guest


class _Host(ABC):
    def __init__(self, ipv4: IPv4Address) -> None:
        self._ipv4 = ipv4

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


class PhysicalHost(_Host):
    @abstractmethod
    def api_request(self, method: str, path: str):
        pass


class ProxmoxHost(PhysicalHost):
    def __init__(self, name: str, ipv4: IPv4Address, fqdn: str, api_token: str):
        super().__init__(ipv4)
        self._name = name
        self._virtual_hosts: list["_Guest"] = []
        self._fqdn = fqdn
        self._api_token = api_token

    @property
    def _api_url(self) -> str:
        return f"https://{self._fqdn}:8006/api2/json/nodes/{self._name}/"

    def api_request(self, method: str, path: str) -> dict:
        response = requests.request(
            method,
            urljoin(self._api_url, path),
            headers={"Authorization": f"PVEAPIToken={self._api_token}"},
        )
        response.raise_for_status()
        return response.json()["data"]

    def api_get(self, path: str) -> dict:
        return self.api_request("GET", path)

    def api_post(self, path: str) -> dict:
        return self.api_request("POST", path)

    def _get_status(self) -> dict:
        return self.api_get(f"status")

    def qemu_status(self, vmid: int) -> dict:
        return self.api_get(f"qemu/{vmid}/status/current")

    def qemu_start(self, vmid: int) -> None:
        self.api_post(f"qemu/{vmid}/status/start")

    def qemu_stop(self, vmid: int) -> None:
        self.api_post(f"qemu/{vmid}/status/stop")

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        self.api_post(f"status/stop")


class TrueNASHost(PhysicalHost): ...
