# 🌍 QuakeHub  
### **Global Earthquake Intelligence for Home Assistant**

QuakeHub unifies real‑time seismic data from **USGS**, **EMSC**, and **GEOFON** into a single, deduplicated, high‑accuracy earthquake feed for Home Assistant.

It delivers **global coverage**, **European precision**, and **multi‑source redundancy**, all through a clean, intuitive UI‑based setup.

---

# ⚠️ Disclaimer

QuakeHub aggregates publicly available earthquake information from external providers, including **USGS**, **EMSC**, and **GEOFON**. These data sources operate independently of this project, and their accuracy, availability, and timeliness are outside the control of the QuakeHub maintainers.

By using QuakeHub, you acknowledge and agree that:

- The project **does not provide emergency alerts**, early‑warning capabilities, or safety‑critical notifications.  
- The project maintainer(s) and contributors **are not responsible or liable** for any decisions, actions, damages, or consequences resulting from the use of this integration or the data it displays.  
- Earthquake information may be **delayed, incomplete, revised, duplicated, or inaccurate**, depending on upstream providers.  
- QuakeHub is intended **for informational and hobbyist use only** and must not be relied upon for personal safety, disaster response, or risk assessment.  

For authoritative seismic alerts or emergency notifications, consult your local government, civil protection agency, or official early‑warning systems.

---

# ✨ Features

- **Multi‑source aggregation**  
  Combines USGS, EMSC, and GEOFON into one unified feed.

- **Smart deduplication engine**  
  Merges identical events across sources using time, distance, and magnitude heuristics.

- **GeoLocation entities**  
  Earthquakes appear on the Home Assistant map with detailed attributes.

- **Powerful sensors**  
  - Latest earthquake  
  - Strongest earthquake (24h)  
  - Earthquake count (24h)

- **Flexible filtering**  
  - Radius‑based filtering  
  - Region‑based filtering  
  - Source enable/disable toggles

- **Full UI configuration**  
  No YAML required — everything is configured through the HA Integrations UI.

- **HACS compatible**  
  Easy installation and automatic updates.

---

# 📦 Installation

## HACS (Recommended)

1. Open **HACS → Integrations**  
2. Click **⋮ → Custom repositories**  
3. Add:  
   ```
   https://github.com/ervede/quakehub
   ```  
4. Category: **Integration**  
5. Install **QuakeHub**  
6. Restart Home Assistant  
7. Go to **Settings → Devices & Services → Add Integration → QuakeHub**

---

## Manual Installation

1. Download the latest release from GitHub  
2. Extract the folder  
3. Copy `custom_components/quakehub/` into:  
   ```
   /config/custom_components/
   ```
4. Restart Home Assistant  
5. Add the integration via the UI

---

# ⚙️ Configuration

QuakeHub is configured entirely through the Home Assistant UI.

### Setup Options

- **Home location**  
  Auto‑detected from HA, with optional override.

- **Filtering mode**  
  - Radius (km)  
  - Region (country/area)

- **Enabled data sources**  
  - USGS  
  - EMSC  
  - GEOFON

- **Update interval**  
  How often QuakeHub polls for new events.

---

# 🗺️ Entities

## GeoLocation Entities
Each earthquake appears as a map entity with:

- Magnitude  
- Depth  
- Distance from home  
- Primary source  
- Combined sources  
- Region  
- Timestamp  

## Sensors

| Sensor | Description |
|--------|-------------|
| **Latest Earthquake** | Magnitude of the most recent quake |
| **Strongest Earthquake (24h)** | Highest magnitude in last 24 hours |
| **Earthquake Count (24h)** | Number of quakes detected in last 24 hours |

---

# 🧠 How QuakeHub Works

QuakeHub fetches data from:

- **USGS GeoJSON feed**  
- **EMSC FDSN GeoJSON feed**  
- **GEOFON JSON feed**

Then it:

1. Normalizes all events  
2. Deduplicates overlapping events  
3. Prioritizes the most accurate source  
4. Filters by radius or region  
5. Exposes events as HA entities  

This gives you **global coverage with local accuracy**.

---


# 🧪 Contributing

Pull requests are welcome.  
Please follow **Conventional Commits** for automated versioning.

Examples:

- `feat: add new sensor`
- `fix: correct EMSC timestamp`
- `chore: update dependencies`

---

# 📜 License

QuakeHub is released under the **MIT License**.
---
