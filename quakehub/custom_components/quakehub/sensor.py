from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EarthquakeCoordinator
from .merger import EarthquakeEvent


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EarthquakeCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = [
        LatestEarthquakeSensor(coordinator, entry),
        StrongestEarthquake24hSensor(coordinator, entry),
        CountEarthquakes24hSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class BaseQuakeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: EarthquakeCoordinator, entry: ConfigEntry):
        super().__init__(coordinator)
        self._entry = entry

    @property
    def should_poll(self) -> bool:
        return False


class LatestEarthquakeSensor(BaseQuakeSensor):
    _attr_icon = "mdi:earthquake"

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self._entry.entry_id}_latest"

    @property
    def name(self) -> str:
        return "QuakeHub Latest Earthquake"

    @property
    def native_value(self) -> float | None:
        events: list[EarthquakeEvent] = self.coordinator.data or []
        if not events:
            return None
        return events[0].magnitude

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        events: list[EarthquakeEvent] = self.coordinator.data or []
        if not events:
            return {}
        e = events[0]
        return {
            "time": e.time.isoformat(),
            "place": e.place,
            "source": e.source,
            "latitude": e.latitude,
            "longitude": e.longitude,
            "depth": e.depth,
        }


class StrongestEarthquake24hSensor(BaseQuakeSensor):
    _attr_icon = "mdi:earthquake"

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self._entry.entry_id}_strongest_24h"

    @property
    def name(self) -> str:
        return "QuakeHub Strongest (24h)"

    @property
    def native_value(self) -> float | None:
        events: list[EarthquakeEvent] = self.coordinator.data or []
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent = [e for e in events if e.time.replace(tzinfo=None) >= cutoff]
        if not recent:
            return None
        return max((e.magnitude or 0 for e in recent), default=None)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        events: list[EarthquakeEvent] = self.coordinator.data or []
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent = [e for e in events if e.time.replace(tzinfo=None) >= cutoff]
        if not recent:
            return {}
        strongest = max(recent, key=lambda e: e.magnitude or 0)
        return {
            "time": strongest.time.isoformat(),
            "place": strongest.place,
            "source": strongest.source,
            "latitude": strongest.latitude,
            "longitude": strongest.longitude,
            "depth": strongest.depth,
        }


class CountEarthquakes24hSensor(BaseQuakeSensor):
    _attr_icon = "mdi:counter"

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self._entry.entry_id}_count_24h"

    @property
    def name(self) -> str:
        return "QuakeHub Count (24h)"

    @property
    def native_value(self) -> int:
        events: list[EarthquakeEvent] = self.coordinator.data or []
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent = [e for e in events if e.time.replace(tzinfo=None) >= cutoff]
        return len(recent)
