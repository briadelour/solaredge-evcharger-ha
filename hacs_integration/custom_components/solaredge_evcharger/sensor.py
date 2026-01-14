"""Sensor platform for SolarEdge EV Charger."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfLength,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CHARGER_STATUS_CHARGING,
    CHARGER_STATUS_PLUGGED_IN,
    CHARGER_STATUS_NOT_CONNECTED,
    EXCESS_PV_ENABLED,
    EXCESS_PV_DISABLED,
    ICON_EV_STATION,
    ICON_EV_PLUG,
    ICON_CAR,
    ICON_SOLAR,
    ICON_SOLAR_VARIANT,
    ICON_SOLAR_PANEL,
    ICON_CALENDAR,
    ICON_CLOCK,
    ICON_TIMER,
    ICON_COG,
    ICON_CONNECTION,
    ICON_DISTANCE,
)
from .coordinator import SolarEdgeEVChargerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SolarEdge EV Charger sensors."""
    coordinator: SolarEdgeEVChargerCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        EVChargerStatusSensor(coordinator, entry),
        EVChargerPowerSensor(coordinator, entry),
        EVSessionEnergySensor(coordinator, entry),
        EVSessionDurationSensor(coordinator, entry),
        EVConnectedVehicleSensor(coordinator, entry),
        EVChargerModeSensor(coordinator, entry),
        EVConnectionStatusSensor(coordinator, entry),
        EVSessionDistanceSensor(coordinator, entry),
        EVSessionDistanceMilesSensor(coordinator, entry),
        EVExcessSolarStatusSensor(coordinator, entry),
        EVSessionSolarUsageSensor(coordinator, entry),
        EVChargingSchedulesSensor(coordinator, entry),
        EVNextScheduledChargeSensor(coordinator, entry),
    ]
    
    async_add_entities(sensors)


class SolarEdgeEVChargerSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for SolarEdge EV Charger sensors."""

    def __init__(
        self,
        coordinator: SolarEdgeEVChargerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
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


class EVChargerStatusSensor(SolarEdgeEVChargerSensorBase):
    """EV Charger Status sensor."""

    _attr_name = "EV Charger Status"
    _attr_unique_id = "solaredge_ev_charger_status"

    @property
    def native_value(self) -> str:
        """Return the state."""
        status = self.charger_data.get("chargerStatus", "")
        if status == CHARGER_STATUS_CHARGING:
            return "Charging"
        elif status == CHARGER_STATUS_PLUGGED_IN:
            return "Plugged In"
        elif status == CHARGER_STATUS_NOT_CONNECTED:
            return "Not Connected"
        return status

    @property
    def icon(self) -> str:
        """Return the icon."""
        status = self.charger_data.get("chargerStatus", "")
        if status == CHARGER_STATUS_CHARGING:
            return ICON_EV_STATION
        return ICON_EV_PLUG


class EVChargerPowerSensor(SolarEdgeEVChargerSensorBase):
    """EV Charger Power sensor."""

    _attr_name = "EV Charger Power"
    _attr_unique_id = "solaredge_ev_charger_power"
    _attr_native_unit_of_measurement = "kW"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float:
        """Return the power in kW."""
        if self.charger_data.get("chargerStatus") == CHARGER_STATUS_CHARGING:
            subtitles = self.charger_data.get("chargerStatusSubTitle", [])
            if subtitles and len(subtitles) > 0:
                numeric_value = subtitles[0].get("numericValue", 0)
                return round(numeric_value / 1000, 2)
        return 0.0


class EVSessionEnergySensor(SolarEdgeEVChargerSensorBase):
    """EV Session Energy sensor."""

    _attr_name = "EV Session Energy"
    _attr_unique_id = "solaredge_ev_session_energy"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self) -> float:
        """Return the session energy."""
        if self.charger_data.get("sessionActive"):
            session_energy = self.charger_data.get("sessionEnergy", 0)
            return round(session_energy / 1000, 2)
        return 0.0


class EVSessionDurationSensor(SolarEdgeEVChargerSensorBase):
    """EV Session Duration sensor."""

    _attr_name = "EV Session Duration"
    _attr_unique_id = "solaredge_ev_session_duration"
    _attr_icon = ICON_TIMER

    @property
    def native_value(self) -> str:
        """Return the session duration."""
        if self.charger_data.get("sessionActive"):
            duration_seconds = self.charger_data.get("sessionDuration", 0)
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        return "0m"


class EVConnectedVehicleSensor(SolarEdgeEVChargerSensorBase):
    """EV Connected Vehicle sensor."""

    _attr_name = "EV Connected Vehicle"
    _attr_unique_id = "solaredge_ev_connected_vehicle"
    _attr_icon = ICON_CAR

    @property
    def native_value(self) -> str:
        """Return the connected vehicle name."""
        appliance_data = self.charger_data.get("applianceData", {})
        return appliance_data.get("alias", "Unknown")


class EVChargerModeSensor(SolarEdgeEVChargerSensorBase):
    """EV Charger Mode sensor."""

    _attr_name = "EV Charger Mode"
    _attr_unique_id = "solaredge_ev_charger_mode"
    _attr_icon = ICON_COG

    @property
    def native_value(self) -> str:
        """Return the charger mode."""
        mode = self.charger_data.get("activationMode", "")
        return mode.title()


class EVConnectionStatusSensor(SolarEdgeEVChargerSensorBase):
    """EV Connection Status sensor."""

    _attr_name = "EV Connection Status"
    _attr_unique_id = "solaredge_ev_connection_status"
    _attr_icon = ICON_CONNECTION

    @property
    def native_value(self) -> str:
        """Return the connection status."""
        status = self.charger_data.get("connectionStatus", "")
        return status.replace("_", " ").title()


class EVSessionDistanceSensor(SolarEdgeEVChargerSensorBase):
    """EV Session Distance sensor (km)."""

    _attr_name = "EV Session Distance"
    _attr_unique_id = "solaredge_ev_session_distance"
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS
    _attr_icon = ICON_DISTANCE

    @property
    def native_value(self) -> float:
        """Return the session distance in km."""
        if self.charger_data.get("sessionActive"):
            distance = self.charger_data.get("sessionDistance", 0)
            return round(distance, 1)
        return 0.0


class EVSessionDistanceMilesSensor(SolarEdgeEVChargerSensorBase):
    """EV Session Distance sensor (miles)."""

    _attr_name = "EV Session Distance (Miles)"
    _attr_unique_id = "solaredge_ev_session_distance_mi"
    _attr_native_unit_of_measurement = UnitOfLength.MILES
    _attr_icon = ICON_DISTANCE

    @property
    def native_value(self) -> float:
        """Return the session distance in miles."""
        if self.charger_data.get("sessionActive"):
            distance_km = self.charger_data.get("sessionDistance", 0)
            return round(distance_km * 0.621371, 1)
        return 0.0


class EVExcessSolarStatusSensor(SolarEdgeEVChargerSensorBase):
    """EV Excess Solar Status sensor."""

    _attr_name = "EV Excess Solar Status"
    _attr_unique_id = "solaredge_ev_excess_solar_status"

    @property
    def native_value(self) -> str:
        """Return the excess solar status."""
        excess_pv = self.charger_data.get("excessPV")
        if excess_pv == EXCESS_PV_ENABLED:
            return "Enabled"
        elif excess_pv == EXCESS_PV_DISABLED:
            return "Disabled"
        return "Unknown"

    @property
    def icon(self) -> str:
        """Return the icon."""
        excess_pv = self.charger_data.get("excessPV")
        if excess_pv == EXCESS_PV_ENABLED:
            return ICON_SOLAR
        return ICON_SOLAR_VARIANT


class EVSessionSolarUsageSensor(SolarEdgeEVChargerSensorBase):
    """EV Session Solar Usage sensor."""

    _attr_name = "EV Session Solar Usage"
    _attr_unique_id = "solaredge_ev_session_solar_usage"
    _attr_icon = ICON_SOLAR_PANEL

    @property
    def native_value(self) -> str:
        """Return the session solar usage."""
        excess_pv = self.charger_data.get("excessPV")
        if excess_pv == EXCESS_PV_ENABLED:
            solar_usage = self.charger_data.get("sessionSolarUsage", "NONE")
            if solar_usage != "NONE":
                return solar_usage.replace("_", " ").title()
            return "No Solar Usage"
        return "Excess Solar Disabled"


class EVChargingSchedulesSensor(SolarEdgeEVChargerSensorBase):
    """EV Charging Schedules sensor."""

    _attr_name = "EV Charging Schedules"
    _attr_unique_id = "solaredge_ev_charging_schedules"
    _attr_icon = ICON_CALENDAR

    @property
    def native_value(self) -> str:
        """Return the number of active schedules."""
        triggers = self.charger_data.get("deviceTriggers", [])
        enabled_schedules = [t for t in triggers if t.get("enable")]
        count = len(enabled_schedules)
        if count > 0:
            return f"{count} Schedule(s) Active"
        return "No Schedules"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the schedules as attributes."""
        triggers = self.charger_data.get("deviceTriggers", [])
        enabled_schedules = [t for t in triggers if t.get("enable")]
        
        schedule_list = []
        for schedule in enabled_schedules:
            start_time = schedule.get("startTime", 0)
            end_time = schedule.get("endTime", 0)
            start_hour = start_time // 60
            start_min = start_time % 60
            end_hour = end_time // 60
            end_min = end_time % 60
            
            time_range = f"{start_hour:02d}:{start_min:02d} - {end_hour:02d}:{end_min:02d}"
            
            days_abbrev = []
            scheduled_days = schedule.get("scheduledDays", [])
            day_map = {
                "MONDAY": "Mon",
                "TUESDAY": "Tue",
                "WEDNESDAY": "Wed",
                "THURSDAY": "Thu",
                "FRIDAY": "Fri",
                "SATURDAY": "Sat",
                "SUNDAY": "Sun",
            }
            for day in scheduled_days:
                if day in day_map:
                    days_abbrev.append(day_map[day])
            
            days_str = ", ".join(days_abbrev)
            schedule_list.append(f"{time_range} ({days_str})")
        
        return {"schedules": schedule_list}


