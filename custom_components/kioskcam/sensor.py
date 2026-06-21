from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from .entity import KioskEntity

# key, name, device_class, unit, icon
SENSORS = [
    ("battery", "Battery", SensorDeviceClass.BATTERY, PERCENTAGE, None),
    ("camFps", "Camera FPS", None, "fps", "mdi:speedometer"),
    ("noiseLevel", "Noise Level", None, None, "mdi:volume-high"),
    ("version", "Version", None, None, "mdi:information-outline"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KioskSensor(coordinator, key, name, dc, unit, icon)
        for key, name, dc, unit, icon in SENSORS
    )


class KioskSensor(KioskEntity, SensorEntity):
    def __init__(self, coordinator, key, name, device_class, unit, icon):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kiosk Mode {name}"
        self._attr_unique_id = f"kioskcam_{key}"
        if device_class:
            self._attr_device_class = device_class
        if unit:
            self._attr_native_unit_of_measurement = unit
        if icon:
            self._attr_icon = icon

    @property
    def native_value(self):
        return self._data.get(self._key)
