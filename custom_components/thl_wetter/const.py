"""Constants for the THL Campus Wetterstation integration."""

DOMAIN = "thl_wetter"

# Live-CSV der Wetterstation des Solarhauses (Labor für Solartechnik, TH Lübeck)
DATA_URL = "https://wetter.th-luebeck.de/1Woche+Max+Min01.CSV"

# Abfrageintervall - vom Nutzer konfigurierbar (Config-/Options-Flow), in Minuten.
# Default entspricht dem bisherigen festen Intervall von 15 Minuten.
CONF_SCAN_INTERVAL_MINUTES = "scan_interval_minutes"
DEFAULT_SCAN_INTERVAL_MINUTES = 15
MIN_SCAN_INTERVAL_MINUTES = 1
MAX_SCAN_INTERVAL_MINUTES = 1440