class EVNextScheduledChargeSensor(SolarEdgeEVChargerSensorBase):
    """EV Next Scheduled Charge sensor."""

    _attr_name = "EV Next Scheduled Charge"
    _attr_unique_id = "solaredge_ev_next_scheduled_charge"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = ICON_CLOCK

    @property
    def native_value(self) -> datetime | None:
        """Return the next scheduled charge time."""
        triggers = self.charger_data.get("deviceTriggers", [])
        enabled_schedules = [t for t in triggers if t.get("enable")]
        
        if not enabled_schedules:
            return None
        
        if self.charger_data.get("chargerStatus") == CHARGER_STATUS_CHARGING:
            return None
        
        # Check if scheduleInfo provides the next start date
        schedule_info = self.charger_data.get("scheduleInfo", {})
        if "startDate" in schedule_info:
            start_date_ms = schedule_info["startDate"]
            return dt_util.utc_from_timestamp(start_date_ms / 1000)
        
        # Calculate next scheduled charge time
        now = dt_util.now()
        current_day = now.weekday()
        current_time_minutes = now.hour * 60 + now.minute
        
        day_map = {
            "MONDAY": 0,
            "TUESDAY": 1,
            "WEDNESDAY": 2,
            "THURSDAY": 3,
            "FRIDAY": 4,
            "SATURDAY": 5,
            "SUNDAY": 6,
        }
        
        next_schedule_time = None
        min_days_ahead = 999
        
        for schedule in enabled_schedules:
            scheduled_days = schedule.get("scheduledDays", [])
            start_time = schedule.get("startTime", 0)
            
            for day_name in scheduled_days:
                if day_name not in day_map:
                    continue
                
                schedule_day = day_map[day_name]
                days_until = (schedule_day - current_day) % 7
                
                # If it's today, check if time has passed
                if days_until == 0 and start_time <= current_time_minutes:
                    days_until = 7
                
                # Find the closest schedule
                if days_until < min_days_ahead or (
                    days_until == min_days_ahead
                    and (next_schedule_time is None or start_time < next_schedule_time)
                ):
                    min_days_ahead = days_until
                    next_schedule_time = start_time
        
        if next_schedule_time is not None:
            next_date = now + timedelta(days=min_days_ahead)
            next_hour = next_schedule_time // 60
            next_min = next_schedule_time % 60
            return next_date.replace(
                hour=next_hour, minute=next_min, second=0, microsecond=0
            )
        
        return None
