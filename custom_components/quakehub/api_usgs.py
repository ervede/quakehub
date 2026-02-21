from __future__ import annotations

import aiohttp
import async_timeout
from datetime import datetime, timezone

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


async def fetch_usgs(session: aiohttp.ClientSession):
    async with async_timeout.timeout(10):
        async with session.get(USGS_URL) as resp:
            resp.raise_for_status()
            data = await resp.json()

    events = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None, None])

        events.append(
            {
                "id": f"usgs_{feature.get('id')}",
                "source": "usgs",
                "time": datetime.fromtimestamp(props.get("time", 0) / 1000, tz=timezone.utc),
                "latitude": coords[1],
                "longitude": coords[0],
                "depth": coords[2],
                "magnitude": props.get("mag"),
                "place": props.get("place"),
                "raw": feature,
            }
        )
    return events
