"""Support for tracking the Calendar Signs."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import as_local, utcnow

from .const import (
    ATTR_ELEMENT,
    ATTR_MODALITY,
    ATTR_STONE,
    DEFAULT_NAME,
    DOMAIN,
    ELEMENT_AIR,
    ELEMENT_EARTH,
    ELEMENT_FIRE,
    ELEMENT_WATER,
    MODALITY_CARDINAL,
    MODALITY_FIXED,
    MODALITY_MUTABLE,
    TA_NAME,
    SIGN_TA_AQUARIUS,
    SIGN_TA_ARIES,
    SIGN_TA_CANCER,
    SIGN_TA_CAPRICORN,
    SIGN_TA_GEMINI,
    SIGN_TA_LEO,
    SIGN_TA_LIBRA,
    SIGN_TA_PISCES,
    SIGN_TA_SAGITTARIUS,
    SIGN_TA_SCORPIO,
    SIGN_TA_TAURUS,
    SIGN_TA_VIRGO,
    JZ_NAME,
    SIGN_JZ_TURTLE,
    SIGN_JZ_CHERRY,
    SIGN_JZ_SUN,
    SIGN_JZ_BAMBOO,
    SIGN_JZ_BUFFALO,
    SIGN_JZ_LOTUS,
    SIGN_JZ_BRIDGE,
    SIGN_JZ_PEBBLE,
    SIGN_JZ_CAESAR,
    SIGN_JZ_EMPRESS,
    SIGN_JZ_MOON,
    NA_NAME,
    SIGN_NA_FALCON,
    SIGN_NA_BEAVER,
    SIGN_NA_DEER,
    SIGN_NA_WOODPECKER,
    SIGN_NA_SALMON,
    SIGN_NA_BEAR,
    SIGN_NA_RAVEN,
    SIGN_NA_SNAKE,
    SIGN_NA_OWL,
    SIGN_NA_GOOSE,
    SIGN_NA_OTTER,
    SIGN_NA_WOLF,
    STONE_OPAL,
    STONE_JASPER,
    STONE_AGATE,
    STONE_ROSEQUARTZ,
    STONE_CARNELIAN,
    STONE_AMETHYST,
    STONE_AZURITE,
    STONE_COPPER,
    STONE_OBSIDIAN,
    STONE_QUARTZ,
    STONE_TURQUOISE,
    STONE_JADE,
    E_NAME,
    SIGN_E_NILE,
    SIGN_E_AMUNRA,
    SIGN_E_MUT,
    SIGN_E_GEB,
    SIGN_E_OSIRIS,
    SIGN_E_ISIS,
    SIGN_E_THOTH,
    SIGN_E_HORUS,
    SIGN_E_ANUBIS,
    SIGN_E_SETH,
    SIGN_E_BASTET,
    SIGN_E_SEKHMET,
    C_NAME,
    SIGN_C_ROWAN,
    SIGN_C_ASH,
    SIGN_C_ALDER,
    SIGN_C_WILLOW,
    SIGN_C_HAWTHORN,
    SIGN_C_OAK,
    SIGN_C_HOLLY,
    SIGN_C_HAZEL,
    SIGN_C_VINE,
    SIGN_C_IVY,
    SIGN_C_REED,
    SIGN_C_ELDER,
    SIGN_C_BIRCH,
)

TRADITIONAL_ASTROLOGICAL_SIGNS_BY_DATE = (
    (
        (21, 3),
        (20, 4),
        SIGN_TA_ARIES,
        {
            ATTR_ELEMENT: ELEMENT_FIRE,
            ATTR_MODALITY: MODALITY_CARDINAL,
        },
    ),
    (
        (21, 4),
        (20, 5),
        SIGN_TA_TAURUS,
        {
            ATTR_ELEMENT: ELEMENT_EARTH,
            ATTR_MODALITY: MODALITY_FIXED,
        },
    ),
    (
        (21, 5),
        (21, 6),
        SIGN_TA_GEMINI,
        {
            ATTR_ELEMENT: ELEMENT_AIR,
            ATTR_MODALITY: MODALITY_MUTABLE,
        },
    ),
    (
        (22, 6),
        (22, 7),
        SIGN_TA_CANCER,
        {
            ATTR_ELEMENT: ELEMENT_WATER,
            ATTR_MODALITY: MODALITY_CARDINAL,
        },
    ),
    (
        (23, 7),
        (22, 8),
        SIGN_TA_LEO,
        {
            ATTR_ELEMENT: ELEMENT_FIRE,
            ATTR_MODALITY: MODALITY_FIXED,
        },
    ),
    (
        (23, 8),
        (21, 9),
        SIGN_TA_VIRGO,
        {
            ATTR_ELEMENT: ELEMENT_EARTH,
            ATTR_MODALITY: MODALITY_MUTABLE,
        },
    ),
    (
        (22, 9),
        (22, 10),
        SIGN_TA_LIBRA,
        {
            ATTR_ELEMENT: ELEMENT_AIR,
            ATTR_MODALITY: MODALITY_CARDINAL,
        },
    ),
    (
        (23, 10),
        (22, 11),
        SIGN_TA_SCORPIO,
        {
            ATTR_ELEMENT: ELEMENT_WATER,
            ATTR_MODALITY: MODALITY_FIXED,
        },
    ),
    (
        (23, 11),
        (21, 12),
        SIGN_TA_SAGITTARIUS,
        {
            ATTR_ELEMENT: ELEMENT_FIRE,
            ATTR_MODALITY: MODALITY_MUTABLE,
        },
    ),
    (
        (22, 12),
        (20, 1),
        SIGN_TA_CAPRICORN,
        {
            ATTR_ELEMENT: ELEMENT_EARTH,
            ATTR_MODALITY: MODALITY_CARDINAL,
        },
    ),
    (
        (21, 1),
        (19, 2),
        SIGN_TA_AQUARIUS,
        {
            ATTR_ELEMENT: ELEMENT_AIR,
            ATTR_MODALITY: MODALITY_FIXED,
        },
    ),
    (
        (20, 2),
        (20, 3),
        SIGN_TA_PISCES,
        {
            ATTR_ELEMENT: ELEMENT_WATER,
            ATTR_MODALITY: MODALITY_MUTABLE,
        },
    ),
)

JAPAN_ZEN_SIGNS_BY_DATE = (
    (
        (19, 1),
        (14, 2),
        SIGN_JZ_TURTLE,
    ),
    (
        (15, 2),
        (20, 3),
        SIGN_JZ_CHERRY,
    ),
    (
        (21, 3),
        (29, 4),
        SIGN_JZ_SUN,
    ),
    (
        (30, 4),
        (4, 6),
        SIGN_JZ_BAMBOO,
    ),
    (
        (5, 6),
        (6, 7),
        SIGN_JZ_BUFFALO,
    ),
    (
        (7, 7),
        (1, 8),
        SIGN_JZ_LOTUS,
    ),
    (
        (2, 8),
        (27, 8),
        SIGN_JZ_BRIDGE,
    ),
    (
        (28, 8),
        (10, 10),
        SIGN_JZ_PEBBLE,
    ),
    (
        (11, 10),
        (18, 11),
        SIGN_JZ_CAESAR,
    ),
    (
        (19, 11),
        (26, 12),
        SIGN_JZ_EMPRESS,
    ),
    (
        (27, 12),
        (18, 1),
        SIGN_JZ_MOON,
    ),
)

NATIVE_AMERICAN_SIGNS_BY_DATE = (
    (
        (21, 3),
        (19, 4),
        SIGN_NA_FALCON,
        {
            ATTR_STONE: STONE_OPAL,
        },
    ),
    (
        (20, 4),
        (20, 5),
        SIGN_NA_BEAVER,
        {
            ATTR_STONE: STONE_JASPER,
        },
    ),
    (
        (21, 5),
        (20, 6),
        SIGN_NA_DEER,
        {
            ATTR_STONE: STONE_AGATE,
        },
    ),
    (
        (21, 6),
        (21, 7),
        SIGN_NA_WOODPECKER,
        {
            ATTR_STONE: STONE_ROSEQUARTZ,
        },
    ),
    (
        (22, 7),
        (21, 8),
        SIGN_NA_SALMON,
        {
            ATTR_STONE: STONE_CARNELIAN,
        },
    ),
    (
        (22, 8),
        (21, 9),
        SIGN_NA_BEAR,
        {
            ATTR_STONE: STONE_AMETHYST,
        },
    ),
    (
        (22, 9),
        (22, 10),
        SIGN_NA_RAVEN,
        {
            ATTR_STONE: STONE_AZURITE,
        },
    ),
    (
        (23, 10),
        (22, 11),
        SIGN_NA_SNAKE,
        {
            ATTR_STONE: STONE_COPPER,
        },
    ),
    (
        (21, 11),
        (21, 12),
        SIGN_NA_OWL,
        {
            ATTR_STONE: STONE_OBSIDIAN,
        },
    ),
    (
        (22, 12),
        (19, 1),
        SIGN_NA_GOOSE,
        {
            ATTR_STONE: STONE_QUARTZ,
        },
    ),
    (
        (20, 1),
        (18, 2),
        SIGN_NA_OTTER,
        {
            ATTR_STONE: STONE_TURQUOISE,
        },
    ),
    (
        (19, 2),
        (20, 3),
        SIGN_NA_WOLF,
        {
            ATTR_STONE: STONE_JADE,
        },
    ),
)

EGYPTIAN_SIGNS_BY_DATE = (
    (
        (1, 1),
        (7, 1),
        SIGN_E_NILE,
    ),
    (
        (8, 1),
        (21, 1),
        SIGN_E_AMUNRA,
    ),
    (
        (22, 1),
        (31, 1),
        SIGN_E_MUT,
    ),
    (
        (12, 2),
        (29, 2),
        SIGN_E_GEB,
    ),
    (
        (1, 3),
        (10, 3),
        SIGN_E_OSIRIS,
    ),
    (
        (11, 3),
        (31, 3),
        SIGN_E_ISIS,
    ),
    (
        (1, 4),
        (19, 4),
        SIGN_E_THOTH,
    ),
    (
        (20, 4),
        (7, 8),
        SIGN_E_HORUS,
    ),
    (
        (8, 5),
        (27, 5),
        SIGN_E_ANUBIS,
    ),
    (
        (28, 5),
        (18, 6),
        SIGN_E_SETH,
    ),
    (
        (14, 7),
        (28, 7),
        SIGN_E_BASTET,
    ),
    (
        (29, 7),
        (11, 8),
        SIGN_E_SEKHMET,
    ),
    (
        (19, 6),
        (28, 6),
        SIGN_E_NILE,
    ),
    (
        (1, 2),
        (11, 2),
        SIGN_E_AMUNRA,
    ),
    (
        (8, 9),
        (22, 9),
        SIGN_E_MUT,
    ),
    (
        (20, 8),
        (31, 8),
        SIGN_E_GEB,
    ),
    (
        (27, 11),
        (18, 12),
        SIGN_E_OSIRIS,
    ),
    (
        (18, 10),
        (29, 10),
        SIGN_E_ISIS,
    ),
    (
        (8, 11),
        (17, 11),
        SIGN_E_THOTH,
    ),
    (
        (12, 8),
        (19, 8),
        SIGN_E_HORUS,
    ),
    (
        (29, 6),
        (13, 7),
        SIGN_E_ANUBIS,
    ),
    (
        (28, 9),
        (2, 10),
        SIGN_E_SETH,
    ),
    (
        (23, 9),
        (27, 9),
        SIGN_E_BASTET,
    ),
    (
        (30, 10),
        (7, 11),
        SIGN_E_SEKHMET,
    ),
    (
        (1, 9),
        (7, 9),
        SIGN_E_NILE,
    ),
    (
        (19, 12),
        (31, 12),
        SIGN_E_ISIS,
    ),
    (
        (3, 10),
        (17, 10),
        SIGN_E_BASTET,
    ),
    (
        (18, 11),
        (26, 11),
        SIGN_E_NILE,
    ),
)

CELTIC_SIGNS_BY_DATE = (
    (
        (21, 1),
        (17, 2),
        SIGN_C_ROWAN,
    ),
    (
        (18, 2),
        (17, 3),
        SIGN_C_ASH,
    ),
    (
        (18, 3),
        (14, 4),
        SIGN_C_ALDER,
    ),
    (
        (15, 4),
        (12, 5),
        SIGN_C_WILLOW,
    ),
    (
        (13, 5),
        (9, 6),
        SIGN_C_HAWTHORN,
    ),
    (
        (10, 6),
        (7, 7),
        SIGN_C_OAK,
    ),
    (
        (8, 7),
        (4, 8),
        SIGN_C_HOLLY,
    ),
    (
        (5, 8),
        (1, 9),
        SIGN_C_HAZEL,
    ),
    (
        (2, 9),
        (29, 9),
        SIGN_C_VINE,
    ),
    (
        (30, 9),
        (27, 10),
        SIGN_C_IVY,
    ),
    (
        (28, 10),
        (24, 11),
        SIGN_C_REED,
    ),
    (
        (25, 11),
        (23, 12),
        SIGN_C_ELDER,
    ),
    (
        (24, 12),
        (20, 1),
        SIGN_C_BIRCH,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize the entries."""

    async_add_entities([TraditionalAstrologicalZodiacSensor(entry_id=entry.entry_id)], True)
    async_add_entities([JapanZenSignsSensor(entry_id=entry.entry_id)], True)
    """async_add_entities([AztecSignsSensor(entry_id=entry.entry_id)], True)"""
    async_add_entities([NativeAmericanSignsSensor(entry_id=entry.entry_id)], True)
    """async_add_entities([PersianSignsSensor(entry_id=entry.entry_id)], True)"""
    async_add_entities([EgyptianSignsSensor(entry_id=entry.entry_id)], True)
    async_add_entities([CelticSignsSensor(entry_id=entry.entry_id)], True)
    """async_add_entities([ChineseSignsSensor(entry_id=entry.entry_id)], True)"""
    
