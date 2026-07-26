"""Sensor platform for the THL Campus Wetterstation integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    UnitOfIrradiance,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ThlWetterCoordinator, degrees_to_compass


@dataclass(frozen=True, kw_only=True)
class ThlSensorDescription(SensorEntityDescription):
    """Beschreibt einen einzelnen Messwert der THL-Wetterstation."""


SENSOR_DESCRIPTIONS: tuple[ThlSensorDescription, ...] = (
    ThlSensorDescription(
        key="temperature",
        translation_key="temperature",
        name="Temperatur",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="temperature_max",
        translation_key="temperature_max",
        name="Temperatur Maximum",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="temperature_min",
        translation_key="temperature_min",
        name="Temperatur Minimum",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="pressure",
        translation_key="pressure",
        name="Luftdruck",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="pressure_max",
        translation_key="pressure_max",
        name="Luftdruck Maximum",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="pressure_min",
        translation_key="pressure_min",
        name="Luftdruck Minimum",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="humidity",
        translation_key="humidity",
        name="Luftfeuchtigkeit",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="humidity_max",
        translation_key="humidity_max",
        name="Luftfeuchtigkeit Maximum",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="humidity_min",
        translation_key="humidity_min",
        name="Luftfeuchtigkeit Minimum",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="wind_speed",
        translation_key="wind_speed",
        name="Windgeschwindigkeit",
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="wind_speed_max",
        translation_key="wind_speed_max",
        name="Windgeschwindigkeit Maximum",
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="wind_speed_min",
        translation_key="wind_speed_min",
        name="Windgeschwindigkeit Minimum",
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="wind_direction",
        translation_key="wind_direction",
        name="Windrichtung",
        native_unit_of_measurement=DEGREE,
        icon="mdi:compass-outline",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="radiation_direct",
        translation_key="radiation_direct",
        name="Direkte Sonneneinstrahlung",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ThlSensorDescription(
        key="radiation_direct_max",
        translation_key="radiation_direct_max",
        name="Direkte Sonneneinstrahlung Maximum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_direct_min",
        translation_key="radiation_direct_min",
        name="Direkte Sonneneinstrahlung Minimum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_horizontal",
        translation_key="radiation_horizontal",
        name="Sonneneinstrahlung horizontal",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_horizontal_max",
        translation_key="radiation_horizontal_max",
        name="Sonneneinstrahlung horizontal Maximum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_horizontal_min",
        translation_key="radiation_horizontal_min",
        name="Sonneneinstrahlung horizontal Minimum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_30deg",
        translation_key="radiation_30deg",
        name="Sonneneinstrahlung 30°-Ebene",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_30deg_max",
        translation_key="radiation_30deg_max",
        name="Sonneneinstrahlung 30°-Ebene Maximum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="radiation_30deg_min",
        translation_key="radiation_30deg_min",
        name="Sonneneinstrahlung 30°-Ebene Minimum",
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ThlSensorDescription(
        key="last_update",
        translation_key="last_update",
        name="Letzte Aktualisierung (Station)",
        icon="mdi:clock-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up THL Wetterstation sensors from a config entry."""
    coordinator: ThlWetterCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ThlWetterSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class ThlWetterSensor(CoordinatorEntity[ThlWetterCoordinator], SensorEntity):
    """Repräsentiert einen einzelnen Messwert der THL-Wetterstation."""

    entity_description: ThlSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ThlWetterCoordinator,
        entry: ConfigEntry,
        description: ThlSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="THL Campus Wetterstation",
            manufacturer="Technische Hochschule Lübeck",
            model="Solarhaus Wetterstation",
            configuration_url="https://wetter.th-luebeck.de/",
        )

    @property
    def native_value(self):
        """Aktuellen Wert aus den zuletzt geladenen Koordinator-Daten liefern."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Zusätzliche Attribute - aktuell nur Himmelsrichtung beim Windrichtung-Sensor."""
        if self.entity_description.key != "wind_direction" or self.coordinator.data is None:
            return None
        compass = degrees_to_compass(self.coordinator.data.get("wind_direction"))
        if compass is None:
            return None
        return {"himmelsrichtung": compass}
