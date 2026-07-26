# THL Campus Wetterstation – Custom Integration für Home Assistant

Liest die Live-Messwerte der Wetterstation des Solarhauses der
Technischen Hochschule Lübeck (https://wetter.th-luebeck.de/) in einem
einstellbaren Intervall aus und stellt sie als Sensor-Entities in Home
Assistant bereit.

## Installation via HACS (empfohlen)

1. In Home Assistant **HACS → oben rechts die drei Punkte →
   Benutzerdefinierte Repositories** öffnen.
2. Repository-URL eintragen: `https://github.com/jetlon/TH-Luebeck-Wetter`
3. Kategorie **Integration** auswählen → **Hinzufügen**.
4. Danach in HACS nach **„THL Campus Wetterstation"** suchen und
   herunterladen.
5. Home Assistant **vollständig neu starten** (siehe Hinweis unten – ein
   YAML-Reload reicht bei neuen Custom Integrations nicht).
6. **Einstellungen → Geräte & Dienste → Integration hinzufügen** →
   „THL Campus Wetterstation" suchen → hinzufügen. Dabei wird das
   **Abfrageintervall in Minuten** abgefragt (Standard: 15 Minuten).

Updates erscheinen künftig automatisch in HACS, sobald ein neuer
GitHub-Release/Tag im Repo veröffentlicht wird.

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
   hinzufügen. Dabei wird das **Abfrageintervall in Minuten** abgefragt
   (Standard: 15 Minuten). Das Intervall lässt sich später jederzeit über
   **Konfigurieren** bei der Integration ändern, ohne sie neu einrichten
   zu müssen.

4. Es erscheint ein Gerät "THL Campus Wetterstation" mit folgenden
   Entities:
   - Temperatur (°C)
   - Luftdruck (hPa)
   - Luftfeuchtigkeit (%)
   - Windgeschwindigkeit (m/s)
   - Windrichtung (°)
   - Direkte Sonneneinstrahlung (W/m²)
   - Direkte Sonneneinstrahlung Einstufung (Text: Keine/Schwach/Mäßig/
     Stark/Sehr stark)
   - Sonneneinstrahlung horizontal (W/m²)
   - Sonneneinstrahlung 30°-Ebene (W/m²)
   - Letzte Aktualisierung (Station) – Diagnose-Sensor

   Für Temperatur, Luftdruck, Luftfeuchtigkeit, Windgeschwindigkeit sowie
   alle drei Sonneneinstrahlungs-Kanäle gibt es zusätzlich je einen
   Maximum- und Minimum-Sensor (bezogen auf das eingestellte
   Abfrageintervall). Windrichtung hat kein Maximum/Minimum, da die
   Gradangabe umlaufend ist. Sonneneinstrahlung horizontal, Sonneneinstrahlung
   30°-Ebene sowie alle Maximum-/Minimum-Sensoren sind standardmäßig
   deaktiviert.

   Deaktivierte Sensoren kannst du in den Entity-Einstellungen jederzeit
   einschalten.

## Hinweis zur Spaltenzuordnung

Die Zuordnung der CSV-Spalten (`coordinator.py`, Funktion `parse_csv`)
basiert auf einer Analyse des JavaScript-Codes der Original-Wetterseite
(`table.js`, `scripts.js`). Falls nach der Installation einzelne Werte
offensichtlich falsch erscheinen (z. B. Temperatur und Luftdruck
vertauscht), bitte den Zustand der Entities bzw. die Roh-CSV prüfen –
die Spaltenindizes in `parse_csv()` lassen sich leicht anpassen.

## Repository

- GitHub: https://github.com/jetlon/TH-Luebeck-Wetter
- Releases: https://github.com/jetlon/TH-Luebeck-Wetter/releases
- Issues/Bugs: https://github.com/jetlon/TH-Luebeck-Wetter/issues

## Haftungsausschluss

Dies ist ein privates, nicht-kommerzielles Hobby-Projekt ohne jede
Verbindung zur Technischen Hochschule Lübeck. Die Integration greift
lediglich auf eine öffentlich zugängliche Datenquelle der TH Lübeck zu;
Betrieb, Inhalt und Verfügbarkeit dieser Datenquelle liegen außerhalb
meines Einflussbereichs.

Die Nutzung dieser Integration erfolgt vollständig auf eigene Gefahr. Sie
wird „wie besehen" (as-is), ohne jegliche ausdrückliche oder
stillschweigende Gewährleistung bereitgestellt – insbesondere ohne
Zusicherung der Richtigkeit, Vollständigkeit, Aktualität oder
Eignung der gelieferten Wetterdaten für einen bestimmten Zweck, und ohne
Zusicherung eines fehlerfreien oder unterbrechungsfreien Betriebs.

Jegliche Haftung für Schäden – gleich welcher Art und ob unmittelbar oder
mittelbar –, die aus der Installation, Nutzung oder Fehlfunktion dieser
Integration oder aus fehlerhaften, verzögerten oder ausbleibenden Daten
der externen Wetterstation entstehen, ist im gesetzlich zulässigen Rahmen
ausgeschlossen. Der Rechtsweg ist, soweit gesetzlich zulässig,
ausgeschlossen.

Nach deutschem Recht nicht ausschließbare Haftung – insbesondere für
Vorsatz, grobe Fahrlässigkeit sowie Schäden an Leben, Körper oder
Gesundheit – bleibt von diesem Ausschluss unberührt.
