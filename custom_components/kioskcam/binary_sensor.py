from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .const import DOMAIN
from .entity import KioskEntity

# key, name, device_class, icon (icon only used when no device_class)
BINARY = [
    ("streaming", "Streaming", BinarySensorDeviceClass.RUNNING, None),
    ("motion", "Motion", BinarySensorDeviceClass.MOTION, None),
    ("face", "Face", BinarySensorDeviceClass.OCCUPANCY, None),
    ("noise", "Noise", BinarySensorDeviceClass.SOUND, None),
    ("charging", "Charging", BinarySensorDeviceClass.BATTERY_CHARGING, None),
    ("screenOn", "Screen On", None, "mdi:tablet-dashboard"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KioskBinarySensor(coordinator, key, name, dc, icon)
        for key, name, dc, icon in BINARY
    )


class KioskBinarySensor(KioskEntity, BinarySensorEntity):
    def __init__(self, coordinator, key, name, device_class, icon):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kiosk Mode {name}"
        self._attr_unique_id = f"kioskcam_{key}"
        if device_class:
            self._attr_device_class = device_class
        if icon:
            self._attr_icon = icon

    @property
    def is_on(self):
        return bool(self._data.get(self._key))
