"""DataUpdateCoordinator for DVLA Vehicle integration."""
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class DVLAVehicleDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching DVLA Vehicle data."""

    def __init__(
        self,
        hass: HomeAssistant,
        vehicle_api,
        registration: str,
        update_interval: timedelta | None,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.vehicle_api = vehicle_api
        self.registration = registration

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.hass.async_add_executor_job(
                self.vehicle_api.fetch_vehicle_data,
                self.registration,
            )
        except Exception as error:
            raise UpdateFailed(f"Error communicating with API: {error}")