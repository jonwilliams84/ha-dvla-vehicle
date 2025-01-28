"""The DVLA Vehicle integration."""
import asyncio
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN, CONF_API_KEY, CONF_REGISTRATION
from .coordinator import DVLAVehicleDataUpdateCoordinator
from .vehicle import VehicleLookupSystem

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]

SERVICE_LOOKUP_SCHEMA = vol.Schema({
    vol.Required(CONF_REGISTRATION): cv.string,
})

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the DVLA Vehicle component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DVLA Vehicle from a config entry."""
    api = VehicleLookupSystem(
        db_path=hass.config.path(f"dvla_vehicle_{entry.entry_id}.db"),
        api_key=entry.data[CONF_API_KEY],
    )

    coordinator = DVLAVehicleDataUpdateCoordinator(
        hass,
        api,
        entry.data[CONF_REGISTRATION],
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register lookup service
    async def handle_lookup(call: ServiceCall) -> None:
        """Handle the service call."""
        registration = call.data[CONF_REGISTRATION].upper()

        # Check if entry already exists
        existing_entries = [
            entry for entry in hass.config_entries.async_entries(DOMAIN)
            if entry.data.get(CONF_REGISTRATION) == registration
        ]

        if existing_entries:
            # Update existing entry
            entry_id = existing_entries[0].entry_id
            coordinator = hass.data[DOMAIN][entry_id]
            await coordinator.async_refresh()
            return

        # Create new entry using current API key
        api_key = entry.data[CONF_API_KEY]
        
        # Create new config entry
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": "user"},
            data={
                CONF_API_KEY: api_key,
                CONF_REGISTRATION: registration,
            },
        )

    hass.services.async_register(
        DOMAIN,
        "lookup_vehicle",
        handle_lookup,
        schema=SERVICE_LOOKUP_SCHEMA,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
