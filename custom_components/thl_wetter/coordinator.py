"""DataUpdateCoordinator for the THL Campus Wetterstation integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DATA_URL, DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15

_COMPASS_POINTS = [
    "N", "NNO", "NO", "ONO", "O", "OSO", "SO", "SSO",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]

# Kanal-Spec: (key, CSV-Spaltenindex, hat_min_max)
# Spaltenzuordnung abgeleitet aus table.js/scripts.js der Original-Website,
# verifiziert per Live-CSV-Fetch und Abgleich mit der "Aktuelle"-Tabelle der
# Website. wind_direction hat bewusst kein Min/Max (Gradangabe ist
# umlaufend, die Website zeigt dafür leere Maximum-/Minimum-Zellen).
CHANNELS: tuple[tuple[str, int, bool], ...] = (
    ("wind_speed", 1, True),
    ("wind_direction", 3, False),
    ("pressure", 5, True),
    ("humidity", 7, True),
    ("temperature", 9, True),
    ("radiation_direct", 11, True),
    ("radiation_horizontal", 13, True),
    ("radiation_30deg", 15, True),
)


def degrees_to_compass(degrees: float | None) -> str | None:
    """Wandelt eine Windrichtung in Grad in die 16-Punkte-Himmelsrichtung um."""
    if degrees is None:
        return None
    index = int((degrees % 360) / 22.5 + 0.5) % 16
    return _COMPASS_POINTS[index]


def _to_num(raw: str | None) -> float | None:
    """Zahlen-Konvertierung analog zu numberConverter() aus lib.js der Wetterseite."""
    s = (raw or "").strip()
    if s == "":
        return None
    if s[-1] in ("+", "-"):
        s = s[:-1]
    s = s.replace(",", ".")
    try:
        return round(float(s), 2)
    except ValueError:
        return None


def _decode(raw: bytes) -> str:
    """Dekodiert die CSV robust - die Datei ist nicht garantiert UTF-8."""
    for encoding in ("utf-8", "cp1252", "iso-8859-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def parse_csv(raw: bytes) -> dict[str, Any]:
    """Parst die Live-CSV und liefert das letzte vollständige Mittel/Max/Min-Triplet.

    Die CSV enthält pro Messzeitpunkt drei aufeinanderfolgende Zeilen
    (Mittelwert, Maximum, Minimum) je Spalte/Kanal - siehe table.js/scripts.js
    der Original-Wetterseite.
    """
    raw_text = _decode(raw)
    lines = [line for line in raw_text.strip("\n").split("\n") if line != ""]
    rows = [line.split(";") for line in lines]

    if not rows:
        raise UpdateFailed("Leere Antwort von der Wetterstation")

    num_cols = max(len(r) for r in rows)
    cols: list[list[str]] = [[] for _ in range(num_cols)]
    for row in rows:
        for i in range(num_cols):
            cols[i].append(row[i] if i < len(row) else "")

    col1 = cols[1] if len(cols) > 1 else []
    last_idx: int | None = None
    for i in range(len(col1) - 1, -1, -1):
        if col1[i] not in ("", None):
            last_idx = i
            break

    if last_idx is None or last_idx < 2:
        raise UpdateFailed("Keine gültigen Messwerte in der CSV gefunden")

    mean_idx = last_idx - 2
    max_idx = last_idx - 1
    min_idx = last_idx

    def val(col_index: int, row_index: int = mean_idx) -> float | None:
        if col_index >= len(cols):
            return None
        return _to_num(cols[col_index][row_index])

    data: dict[str, Any] = {
        "last_update": cols[0][mean_idx].strip() if mean_idx < len(cols[0]) else None,
    }
    for key, col_index, has_min_max in CHANNELS:
        data[key] = val(col_index)
        if has_min_max:
            data[f"{key}_max"] = val(col_index, max_idx)
            data[f"{key}_min"] = val(col_index, min_idx)

    return data


class ThlWetterCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Koordinator, der die Live-CSV der THL-Wetterstation periodisch abruft."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            async with async_timeout.timeout(REQUEST_TIMEOUT):
                async with self._session.get(DATA_URL) as resp:
                    resp.raise_for_status()
                    raw_bytes = await resp.read()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Fehler beim Abrufen der Wetterdaten: {err}") from err

        return await self.hass.async_add_executor_job(parse_csv, raw_bytes)
