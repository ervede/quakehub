from __future__ import annotations

from typing import Any

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EarthquakeCoordinator
from .merger import EarthquakeEvent, haversine_km


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EarthquakeCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[EarthquakeGeoEntity] = []

    for event in coordinator.data:
        entities.append(EarthquakeGeoEntity(coordinator, event))

    async_add_entities(entities)

    def _update_entities():
        existing_ids = {e.unique_id for e in entities}
        new_entities: list[EarthquakeGeoEntity] = []
        for event in coordinator.data:
            uid = f"{DOMAIN}_{event.id}"
            if uid not in existing_ids:
                new_entities.append(EarthquakeGeoEntity(coordinator, event))
        if new_entities:
            async_add_entities(new_entities)

    coordinator.async_add_listener(_update_entities)


class EarthquakeGeoEntity(CoordinatorEntity, GeolocationEvent):
    _attr_icon = "mdi:earthquake"

    def __init__(self, coordinator: EarthquakeCoordinator, event: EarthquakeEvent):
        super().__init__(coordinator)
        self._event = event
        self._attr_unique_id = f"{DOMAIN}_{event.id}"
        self._attr_name = f"Quake {event.magnitude or '?'} {event.place or ''}".strip()

    @property
    def latitude(self) -> float:
        return self._event.latitude

    @property
    def longitude(self) -> float:
        return self._event.longitude

    @property
    def source(self) -> str:
        return DOMAIN

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        coord: EarthquakeCoordinator = self.coordinator
        distance = haversine_km(
            coord.lat, coord.lon, self._event.latitude, self._event.longitude
        )
        return {
            "magnitude": self._event.magnitude,
            "depth": self._event.depth,
            "time": self._event.time.isoformat(),
            "place": self._event.place,
            "source_primary": self._event.source,
            "sources_combined": self._event.extra.get("sources"),
            "distance_km": round(distance, 1),
        }

    @property
    def state(self) -> float:
        coord: EarthquakeCoordinator = self.coordinator
        return round(
            haversine_km(
                coord.lat, coord.lon, self._event.latitude, self._event.longitude
            ),
            1,
        )

    @property
    def should_poll(self) -> bool:
        return False
