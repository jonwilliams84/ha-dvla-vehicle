"""Config flow for DVLA Vehicle integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_REGISTRATION,
    CONF_UPDATE_INTERVAL,
    CONF_DISABLE_UPDATES,
    UPDATE_INTERVALS,
)
from .vehicle import VehicleLookupSystem

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DVLA Vehicle."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                # Store update interval choice
                interval_choice = user_input.get(CONF_UPDATE_INTERVAL)
                update_interval = UPDATE_INTERVALS.get(interval_choice, UPDATE_INTERVALS["1 day"])
                
                # Create data dict without the interval choice string
                data = {
                    CONF_API_KEY: user_input[CONF_API_KEY],
                    CONF_REGISTRATION: user_input[CONF_REGISTRATION].upper(),
                    CONF_DISABLE_UPDATES: user_input.get(CONF_DISABLE_UPDATES, False),
                    CONF_UPDATE_INTERVAL: update_interval.total_seconds() if update_interval else None,
                }

                # Test the API connection
                vehicle_api = VehicleLookupSystem(
                    db_path=":memory:",
                    api_key=data[CONF_API_KEY],
                )
                
                result = await self.hass.async_add_executor_job(
                    vehicle_api.fetch_vehicle_data,
                    data[CONF_REGISTRATION],
                )
                
                if result:
                    return self.async_create_entry(
                        title=f"Vehicle {data[CONF_REGISTRATION]}",
                        data=data,
                    )
                else:
                    errors["base"] = "cannot_connect"
                    
            except Exception as error:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Prepare the form schema
        schema = {
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_REGISTRATION): str,
            vol.Required(CONF_UPDATE_INTERVAL, default="1 day"): vol.In(UPDATE_INTERVALS.keys()),
            vol.Optional(CONF_DISABLE_UPDATES, default=False): bool,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(schema),
            errors=errors,
        )
