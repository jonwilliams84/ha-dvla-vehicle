"""Sensor platform for DVLA Vehicle integration."""
from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ATTR_ART_END_DATE,
    ATTR_CO2_EMISSIONS,
    ATTR_COLOR,
    ATTR_ENGINE_CAPACITY,
    ATTR_FUEL_TYPE,
    ATTR_MAKE,
    ATTR_MARKED_FOR_EXPORT,
    ATTR_MONTH_OF_FIRST_REG,
    ATTR_MOT_STATUS,
    ATTR_REGISTRATION,
    ATTR_REVENUE_WEIGHT,
    ATTR_TAX_DUE_DATE,
    ATTR_TAX_STATUS,
    ATTR_TYPE_APPROVAL,
    ATTR_WHEELPLAN,
    ATTR_YEAR,
    ATTR_EURO_STATUS,
    ATTR_REAL_DRIVING_EMISSIONS,
    ATTR_DATE_OF_LAST_V5C,
)
from .coordinator import DVLAVehicleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up DVLA Vehicle sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DVLAVehicleSensor(coordinator, entry)])

class DVLAVehicleSensor(CoordinatorEntity, SensorEntity):
    """Representation of a DVLA Vehicle sensor."""

    def __init__(
        self,
        coordinator: DVLAVehicleDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{config_entry.data['registration']}"
        self._attr_name = f"Vehicle {config_entry.data['registration']}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data:
            make = self.coordinator.data.get("make", "Unknown")
            return make
        return "Unknown"

    def _format_date(self, date_str: str | None) -> str | None:
        """Format date string to YYYY-MM-DD."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return date_str

    def _format_year(self, year: Any) -> str | None:
        """Format year as YYYY."""
        if not year:
            return None
        try:
            return f"{int(year):04d}"
        except (ValueError, TypeError):
            return str(year)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        data = self.coordinator.data
        
        return {
            ATTR_ART_END_DATE: self._format_date(data.get("artEndDate")),
            ATTR_CO2_EMISSIONS: data.get("co2Emissions"),
            ATTR_COLOR: data.get("colour"),
            ATTR_ENGINE_CAPACITY: data.get("engineCapacity"),
            ATTR_FUEL_TYPE: data.get("fuelType"),
            ATTR_MAKE: data.get("make"),
            ATTR_MARKED_FOR_EXPORT: data.get("markedForExport"),
            ATTR_MONTH_OF_FIRST_REG: data.get("monthOfFirstRegistration"),
            ATTR_MOT_STATUS: data.get("motStatus"),
            ATTR_REGISTRATION: data.get("registrationNumber"),
            ATTR_REVENUE_WEIGHT: data.get("revenueWeight"),
            ATTR_TAX_DUE_DATE: self._format_date(data.get("taxDueDate")),
            ATTR_TAX_STATUS: data.get("taxStatus"),
            ATTR_TYPE_APPROVAL: data.get("typeApproval"),
            ATTR_WHEELPLAN: data.get("wheelplan"),
            ATTR_YEAR: self._format_year(data.get("yearOfManufacture")),
            ATTR_EURO_STATUS: data.get("euroStatus"),
            ATTR_REAL_DRIVING_EMISSIONS: data.get("realDrivingEmissions"),
            ATTR_DATE_OF_LAST_V5C: self._format_date(data.get("dateOfLastV5CIssued")),
        }
