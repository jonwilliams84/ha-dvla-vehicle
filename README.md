# ha-dvla-vehicle

Home Assistant Custom Component for DVLA Vehicle Enquiry Service

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This custom component integrates with the DVLA Vehicle Enquiry Service API to provide vehicle information in Home Assistant.

## Features

- Look up vehicle details using registration numbers
- Vehicles must be added manually (no auto-creation on lookup)
- Caches results to minimise API calls
- Creates sensors with comprehensive vehicle information
- Supports multiple vehicles
- Integrates with notifications

## Installation

### HACS Installation (Recommended)

1. Add this repository as a custom repository in HACS:
   - HACS → Integrations → 3 dots (top right) → Custom repositories
   - URL: `https://github.com/jonwilliams84/ha-dvla-vehicle`
   - Category: Integration

2. Click Install

### Manual Installation

1. Copy the `dvla_vehicle` directory to your `custom_components` directory:
```bash
cd /config/custom_components
git clone https://github.com/jonwilliams84/ha-dvla-vehicle
```

2. Restart Home Assistant

## Configuration

### Initial Setup

1. Get your DVLA API key from [DVLA Developer Portal](https://developer-portal.driver-vehicle-licensing.api.gov.uk/)
2. In Home Assistant, go to Configuration → Integrations
3. Click the + button and search for "DVLA Vehicle Information"
4. Enter your API key and a vehicle registration

### Adding Vehicles

Vehicles are not automatically created on lookup. Use the service to add vehicles you want to track:

```yaml
service: dvla_vehicle.lookup_vehicle
data:
  registration: "AB12CDE"
```

See [Automations](docs/automations.md) for example workflows including manual tracking, ANPR integration, and alerts.

## Available Data

Each vehicle sensor provides the following attributes:

- Make
- Color
- Fuel Type
- MOT Status & Expiry
- Tax Status & Due Date
- Year of Manufacture
- Engine Capacity
- CO2 Emissions
- Euro Status
- Real Driving Emissions
- Type Approval
- Wheelplan
- Revenue Weight
- Date of Last V5C Issue
- ART End Date
- Marked for Export Status

## Troubleshooting

### API Rate Limits

The DVLA API has rate limits. The integration caches results to minimise API calls, but be mindful of how often you trigger lookups.

### Common Issues

1. "No details held by DVLA" — valid response from the API for some vehicles
2. Config flow errors — usually resolved by restarting Home Assistant
3. Multiple plates not being processed — check the format of your ANPR sensor output

## Support

For issues and feature requests, please use the GitHub issues page.

## Credits

Built using the DVLA Vehicle Enquiry Service API.
