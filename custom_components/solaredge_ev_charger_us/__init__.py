"""The SolarEdge EV Charger integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_SITE_ID,
    CONF_COOKIE,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
    CONF_DEVICE_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
)
from .coordinator import SolarEdgeEVChargerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SolarEdge EV Charger from a config entry."""
    
    site_id = entry.data[CONF_SITE_ID]
    cookie = entry.data[CONF_COOKIE]
    device_id = entry.data.get(CONF_DEVICE_ID)
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    timeout = entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
    
    coordinator = SolarEdgeEVChargerCoordinator(
        hass,
        site_id=site_id,
        cookie=cookie,
        device_id=device_id,
        scan_interval=scan_interval,
        timeout=timeout,
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
