"""Config flow for the THL Campus Wetterstation integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_SCAN_INTERVAL_MINUTES,
    DEFAULT_SCAN_INTERVAL_MINUTES,
    DOMAIN,
    MAX_SCAN_INTERVAL_MINUTES,
    MIN_SCAN_INTERVAL_MINUTES,
)


def _scan_interval_schema(default: int) -> vol.Schema:
    """Schema für das Abfrageintervall (Minuten), gemeinsam von Config- und Options-Flow genutzt."""
    return vol.Schema(
        {
            vol.Required(CONF_SCAN_INTERVAL_MINUTES, default=default): vol.All(
                vol.Coerce(int),
                vol.Range(min=MIN_SCAN_INTERVAL_MINUTES, max=MAX_SCAN_INTERVAL_MINUTES),
            )
        }
    )


class ThlWetterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for THL Campus Wetterstation."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Single-instance setup - fragt das gewünschte Abfrageintervall ab."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="THL Campus Wetterstation", data={}, options=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_scan_interval_schema(DEFAULT_SCAN_INTERVAL_MINUTES),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ThlWetterOptionsFlow:
        """Options-Flow, um das Abfrageintervall nachträglich zu ändern."""
        return ThlWetterOptionsFlow(config_entry)


class ThlWetterOptionsFlow(config_entries.OptionsFlow):
    """Erlaubt das nachträgliche Ändern des Abfrageintervalls über 'Konfigurieren'."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Einziger Options-Schritt: Abfrageintervall abfragen/ändern."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self._config_entry.options.get(
            CONF_SCAN_INTERVAL_MINUTES, DEFAULT_SCAN_INTERVAL_MINUTES
        )
        return self.async_show_form(
            step_id="init", data_schema=_scan_interval_schema(current)
        )
