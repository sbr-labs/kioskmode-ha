from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class KioskEntity(CoordinatorEntity):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.host)},
            name="Kiosk Mode",
            manufacturer="Sean",
            model="Tablet Kiosk Camera",
            configuration_url=f"http://{coordinator.host}:2323/",
        )

    @property
    def _data(self) -> dict:
        return self.coordinator.data or {}
