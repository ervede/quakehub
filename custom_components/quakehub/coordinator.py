from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_REGION_MODE,
    REGION_MODE_RADIUS,
    CONF_SOURCES,
    SOURCE_USGS,
    SOURCE_EMSC,
    SOURCE_GEOFON,
)
from .api_usgs import fetch_usgs
from .api_emsc import fetch_emsc
from .api_geofon import fetch_geofon
from .merger import normalize_events, merge_events, haversine_km

_LOGGER = logging.getLogger(__name__)


class EarthquakeCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator",
            update_interval=update_interval,
        )
        self.entry = entry
        self.lat = entry.data[CONF_LATITUDE]
        self.lon = entry.data[CONF_LONGITUDE]
        self.radius = entry.data.get(CONF_RADIUS)
        self.region_mode = entry.data.get(CONF_REGION_MODE, REGION_MODE_RADIUS)
        self.sources = entry.data.get(CONF_SOURCES, [])

    async def _async_update_data(self):
        async with aiohttp.ClientSession() as session:
            raw_events = []

            if SOURCE_USGS in self.sources:
                try:
                    raw_events.extend(await fetch_usgs(session))
                except Exception as err:
                    _LOGGER.warning("USGS fetch failed: %s", err)

            if SOURCE_EMSC in self.sources:
                try:
                    raw_events.extend(await fetch_emsc(session))
                except Exception as err:
                    _LOGGER.warning("EMSC fetch failed: %s", err)

            if SOURCE_GEOFON in self.sources:
                try:
                    raw_events.extend(await fetch_geofon(session))
                except Exception as err:
                    _LOGGER.warning("GEOFON fetch failed: %s", err)

        events = normalize_events(raw_events)
        events = merge_events(events)

        if self.region_mode == REGION_MODE_RADIUS and self.radius:
            events = [
                e
                for e in events
                if haversine_km(self.lat, self.lon, e.latitude, e.longitude)
                <= self.radius
            ]

        events.sort(key=lambda e: e.time, reverse=True)
        return events
