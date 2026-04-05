# DVLA Vehicle Automations

## Manual Vehicle Tracking

Add vehicles to track manually using a script or automation:

```yaml
alias: "Add Vehicle to Tracking"
description: "Add a vehicle registration to DVLA tracking"
trigger:
  - platform: event
    event_type: call_service
    event_data:
      domain: input_text
      service: set_value
      service_data:
        entity_id: input_text.vehicle_to_add
action:
  - service: dvla_vehicle.lookup_vehicle
    data:
      registration: "{{ states('input_text.vehicle_to_add') }}"
```

## ANPR Camera Integration

Automatically look up vehicles detected by ANPR cameras:

```yaml
alias: "ANPR DVLA Vehicle Lookup"
description: "Looks up vehicle details when registration plates are detected by CCTV"
trigger:
  - platform: state
    entity_id: sensor.number_plates
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
        Vehicle {{loop.index}}: {{ plate }}
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

## Tax & MOT Expiry Alerts

Get notified before vehicle tax or MOT expires:

```yaml
alias: "Vehicle Tax Due Alert"
trigger:
  - platform: template
    value_template: >
      {% set vehicle = states.sensor.vehicle_ab12cde %}
      {% if vehicle and vehicle.attributes.tax_due_date %}
        {% set days = (vehicle.attributes.tax_due_date
           | as_datetime - now()).days %}
        {{ days is defined and 0 <= days <= 14 }}
      {% else %}
        false
      {% endif %}
action:
  - service: notify.mobile_app
    data:
      title: "Vehicle Tax Due"
      message: "Tax for {{ states('sensor.vehicle_ab12cde') }}
                is due in {{ (states.sensor.vehicle_ab12cde.attributes.tax_due_date
                | as_datetime - now()).days }} days"
```

```yaml
alias: "Vehicle MOT Expiry Alert"
trigger:
  - platform: template
    value_template: >
      {% set vehicle = states.sensor.vehicle_ab12cde %}
      {% if vehicle and vehicle.attributes.mot_expiry_date %}
        {% set days = (vehicle.attributes.mot_expiry_date
           | as_datetime - now()).days %}
        {{ days is defined and 0 <= days <= 30 }}
      {% else %}
        false
      {% endif %}
action:
  - service: notify.mobile_app
    data:
      title: "Vehicle MOT Expiring"
      message: "MOT for {{ states('sensor.vehicle_ab12cde') }}
                expires in {{ (states.sensor.vehicle_ab12cde.attributes.mot_expiry_date
                | as_datetime - now()).days }} days"
```

## Dashboard Display

Show vehicle status on a dashboard:

```yaml
type: entities
entities:
  - entity: sensor.vehicle_ab12cde
    name: My Vehicle
    secondary_info: last-updated
  - entity: sensor.vehicle_ab12cde
    attribute: make
    name: Make
  - entity: sensor.vehicle_ab12cde
    attribute: color
    name: Colour
  - entity: sensor.vehicle_ab12cde
    attribute: mot_status
    name: MOT Status
  - entity: sensor.vehicle_ab12cde
    attribute: mot_expiry_date
    name: MOT Expires
  - entity: sensor.vehicle_ab12cde
    attribute: tax_status
    name: Tax Status
  - entity: sensor.vehicle_ab12cde
    attribute: tax_due_date
    name: Tax Due
```
