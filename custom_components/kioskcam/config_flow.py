"""Config flow for KioskCam."""
from __future__ import annotations

import asyncio

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, WEB_PORT


class KioskCamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input["host"].strip()
            try:
                session = async_get_clientsession(self.hass)
                async with asyncio.timeout(8):
                    resp = await session.get(f"http://{host}:{WEB_PORT}/status")
                    await resp.json(content_type=None)
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="KioskCam", data={"host": host})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("host", default="192.168.1.37"): str}
            ),
            errors=errors,
        )
