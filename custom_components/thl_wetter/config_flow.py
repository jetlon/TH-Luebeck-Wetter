"""Config flow for the THL Campus Wetterstation integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class ThlWetterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for THL Campus Wetterstation."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Single-instance setup - keine weiteren Eingaben nötig."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="THL Campus Wetterstation", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
