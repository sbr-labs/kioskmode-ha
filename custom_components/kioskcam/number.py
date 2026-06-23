from __future__ import annotations

import asyncio

from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE

from .const import DOMAIN, WEB_PORT
from .entity import KioskEntity

# key, name, icon
NUMBERS = [
    ("brightness", "Brightness", "mdi:brightness-6"),
    ("volume", "Volume", "mdi:volume-high"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(KioskNumber(coordinator, *args) for args in NUMBERS)


class KioskNumber(KioskEntity, NumberEntity):
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator, key, name, icon):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kiosk Mode {name}"
        self._attr_unique_id = f"kioskcam_{key}_num"
        self._attr_icon = icon

    @property
    def native_value(self):
        v = self._data.get(self._key)
        if v is None or v < 0:  # -1 = auto/unset
            return None
        return v

    async def async_set_native_value(self, value: float) -> None:
        url = f"http://{self.coordinator.host}:{WEB_PORT}/set?{self._key}={int(value)}"
        try:
            async with asyncio.timeout(8):
                await self.coordinator.session.get(url)
        except Exception:  # noqa: BLE001
            pass
        await self.coordinator.async_request_refresh()
