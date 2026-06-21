from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .entity import KioskEntity

DIAG = EntityCategory.DIAGNOSTIC

# key, name, device_class, unit, icon, entity_category
SENSORS = [
    ("battery", "Battery", SensorDeviceClass.BATTERY, PERCENTAGE, None, None),
    ("camFps", "Camera FPS", None, "fps", "mdi:speedometer", DIAG),
    ("noiseLevel", "Noise Level", None, None, "mdi:volume-high", None),
    ("version", "Version", None, None, "mdi:information-outline", DIAG),
    ("batteryTemp", "Battery Temperature", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, None, DIAG),
    ("wifiSignal", "Wi-Fi Signal", None, PERCENTAGE, "mdi:wifi", DIAG),
    ("ssid", "Wi-Fi Network", None, None, "mdi:wifi", DIAG),
    ("wifiBand", "Wi-Fi Band", None, None, "mdi:wifi-cog", DIAG),
    ("linkMbps", "Wi-Fi Link Speed", None, "Mbit/s", "mdi:speedometer", DIAG),
    ("ip", "IP Address", None, None, "mdi:ip-network", DIAG),
    ("ramFreeMb", "Memory Free", None, "MB", "mdi:memory", DIAG),
    ("storageFreeGb", "Storage Free", None, "GB", "mdi:harddisk", DIAG),
    ("uptimeHours", "Uptime", None, "h", "mdi:timer-outline", DIAG),
    ("orientation", "Orientation", None, None, "mdi:screen-rotation", DIAG),
    ("pluggedType", "Power Source", None, None, "mdi:power-plug", DIAG),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(KioskSensor(coordinator, *args) for args in SENSORS)


class KioskSensor(KioskEntity, SensorEntity):
    def __init__(self, coordinator, key, name, device_class, unit, icon, category):
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
        if category:
            self._attr_entity_category = category

    @property
    def native_value(self):
        v = self._data.get(self._key)
        if v in ("", None):
            return None
        # Treat sentinel negatives (unknown) as unavailable.
        if self._key in ("wifiSignal", "batteryTemp", "linkMbps", "storageFreeGb", "uptimeHours"):
            try:
                if float(v) < 0:
                    return None
            except (TypeError, ValueError):
                pass
        return v
