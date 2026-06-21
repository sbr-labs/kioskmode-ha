"""KioskCam integration: polls the tablet's web admin and exposes a device."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, WEB_PORT

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH, Platform.CAMERA]


class KioskCamCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str) -> None:
        super().__init__(
            hass, _LOGGER, name="KioskCam", update_interval=timedelta(seconds=10)
        )
        self.host = host
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        url = f"http://{self.host}:{WEB_PORT}/status"
        try:
            async with asyncio.timeout(8):
                resp = await self.session.get(url)
                return await resp.json(content_type=None)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"KioskCam unreachable: {err}") from err


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = KioskCamCoordinator(hass, entry.data["host"])
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
