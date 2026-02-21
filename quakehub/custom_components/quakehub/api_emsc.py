from __future__ import annotations

import aiohttp
import async_timeout
from datetime import datetime, timezone

EMSC_URL = "https://www.seismicportal.eu/fdsnws/event/1/query?format=geojson&limit=200"


async def fetch_emsc(session: aiohttp.ClientSession):
    async with async_timeout.timeout(10):
        async with session.get(EMSC_URL) as resp:
            resp.raise_for_status()
            data = await resp.json()

    events = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None, None])

        time_val = props.get("time")
        if isinstance(time_val, (int, float)):
            dt = datetime.fromtimestamp(time_val / 1000, tz=timezone.utc)
        else:
            dt = datetime.now(timezone.utc)

        events.append(
            {
                "id": f"emsc_{props.get('eventid') or feature.get('id')}",
                "source": "emsc",
                "time": dt,
                "latitude": coords[1],
                "longitude": coords[0],
                "depth": coords[2],
                "magnitude": props.get("mag"),
                "place": props.get("flynn_region") or props.get("region"),
                "felt_reports": props.get("felt"),
                "raw": feature,
            }
        )
    return events
