from __future__ import annotations

import asyncio

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from .const import DOMAIN, WEB_PORT
from .entity import KioskEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KioskScreenSwitch(coordinator)])


class KioskScreenSwitch(KioskEntity, SwitchEntity):
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kiosk Mode Screen"
        self._attr_unique_id = "kioskcam_screen_switch"
        self._attr_icon = "mdi:tablet-dashboard"

    @property
    def is_on(self):
        return bool(self._data.get("screenOn"))

    async def _cmd(self, path: str) -> None:
        url = f"http://{self.coordinator.host}:{WEB_PORT}{path}"
        try:
            async with asyncio.timeout(8):
                await self.coordinator.session.get(url)
        except Exception:  # noqa: BLE001
            pass
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs):
        await self._cmd("/screen/on")

    async def async_turn_off(self, **kwargs):
        await self._cmd("/screen/off")
