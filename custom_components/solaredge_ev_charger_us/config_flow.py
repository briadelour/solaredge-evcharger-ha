"""Config flow for SolarEdge EV Charger integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_SITE_ID,
    CONF_COOKIE,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
    CONF_DEVICE_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DEFAULT_NAME,
    API_BASE_URL,
    API_DEVICES_ENDPOINT,
    COOKIE_NAME,
    ERROR_AUTH_FAILED,
    ERROR_CANNOT_CONNECT,
    ERROR_INVALID_SITE,
    ERROR_UNKNOWN,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.
    
    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    site_id = data[CONF_SITE_ID]
    cookie = data[CONF_COOKIE]
    timeout = data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
    
    # Test the API connection
    url = f"{API_BASE_URL}{API_DEVICES_ENDPOINT.format(site_id=site_id)}"
    headers = {
        "Cookie": f"{COOKIE_NAME}={cookie}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                if response.status != 200:
                    raise Exception(ERROR_AUTH_FAILED)
                
                result = await response.json()
                
                # Check for EV charger in response
                if "devicesByType" not in result:
                    raise Exception(ERROR_INVALID_SITE)
                
                if "EV_CHARGER" not in result["devicesByType"]:
                    raise Exception(ERROR_INVALID_SITE)
                
                ev_chargers = result["devicesByType"]["EV_CHARGER"]
                if not ev_chargers or len(ev_chargers) == 0:
                    raise Exception(ERROR_INVALID_SITE)
                
                # Extract device ID (reporterId)
                device_id = ev_chargers[0].get("reporterId")
                if not device_id:
                    raise Exception("Could not find EV Charger device ID")
                
                # Get charger name if available
                charger_name = ev_chargers[0].get("name", DEFAULT_NAME)
                
                return {
                    "title": charger_name,
                    CONF_DEVICE_ID: str(device_id),
                }
                
    except aiohttp.ClientError:
        raise Exception(ERROR_CANNOT_CONNECT)
    except Exception as e:
        if str(e) in [ERROR_AUTH_FAILED, ERROR_INVALID_SITE, ERROR_CANNOT_CONNECT]:
            raise
        _LOGGER.exception("Unexpected error validating credentials")
        raise Exception(ERROR_UNKNOWN)


class SolarEdgeEVChargerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SolarEdge EV Charger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                # Store device_id in user_input
                user_input[CONF_DEVICE_ID] = info[CONF_DEVICE_ID]
                
                # Create unique ID from site_id and device_id
                await self.async_set_unique_id(
                    f"{user_input[CONF_SITE_ID]}_{info[CONF_DEVICE_ID]}"
                )
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )
            except Exception as e:
                error_msg = str(e)
                if ERROR_AUTH_FAILED in error_msg:
                    errors["base"] = "invalid_auth"
                elif ERROR_CANNOT_CONNECT in error_msg:
                    errors["base"] = "cannot_connect"
                elif ERROR_INVALID_SITE in error_msg:
                    errors["base"] = "invalid_site"
                else:
                    errors["base"] = "unknown"
                _LOGGER.error("Error setting up SolarEdge EV Charger: %s", error_msg)
        
        data_schema = vol.Schema(
            {
                vol.Required(CONF_SITE_ID): str,
                vol.Required(CONF_COOKIE): str,
                vol.Optional(CONF_USERNAME): str,
                vol.Optional(CONF_PASSWORD): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                vol.Optional(
                    CONF_TIMEOUT, default=DEFAULT_TIMEOUT
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=120)),
            }
        )
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "site_id_help": "Find this in your SolarEdge monitoring URL",
                "cookie_help": "Extract from browser Developer Tools",
            },
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SolarEdgeEVChargerOptionsFlow:
        """Get the options flow for this handler."""
        return SolarEdgeEVChargerOptionsFlow()


class SolarEdgeEVChargerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for SolarEdge EV Charger."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            # Validate the new cookie if provided
            if CONF_COOKIE in user_input and user_input[CONF_COOKIE]:
                try:
                    # Create test data with new cookie
                    test_data = {
                        CONF_SITE_ID: self.config_entry.data[CONF_SITE_ID],
                        CONF_COOKIE: user_input[CONF_COOKIE],
                        CONF_TIMEOUT: user_input.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
                    }
                    await validate_input(self.hass, test_data)
                    
                    # Update the config entry data with new cookie
                    new_data = {**self.config_entry.data}
                    new_data[CONF_COOKIE] = user_input[CONF_COOKIE]
                    if CONF_SCAN_INTERVAL in user_input:
                        new_data[CONF_SCAN_INTERVAL] = user_input[CONF_SCAN_INTERVAL]
                    if CONF_TIMEOUT in user_input:
                        new_data[CONF_TIMEOUT] = user_input[CONF_TIMEOUT]
                    
                    self.hass.config_entries.async_update_entry(
                        self.config_entry,
                        data=new_data,
                    )
                    
                    return self.async_create_entry(title="", data={})
                    
                except Exception as e:
                    error_msg = str(e)
                    if ERROR_AUTH_FAILED in error_msg:
                        errors["base"] = "invalid_auth"
                    elif ERROR_CANNOT_CONNECT in error_msg:
                        errors["base"] = "cannot_connect"
                    else:
                        errors["base"] = "unknown"
                    _LOGGER.error("Error updating cookie: %s", error_msg)
            else:
                # Just update scan interval and timeout
                new_data = {**self.config_entry.data}
                if CONF_SCAN_INTERVAL in user_input:
                    new_data[CONF_SCAN_INTERVAL] = user_input[CONF_SCAN_INTERVAL]
                if CONF_TIMEOUT in user_input:
                    new_data[CONF_TIMEOUT] = user_input[CONF_TIMEOUT]
                
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=new_data,
                )
                
                return self.async_create_entry(title="", data={})
        
        # Show current values
        current_cookie = self.config_entry.data.get(CONF_COOKIE, "")
        current_scan_interval = self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        current_timeout = self.config_entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
        
        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_COOKIE,
                    description={"suggested_value": current_cookie[:20] + "..." if len(current_cookie) > 20 else current_cookie},
                ): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=current_scan_interval,
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                vol.Optional(
                    CONF_TIMEOUT,
                    default=current_timeout,
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=120)),
            }
        )
        
        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
            description_placeholders={
                "cookie_help": "Leave blank to keep current cookie. Update when expired.",
            },
        )
