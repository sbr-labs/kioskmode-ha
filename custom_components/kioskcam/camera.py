from __future__ import annotations

import asyncio

from homeassistant.components.camera import Camera, CameraEntityFeature

from .const import DOMAIN, RTSP_PORT, WEB_PORT
from .entity import KioskEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KioskCamera(coordinator)])


class KioskCamera(KioskEntity, Camera):
    _attr_name = "Kiosk Mode"
    _attr_unique_id = "kioskcam_camera"
    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, coordinator):
        KioskEntity.__init__(self, coordinator)
        Camera.__init__(self)

    async def stream_source(self) -> str | None:
        return f"rtsp://{self.coordinator.host}:{RTSP_PORT}/"

    async def async_camera_image(self, width=None, height=None):
        url = f"http://{self.coordinator.host}:{WEB_PORT}/snapshot.jpg"
        try:
            async with asyncio.timeout(8):
                resp = await self.coordinator.session.get(url)
                if resp.status == 200:
                    return await resp.read()
        except Exception:  # noqa: BLE001
            return None
        return None
