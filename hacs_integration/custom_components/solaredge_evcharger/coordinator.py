"""Data update coordinator for SolarEdge EV Charger."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    API_BASE_URL,
    API_DEVICES_ENDPOINT,
    API_CONTROL_ENDPOINT,
    COOKIE_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


class SolarEdgeEVChargerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching SolarEdge EV Charger data."""

    def __init__(
        self,
        hass: HomeAssistant,
        site_id: str,
        cookie: str,
        device_id: str | None = None,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the coordinator."""
        self.site_id = site_id
        self.cookie = cookie
        self.device_id = device_id
        self.timeout = timeout
        self._session = None
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(self.timeout):
                return await self._fetch_data()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")

    async def _fetch_data(self) -> dict[str, Any]:
        """Fetch data from SolarEdge API."""
        url = f"{API_BASE_URL}{API_DEVICES_ENDPOINT.format(site_id=self.site_id)}"
        headers = {
            "Cookie": f"{COOKIE_NAME}={self.cookie}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
        
        if self._session is None:
            self._session = aiohttp.ClientSession()
        
        async with self._session.get(url, headers=headers) as response:
            if response.status != 200:
                raise UpdateFailed(f"API returned status {response.status}")
            
            data = await response.json()
            
            # Validate data structure
            if "devicesByType" not in data:
                raise UpdateFailed("Invalid API response: missing devicesByType")
            
            if "EV_CHARGER" not in data["devicesByType"]:
                raise UpdateFailed("No EV Charger found in API response")
            
            ev_chargers = data["devicesByType"]["EV_CHARGER"]
            if not ev_chargers or len(ev_chargers) == 0:
                raise UpdateFailed("No EV Charger data available")
            
            # Store device_id if not already set
            if not self.device_id:
                self.device_id = str(ev_chargers[0].get("reporterId"))
            
            return ev_chargers[0]

    async def async_start_charging(self) -> bool:
        """Start charging the EV."""
        return await self._set_charging_state(100)

    async def async_stop_charging(self) -> bool:
        """Stop charging the EV."""
        return await self._set_charging_state(0)

    async def _set_charging_state(self, level: int) -> bool:
        """Set the charging state."""
        if not self.device_id:
            _LOGGER.error("Device ID not available")
            return False
        
        url = f"{API_BASE_URL}{API_CONTROL_ENDPOINT.format(site_id=self.site_id, device_id=self.device_id)}"
        headers = {
            "Cookie": f"{COOKIE_NAME}={self.cookie}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
        payload = {
            "mode": "MANUAL",
            "level": level,
            "duration": None,
        }
        
        try:
            if self._session is None:
                self._session = aiohttp.ClientSession()
            
            async with async_timeout.timeout(self.timeout):
                async with self._session.put(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        _LOGGER.error("Failed to set charging state: %s", response.status)
                        return False
                    
                    result = await response.json()
                    if result.get("status") == "PASSED":
                        # Request immediate refresh
                        await self.async_request_refresh()
                        return True
                    
                    _LOGGER.error("API returned error: %s", result)
                    return False
        except Exception as err:
            _LOGGER.error("Error setting charging state: %s", err)
            return False

    async def async_shutdown(self) -> None:
        """Close the session."""
        if self._session:
            await self._session.close()
            self._session = None
