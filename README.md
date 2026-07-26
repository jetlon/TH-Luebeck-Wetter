# THL Campus Wetterstation – Custom Integration für Home Assistant

Liest die Live-Messwerte der Wetterstation des Solarhauses der
Technischen Hochschule Lübeck (https://wetter.th-luebeck.de/) alle 5
Minuten aus und stellt sie als Sensor-Entities in Home Assistant bereit.

## Installation (manuell, ohne HACS)

1. Den Ordner `custom_components/thl_wetter` in dein Home Assistant
   `config`-Verzeichnis kopieren, sodass am Ende folgender Pfad existiert:

   ```
   /config/custom_components/thl_wetter/
       __init__.py
       config_flow.py
       const.py
       coordinator.py
       manifest.json
       sensor.py
       strings.json
       translations/de.json
   ```

2. Home Assistant neu starten (Entwicklerwerkzeuge → YAML → "Home
   Assistant neu starten" reicht **nicht** – bei neuen Custom
   Integrations ist ein vollständiger Neustart nötig).

3. Nach dem Neustart: **Einstellungen → Geräte & Dienste →
   Integration hinzufügen** → "THL Campus Wetterstation" suchen →
   hinzufügen. Es sind keine weiteren Eingaben nötig.

4. Es erscheint ein Gerät "THL Campus Wetterstation" mit folgenden
   Entities:
   - Temperatur (°C)
   - Luftdruck (hPa)
   - Luftfeuchtigkeit (%)
   - Windgeschwindigkeit (m/s)
   - Windrichtung (°)
   - Direkte Sonneneinstrahlung (W/m²)
   - Sonneneinstrahlung horizontal (W/m²)
   - Sonneneinstrahlung 30°-Ebene (W/m²)
   - Letzte Aktualisierung (Station) – Diagnose-Sensor

   Für Temperatur, Luftdruck, Luftfeuchtigkeit, Windgeschwindigkeit sowie
   alle drei Sonneneinstrahlungs-Kanäle gibt es zusätzlich je einen
   Maximum- und Minimum-Sensor (bezogen auf das aktuelle 15-Minuten-
   Intervall der Station). Windrichtung hat kein Maximum/Minimum, da die
   Gradangabe umlaufend ist. Direkte Sonneneinstrahlung, Sonneneinstrahlung
   horizontal, Sonneneinstrahlung 30°-Ebene sowie alle Maximum-/
   Minimum-Sensoren sind standardmäßig deaktiviert.

   Deaktivierte Sensoren kannst du in den Entity-Einstellungen jederzeit
   einschalten.

## Hinweis zur Spaltenzuordnung

Die Zuordnung der CSV-Spalten (`coordinator.py`, Funktion `parse_csv`)
basiert auf einer Analyse des JavaScript-Codes der Original-Wetterseite
(`table.js`, `scripts.js`). Falls nach der Installation einzelne Werte
offensichtlich falsch erscheinen (z. B. Temperatur und Luftdruck
vertauscht), bitte den Zustand der Entities bzw. die Roh-CSV prüfen –
die Spaltenindizes in `parse_csv()` lassen sich leicht anpassen.

## Spätere Umwandlung in eine "echte" HACS-Integration

Dieser Ordner ist bereits so aufgebaut, dass er 1:1 in ein GitHub-Repo
übernommen werden kann. Für HACS zusätzlich nötig:
- `hacs.json` im Repo-Root
- Ein GitHub-Release/Tag
- Repo bei HACS als "Custom Repository" (Kategorie: Integration)
  hinzufügen
