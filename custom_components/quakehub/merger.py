from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from typing import List, Dict, Any


@dataclass
class EarthquakeEvent:
    id: str
    source: str
    time: datetime
    latitude: float
    longitude: float
    depth: float | None
    magnitude: float | None
    place: str | None
    extra: Dict[str, Any]


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def normalize_events(raw_events: List[Dict[str, Any]]) -> List[EarthquakeEvent]:
    events: List[EarthquakeEvent] = []
    for e in raw_events:
        events.append(
            EarthquakeEvent(
                id=e["id"],
                source=e["source"],
                time=e["time"],
                latitude=e["latitude"],
                longitude=e["longitude"],
                depth=e.get("depth"),
                magnitude=e.get("magnitude"),
                place=e.get("place"),
                extra={
                    k: v
                    for k, v in e.items()
                    if k
                    not in {
                        "id",
                        "source",
                        "time",
                        "latitude",
                        "longitude",
                        "depth",
                        "magnitude",
                        "place",
                    }
                },
            )
        )
    return events


def merge_events(events: List[EarthquakeEvent]) -> List[EarthquakeEvent]:
    merged: List[EarthquakeEvent] = []

    for event in events:
        matched = None
        for existing in merged:
            if abs((event.time - existing.time).total_seconds()) > 60:
                continue
            if haversine_km(
                event.latitude, event.longitude, existing.latitude, existing.longitude
            ) > 10:
                continue
            if (
                event.magnitude is not None
                and existing.magnitude is not None
                and abs(event.magnitude - existing.magnitude) > 0.3
            ):
                continue
            matched = existing
            break

        if matched is None:
            merged.append(event)
        else:
            priority = {"emsc": 3, "usgs": 2, "geofon": 1}
            if priority.get(event.source, 0) > priority.get(matched.source, 0):
                merged.remove(matched)
                merged.append(event)
            else:
                matched.extra.setdefault("sources", set())
                matched.extra["sources"].add(event.source)

    for e in merged:
        if "sources" in e.extra and isinstance(e.extra["sources"], set):
            e.extra["sources"] = list(e.extra["sources"])

    return merged
