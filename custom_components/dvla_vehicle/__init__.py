"""The DVLA Vehicle integration."""
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
    api_key = entry.data[CONF_API_KEY]

    api = VehicleLookupSystem(
        db_path=hass.config.path("dvla_vehicle.db"),
        api_key=api_key,
    )

    # Store API key globally so the lookup service can use it
    hass.data[DOMAIN]["api_key"] = api_key

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

    # Register lookup service — reads API key from first configured entry
    async def handle_lookup(call: ServiceCall) -> None:
        """Handle the service call — look up vehicle data without creating an entry."""
        registration = call.data[CONF_REGISTRATION].upper()

        stored_api_key = hass.data[DOMAIN].get("api_key")
        if not stored_api_key:
            _LOGGER.error(
                "No API key available — please add a DVLA Vehicle config entry first"
            )
            return

        temp_api = VehicleLookupSystem(
            db_path=hass.config.path("dvla_vehicle.db"),
            api_key=stored_api_key,
        )

        result = await hass.async_add_executor_job(
            temp_api.fetch_vehicle_data, registration
        )

        if result:
            hass.bus.async_fire(
                f"{DOMAIN}_vehicle_lookup",
                {"registration": registration, "data": result},
            )
            _LOGGER.debug(f"Lookup result for {registration}: {result}")
        else:
            _LOGGER.warning(f"No data found for {registration}")

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
