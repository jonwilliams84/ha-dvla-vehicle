# DVLA Vehicle Information for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This custom component integrates with the DVLA Vehicle Enquiry Service API to provide vehicle information in Home Assistant. It can be used standalone or integrated with ANPR cameras for automatic vehicle lookups.

## Features

- Look up vehicle details using registration numbers
- Automatic vehicle lookups from ANPR camera detection
- Caches results to minimize API calls
- Creates sensors with comprehensive vehicle information
- Supports multiple vehicles
- Integrates with notifications
- Support for batch processing of multiple plates

## Installation

### HACS Installation (Recommended)

1. Add this repository as a custom repository in HACS:
   - HACS → Integrations → 3 dots (top right) → Custom repositories
   - URL: `your-repository-url`
   - Category: Integration

2. Click Install

### Manual Installation

1. Copy the `dvla_vehicle` directory to your `custom_components` directory:
```bash
cd /config/custom_components
git clone your-repository-url
```

2. Restart Home Assistant

## Configuration

### Initial Setup

1. Get your DVLA API key from [DVLA Developer Portal](https://developer-portal.driver-vehicle-licensing.api.gov.uk/)
2. In Home Assistant, go to Configuration → Integrations
3. Click the + button and search for "DVLA Vehicle Information"
4. Enter your API key and a vehicle registration

### Service Calls

The integration provides a service to look up vehicles:

```yaml
service: dvla_vehicle.lookup_vehicle
data:
  registration: "AB12CDE"
```

### Integration with ANPR

If you have an ANPR camera that provides registration plates via a sensor, you can use this automation:

```yaml
alias: "ANPR DVLA Vehicle Lookup"
description: "Looks up vehicle details when new registration plates are detected by CCTV"
trigger:
  - platform: state
    entity_id: sensor.number_plates_2
condition:
  - condition: template
    value_template: "{{ trigger.to_state.state | length > 0 }}"
action:
  - variables:
      plates: >-
        {{ trigger.to_state.state.split(',') | map('trim') | list }}
  - repeat:
      count: "{{ plates | length }}"
      sequence:
        - service: dvla_vehicle.lookup_vehicle
          data:
            registration: "{{ plates[repeat.index-1] }}"
        - delay: 2
  - delay: 5
  - service: persistent_notification.create
    data:
      title: "New Vehicles Detected"
      message: |-
        {% for plate in plates %}
        Vehicle {{loop.index}}:
        Registration: {{ plate }}
          {% for entity in states.sensor if entity.attributes.registration_number is defined %}
            {% if entity.attributes.registration_number == plate %}
        Make: {{ entity.attributes.make }}
        Color: {{ entity.attributes.color }}
        Year: {{ entity.attributes.year_of_manufacture }}
        MOT Status: {{ entity.attributes.mot_status }}
        Tax Status: {{ entity.attributes.tax_status }}
            {% endif %}
          {% endfor %}
        {% endfor %}
```

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

## Example Uses

### Dashboard Card
```yaml
type: entities
entities:
  - entity: sensor.vehicle_ab12cde
    secondary_info: last-updated
```

### Conditional Alerts
```yaml
alias: "Vehicle Tax Due Alert"
trigger:
  - platform: template
    value_template: >
      {% set days = (states.sensor.vehicle_ab12cde.attributes.tax_due_date 
         | as_datetime - now()).days %}
      {{ days <= 14 }}
action:
  - service: notify.mobile_app
    data:
      title: "Vehicle Tax Due"
      message: "Tax for vehicle {{ states.sensor.vehicle_ab12cde.attributes.registration_number }} 
                is due in {{ days }} days"
```

### Multiple Vehicle Status
```yaml
type: custom:auto-entities
card:
  type: entities
  title: Vehicle Fleet Status
filter:
  include:
    - integration: dvla_vehicle
sort:
  method: name
```

## Troubleshooting

### API Rate Limits
The DVLA API has rate limits. The integration caches results to minimize API calls, but be mindful of how often you trigger lookups.

### Common Issues
1. "No details held by DVLA" - This is a valid response from the API for some vehicles
2. Config flow errors - Usually resolved by restarting Home Assistant
3. Multiple plates not being processed - Check the format of your ANPR sensor output

## Support

For issues and feature requests, please use the GitHub issues page.

## Credits

Built using the DVLA Vehicle Enquiry Service API.
