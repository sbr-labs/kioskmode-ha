from __future__ import annotations

import asyncio

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity

from .const import DOMAIN, WEB_PORT
from .entity import KioskEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KioskTorch(coordinator), KioskScreenLight(coordinator)])


class _Base(KioskEntity, LightEntity):
    async def _get(self, path: str) -> None:
        url = f"http://{self.coordinator.host}:{WEB_PORT}{path}"
        try:
            async with asyncio.timeout(8):
                await self.coordinator.session.get(url)
        except Exception:  # noqa: BLE001
            pass
        await self.coordinator.async_request_refresh()


class KioskTorch(_Base):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kiosk Mode Torch"
        self._attr_unique_id = "kioskcam_torch"
        self._attr_icon = "mdi:flashlight"

    @property
    def is_on(self):
        return bool(self._data.get("torchOn"))

    async def async_turn_on(self, **kwargs):
        await self._get("/torch?on=1")

    async def async_turn_off(self, **kwargs):
        await self._get("/torch?on=0")


class KioskScreenLight(_Base):
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kiosk Mode Screen Light"
        self._attr_unique_id = "kioskcam_screenlight"
        self._attr_icon = "mdi:television-ambient-light"

    @property
    def is_on(self):
        return bool(self._data.get("screenLightOn"))

    @property
    def brightness(self):
        lvl = self._data.get("screenLightLevel") or 80
        return round(lvl * 255 / 100)

    async def async_turn_on(self, **kwargs):
        b = kwargs.get(ATTR_BRIGHTNESS)
        level = round(b * 100 / 255) if b is not None else (self._data.get("screenLightLevel") or 80)
        await self._get(f"/light?on=1&level={int(level)}")

    async def async_turn_off(self, **kwargs):
        await self._get("/light?on=0")
