"""Button platform for SolarEdge EV Charger."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ICON_PLAY,
    ICON_STOP,
)
from .coordinator import SolarEdgeEVChargerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SolarEdge EV Charger buttons."""
    coordinator: SolarEdgeEVChargerCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    buttons = [
        EVChargerStartChargingButton(coordinator, entry),
        EVChargerStopChargingButton(coordinator, entry),
    ]
    
    async_add_entities(buttons)


class SolarEdgeEVChargerButtonBase(CoordinatorEntity, ButtonEntity):
    """Base class for SolarEdge EV Charger buttons."""

    def __init__(
        self,
        coordinator: SolarEdgeEVChargerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "name": "SolarEdge EV Charger",
            "manufacturer": "SolarEdge",
            "model": "EV Charger",
        }


class EVChargerStartChargingButton(SolarEdgeEVChargerButtonBase):
    """EV Charger Start Charging button."""

    _attr_name = "EV Charger Start Charging"
    _attr_unique_id = "solaredge_ev_charger_start_charging"
    _attr_icon = ICON_PLAY

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Starting EV charging")
        success = await self.coordinator.async_start_charging()
        if not success:
            _LOGGER.error("Failed to start charging")


class EVChargerStopChargingButton(SolarEdgeEVChargerButtonBase):
    """EV Charger Stop Charging button."""

    _attr_name = "EV Charger Stop Charging"
    _attr_unique_id = "solaredge_ev_charger_stop_charging"
    _attr_icon = ICON_STOP

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Stopping EV charging")
        success = await self.coordinator.async_stop_charging()
        if not success:
            _LOGGER.error("Failed to stop charging")