class TraditionalAstrologicalZodiacSensor(SensorEntity):
    """Representation of a Traditional Astrological Zodiac sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        SIGN_TA_AQUARIUS,
        SIGN_TA_ARIES,
        SIGN_TA_CANCER,
        SIGN_TA_CAPRICORN,
        SIGN_TA_GEMINI,
        SIGN_TA_LEO,
        SIGN_TA_LIBRA,
        SIGN_TA_PISCES,
        SIGN_TA_SAGITTARIUS,
        SIGN_TA_SCORPIO,
        SIGN_TA_TAURUS,
        SIGN_TA_VIRGO,
    ]
    _attr_translation_key = "sign"
    _attr_device_info = DeviceInfo(
        name=DEFAULT_NAME,
        identifiers={(DOMAIN, entry_id)},
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(self, entry_id: str) -> None:
        """Initialize Traditional Astrological Signs sensor."""
        self._attr_unique_id = "traditional_astrological_zodiac"
        self._attr_name = TA_NAME

    async def async_update(self) -> None:
        """Get the time and updates the state."""
        today = as_local(utcnow()).date()

        for sign in TRADITIONAL_ASTROLOGICAL_SIGNS_BY_DATE:
            if (today.month == sign[0][1] and today.day >= sign[0][0]) or (
                today.month == sign[1][1] and today.day <= sign[1][0]
            ):
                self._attr_native_value = sign[2]
                self._attr_extra_state_attributes = sign[3]
                break

class JapanZenSignsSensor(SensorEntity):
    """Representation of a Japan Zen Signs sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        SIGN_JZ_TURTLE,
        SIGN_JZ_CHERRY,
        SIGN_JZ_SUN,
        SIGN_JZ_BAMBOO,
        SIGN_JZ_BUFFALO,
        SIGN_JZ_LOTUS,
        SIGN_JZ_BRIDGE,
        SIGN_JZ_PEBBLE,
        SIGN_JZ_CAESAR,
        SIGN_JZ_EMPRESS,
        SIGN_JZ_MOON,
    ]
    _attr_translation_key = "sign"
    _attr_device_info = DeviceInfo(
        name=DEFAULT_NAME,
        identifiers={(DOMAIN, entry_id)},
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(self, entry_id: str) -> None:
        """Initialize Japan Zen Signs sensor."""
        self._attr_unique_id = "japan_zen_signs"
        self._attr_name = JZ_NAME

    async def async_update(self) -> None:
        """Get the time and updates the state."""
        today = as_local(utcnow()).date()

        for sign in JAPAN_ZEN_SIGNS_BY_DATE:
            if (today.month == sign[0][1] and today.day >= sign[0][0]) or (
                today.month == sign[1][1] and today.day <= sign[1][0]
            ):
                self._attr_native_value = sign[2]
                break

class NativeAmericanSignsSensor(SensorEntity):
    """Representation of a Native American Signs sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        SIGN_NA_FALCON,
        SIGN_NA_BEAVER,
        SIGN_NA_DEER,
        SIGN_NA_WOODPECKER,
        SIGN_NA_SALMON,
        SIGN_NA_BEAR,
        SIGN_NA_RAVEN,
        SIGN_NA_SNAKE,
        SIGN_NA_OWL,
        SIGN_NA_GOOSE,
        SIGN_NA_OTTER,
        SIGN_NA_WOLF,
    ]
    _attr_translation_key = "sign"
    _attr_device_info = DeviceInfo(
        name=DEFAULT_NAME,
        identifiers={(DOMAIN, entry_id)},
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(self, entry_id: str) -> None:
        """Initialize Native American Signs sensor."""
        self._attr_unique_id = "native_american_signs"
        self._attr_name = NA_NAME

    async def async_update(self) -> None:
        """Get the time and updates the state."""
        today = as_local(utcnow()).date()

        for sign in NATIVE_AMERICAN_SIGNS_BY_DATE:
            if (today.month == sign[0][1] and today.day >= sign[0][0]) or (
                today.month == sign[1][1] and today.day <= sign[1][0]
            ):
                self._attr_native_value = sign[2]
                self._attr_extra_state_attributes = sign[3]
                break

class EgyptianSignsSensor(SensorEntity):
    """Representation of a Egyptian Signs sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        SIGN_E_NILE,
        SIGN_E_AMUNRA,
        SIGN_E_MUT,
        SIGN_E_GEB,
        SIGN_E_OSIRIS,
        SIGN_E_ISIS,
        SIGN_E_THOTH,
        SIGN_E_HORUS,
        SIGN_E_ANUBIS,
        SIGN_E_SETH,
        SIGN_E_BASTET,
        SIGN_E_SEKHMET,
    ]
    _attr_translation_key = "sign"
    _attr_device_info = DeviceInfo(
        name=DEFAULT_NAME,
        identifiers={(DOMAIN, entry_id)},
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(self, entry_id: str) -> None:
        """Initialize Egyptian Signs sensor."""
        self._attr_unique_id = "egyptian_signs"
        self._attr_name = E_NAME

    async def async_update(self) -> None:
        """Get the time and updates the state."""
        today = as_local(utcnow()).date()

        for sign in EGYPTIAN_SIGNS_BY_DATE:
            if (today.month == sign[0][1] and today.day >= sign[0][0]) or (
                today.month == sign[1][1] and today.day <= sign[1][0]
            ):
                self._attr_native_value = sign[2]
                break

class CelticSignsSensor(SensorEntity):
    """Representation of a Celtic Signs sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        SIGN_C_ROWAN,
        SIGN_C_ASH,
        SIGN_C_ALDER,
        SIGN_C_WILLOW,
        SIGN_C_HAWTHORN,
        SIGN_C_OAK,
        SIGN_C_HOLLY,
        SIGN_C_HAZEL,
        SIGN_C_VINE,
        SIGN_C_IVY,
        SIGN_C_REED,
        SIGN_C_ELDER,
        SIGN_C_BIRCH,
    ]
    _attr_translation_key = "sign"
    _attr_device_info = DeviceInfo(
        name=DEFAULT_NAME,
        identifiers={(DOMAIN, entry_id)},
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(self, entry_id: str) -> None:
        """Initialize Celtic Signs sensor."""
        self._attr_unique_id = "celtic_signs"
        self._attr_name = C_NAME

    async def async_update(self) -> None:
        """Get the time and updates the state."""
        today = as_local(utcnow()).date()

        for sign in CELTIC_SIGNS_BY_DATE:
            if (today.month == sign[0][1] and today.day >= sign[0][0]) or (
                today.month == sign[1][1] and today.day <= sign[1][0]
            ):
                self._attr_native_value = sign[2]
                break
