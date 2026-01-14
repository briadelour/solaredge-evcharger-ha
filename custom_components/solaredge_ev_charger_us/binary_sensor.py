"""Binary sensor platform for SolarEdge EV Charger."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CHARGER_STATUS_CHARGING,
    CONNECTION_STATUS_CHARGING,
    CONNECTION_STATUS_CONNECTED,
    EXCESS_PV_ENABLED,
    ICON_CALENDAR,
    ICON_SOLAR,
)
from .coordinator import SolarEdgeEVChargerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SolarEdge EV Charger binary sensors."""
    coordinator: SolarEdgeEVChargerCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        EVChargerConnectedSensor(coordinator, entry),
        EVChargerChargingSensor(coordinator, entry),
        EVChargeScheduleEnabledSensor(coordinator, entry),
        EVExcessSolarEnabledSensor(coordinator, entry),
    ]
    
    async_add_entities(sensors)


class SolarEdgeEVChargerBinarySensorBase(CoordinatorEntity, BinarySensorEntity):
    """Base class for SolarEdge EV Charger binary sensors."""

    def __init__(
        self,
        coordinator: SolarEdgeEVChargerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "name": "SolarEdge EV Charger",
            "manufacturer": "SolarEdge",
            "model": "EV Charger",
        }

    @property
    def charger_data(self) -> dict[str, Any]:
        """Return the charger data."""
        return self.coordinator.data if self.coordinator.data else {}


class EVChargerConnectedSensor(SolarEdgeEVChargerBinarySensorBase):
    """EV Charger Connected binary sensor."""

    _attr_name = "EV Charger Connected"
    _attr_unique_id = "solaredge_ev_charger_connected"
    _attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self) -> bool:
        """Return true if vehicle is connected."""
        connection_status = self.charger_data.get("connectionStatus", "")
        return connection_status in [CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_CHARGING]


class EVChargerChargingSensor(SolarEdgeEVChargerBinarySensorBase):
    """EV Charger Charging binary sensor."""

    _attr_name = "EV Charger Charging"
    _attr_unique_id = "solaredge_ev_charger_charging"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self) -> bool:
        """Return true if currently charging."""
        return self.charger_data.get("chargerStatus") == CHARGER_STATUS_CHARGING


class EVChargeScheduleEnabledSensor(SolarEdgeEVChargerBinarySensorBase):
    """EV Charge Schedule Enabled binary sensor."""

    _attr_name = "EV Charge Schedule Enabled"
    _attr_unique_id = "solaredge_ev_charge_schedule_enabled"
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = ICON_CALENDAR

    @property
    def is_on(self) -> bool:
        """Return true if any schedule is enabled."""
        triggers = self.charger_data.get("deviceTriggers", [])
        enabled_schedules = [t for t in triggers if t.get("enable")]
        return len(enabled_schedules) > 0


class EVExcessSolarEnabledSensor(SolarEdgeEVChargerBinarySensorBase):
    """EV Excess Solar Enabled binary sensor."""

    _attr_name = "EV Excess Solar Enabled"
    _attr_unique_id = "solaredge_ev_excess_solar_enabled"
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = ICON_SOLAR

    @property
    def is_on(self) -> bool:
        """Return true if excess solar is enabled."""
        return self.charger_data.get("excessPV") == EXCESS_PV_ENABLED
