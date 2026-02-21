from __future__ import annotations

import aiohttp
import async_timeout
from datetime import datetime, timezone

GEOFON_URL = "https://geofon.gfz-potsdam.de/eqinfo/list.json"


async def fetch_geofon(session: aiohttp.ClientSession):
    async with async_timeout.timeout(10):
        async with session.get(GEOFON_URL) as resp:
            resp.raise_for_status()
            data = await resp.json()

    events = []
    # GEOFON may return list or GeoJSON-like structure
    items = data.get("features", data if isinstance(data, list) else [])
    for item in items:
        props = item.get("properties", item)
        geom = item.get("geometry", {})
        coords = geom.get("coordinates", [props.get("lon"), props.get("lat"), props.get("depth")])

        time_val = props.get("time") or props.get("origintime")
        if isinstance(time_val, str):
            try:
                dt = datetime.fromisoformat(time_val.replace("Z", "+00:00"))
            except Exception:
                dt = datetime.now(timezone.utc)
        else:
            dt = datetime.now(timezone.utc)

        events.append(
            {
                "id": f"geofon_{props.get('eventid') or props.get('id')}",
                "source": "geofon",
                "time": dt,
                "latitude": coords[1],
                "longitude": coords[0],
                "depth": coords[2],
                "magnitude": props.get("mag"),
                "place": props.get("region") or props.get("flynn_region"),
                "raw": item,
            }
        )
    return events
