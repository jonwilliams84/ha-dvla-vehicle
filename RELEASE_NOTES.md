Release: 2.0.0

Breaking changes:

• Lookup service no longer auto-creates config entries. Vehicles must be added manually through Settings → Integrations or discovered via the UI. This prevents unwanted entries being created by automated lookups.
• Database now shared across all vehicles (dvla_vehicle.db) instead of per-entry files.

New features:

• Added brand logos (brand/icon.png, brand/logo.png) in DVLA style for the HA integrations panel
• Documentation restructure with dedicated automations guide

Bug fixes:

• Single shared database prevents file proliferation when tracking many vehicles.
