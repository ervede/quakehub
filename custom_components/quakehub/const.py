DOMAIN = "quakehub"

CONF_RADIUS = "radius"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_REGION_MODE = "region_mode"
CONF_REGION = "region"
CONF_SOURCES = "sources"
CONF_UPDATE_INTERVAL = "update_interval"

SOURCE_USGS = "usgs"
SOURCE_EMSC = "emsc"
SOURCE_GEOFON = "geofon"

DEFAULT_RADIUS = 300
DEFAULT_UPDATE_INTERVAL = 300  # seconds
DEFAULT_SOURCES = [SOURCE_USGS, SOURCE_EMSC, SOURCE_GEOFON]

REGION_MODE_RADIUS = "radius"
REGION_MODE_REGION = "region"

PLATFORMS = ["geo_location", "sensor"]
