from abc import ABC
from ipaddress import IPv4Address

from app.models.enums import PowerStatus
from app.models.hosts import ProxmoxHost, _Host


class _Guest(_Host, ABC):
    def __init__(self, ipv4: IPv4Address, hypervisor: ProxmoxHost, id: int):
        super().__init__(ipv4)
        self._hypervisor = hypervisor
        self._id = id


class QemuGuest(_Guest):
    POWER_STATUS_MAP = {
        "stopped": PowerStatus.STOPPED,
        "running": PowerStatus.RUNNING,
    }

    def _get_status(self) -> dict:
        return self._hypervisor.qemu_status(self._id)

    @property
    def power_status(self) -> PowerStatus:
        return self.POWER_STATUS_MAP[self._get_status()["status"]]

    def start(self) -> None:
        current_status = self.power_status
        if current_status != PowerStatus.STOPPED:
            print(f"QemuGuest {self._id} is {current_status}, can't start")
            return
        self._hypervisor.qemu_start(self._id)

    def stop(self) -> None:
        current_status = self.power_status
        if current_status != PowerStatus.RUNNING:
            print(f"QemuGuest {self._id} is {current_status}, can't stop")
            return
        self._hypervisor.qemu_stop(self._id)


class LinuxContainer(_Guest): ...
