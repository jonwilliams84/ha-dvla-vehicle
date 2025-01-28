"""Constants for the DVLA Vehicle integration."""
from typing import Final

DOMAIN: Final = "dvla_vehicle"
CONF_API_KEY: Final = "api_key"
CONF_REGISTRATION: Final = "registration"
CONF_UPDATE_INTERVAL: Final = "update_interval"
CONF_DISABLE_UPDATES: Final = "disable_updates"

DEFAULT_SCAN_INTERVAL = timedelta(days=1)  # 24 hours
UPDATE_INTERVALS = {
    "Disabled": None,
    "1 hour": timedelta(hours=1),
    "12 hours": timedelta(hours=12),
    "1 day": timedelta(days=1),
    "1 week": timedelta(days=7),
    "1 month": timedelta(days=30),
}

# All possible attributes
ATTR_ART_END_DATE: Final = "art_end_date"
ATTR_CO2_EMISSIONS: Final = "co2_emissions"
ATTR_COLOR: Final = "color"
ATTR_ENGINE_CAPACITY: Final = "engine_capacity"
ATTR_FUEL_TYPE: Final = "fuel_type"
ATTR_MAKE: Final = "make"
ATTR_MARKED_FOR_EXPORT: Final = "marked_for_export"
ATTR_MONTH_OF_FIRST_REG: Final = "month_of_first_registration"
ATTR_MOT_STATUS: Final = "mot_status"
ATTR_REGISTRATION: Final = "registration_number"
ATTR_REVENUE_WEIGHT: Final = "revenue_weight"
ATTR_TAX_DUE_DATE: Final = "tax_due_date"
ATTR_TAX_STATUS: Final = "tax_status"
ATTR_TYPE_APPROVAL: Final = "type_approval"
ATTR_WHEELPLAN: Final = "wheelplan"
ATTR_YEAR: Final = "year_of_manufacture"
ATTR_EURO_STATUS: Final = "euro_status"
ATTR_REAL_DRIVING_EMISSIONS: Final = "real_driving_emissions"
ATTR_DATE_OF_LAST_V5C: Final = "date_of_last_v5c_issued"
