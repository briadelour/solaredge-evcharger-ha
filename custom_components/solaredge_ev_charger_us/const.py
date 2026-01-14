"""Constants for the SolarEdge EV Charger integration."""

DOMAIN = "solaredge_ev_charger_us"
PLATFORMS = ["sensor", "binary_sensor", "button"]

# Configuration keys
CONF_SITE_ID = "site_id"
CONF_COOKIE = "cookie"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_TIMEOUT = "timeout"
CONF_DEVICE_ID = "device_id"

# Default values
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_TIMEOUT = 30
DEFAULT_NAME = "SolarEdge EV Charger"

# API endpoints
API_BASE_URL = "https://monitoring.solaredge.com"
API_DEVICES_ENDPOINT = "/services/api/homeautomation/v1.0/sites/{site_id}/devices"
API_CONTROL_ENDPOINT = "/services/m/api/homeautomation/v1.0/{site_id}/devices/{device_id}/activationState"

# Cookie name
COOKIE_NAME = "SPRING_SECURITY_REMEMBER_ME_COOKIE"

# Charger status values
CHARGER_STATUS_CHARGING = "CHARGING"
CHARGER_STATUS_PLUGGED_IN = "PLUGGED_IN"
CHARGER_STATUS_NOT_CONNECTED = "NOT_CONNECTED"

# Connection status values
CONNECTION_STATUS_CHARGING = "CHARGING"
CONNECTION_STATUS_CONNECTED = "CONNECTED"
CONNECTION_STATUS_DISCONNECTED = "DISCONNECTED"

# Activation modes
MODE_MANUAL = "MANUAL"
MODE_AUTO = "AUTO"

# Excess PV values
EXCESS_PV_ENABLED = -1
EXCESS_PV_DISABLED = -2

# Sensor icons
ICON_EV_STATION = "mdi:ev-station"
ICON_EV_PLUG = "mdi:ev-plug-type2"
ICON_CAR = "mdi:car-electric"
ICON_SOLAR = "mdi:solar-power"
ICON_SOLAR_VARIANT = "mdi:solar-power-variant-outline"
ICON_CALENDAR = "mdi:calendar-clock"
ICON_CLOCK = "mdi:clock-outline"
ICON_TIMER = "mdi:timer"
ICON_COG = "mdi:cog"
ICON_CONNECTION = "mdi:connection"
ICON_DISTANCE = "mdi:map-marker-distance"
ICON_SOLAR_PANEL = "mdi:solar-panel"
ICON_PLAY = "mdi:play-circle"
ICON_STOP = "mdi:stop-circle"

# Error messages
ERROR_AUTH_FAILED = "Authentication failed. Please check your credentials."
ERROR_CANNOT_CONNECT = "Cannot connect to SolarEdge API."
ERROR_INVALID_SITE = "Invalid Site ID or no EV Charger found."
ERROR_UNKNOWN = "Unknown error occurred."
