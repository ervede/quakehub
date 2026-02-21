from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_RADIUS,
    CONF_REGION_MODE,
    CONF_REGION,
    CONF_SOURCES,
    CONF_UPDATE_INTERVAL,
    DEFAULT_RADIUS,
    DEFAULT_SOURCES,
    DEFAULT_UPDATE_INTERVAL,
    REGION_MODE_RADIUS,
    REGION_MODE_REGION,
    SOURCE_USGS,
    SOURCE_EMSC,
    SOURCE_GEOFON,
)


def _get_default_location(hass):
    return hass.config.latitude, hass.config.longitude


class QuakeHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "QuakeHub"),
                data=user_input,
            )

        lat, lon = _get_default_location(self.hass)

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="QuakeHub"): str,
                vol.Required(CONF_LATITUDE, default=lat): float,
                vol.Required(CONF_LONGITUDE, default=lon): float,
                vol.Required(CONF_REGION_MODE, default=REGION_MODE_RADIUS): vol.In(
                    [REGION_MODE_RADIUS, REGION_MODE_REGION]
                ),
                vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): int,
                vol.Optional(CONF_REGION, default=""): str,
                vol.Optional(CONF_SOURCES, default=DEFAULT_SOURCES): vol.All(
                    [vol.In([SOURCE_USGS, SOURCE_EMSC, SOURCE_GEOFON])]
                ),
                vol.Optional(
                    CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                ): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)
