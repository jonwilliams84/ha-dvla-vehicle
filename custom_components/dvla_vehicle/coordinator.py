"""DataUpdateCoordinator for DVLA Vehicle integration."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .vehicle import VehicleLookupSystem
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class DVLAVehicleDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching DVLA Vehicle data."""

    def __init__(
        self,
        hass: HomeAssistant,
        vehicle_api: VehicleLookupSystem,
        registration: str,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.vehicle_api = vehicle_api
        self.registration = registration

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.hass.async_add_executor_job(
                self.vehicle_api.fetch_vehicle_data, self.registration
            )
            if data is None:
                raise UpdateFailed(f"No data returned for {self.registration}")
            return data
        except Exception as error:
            raise UpdateFailed(f"Error communicating with API: {error}")

