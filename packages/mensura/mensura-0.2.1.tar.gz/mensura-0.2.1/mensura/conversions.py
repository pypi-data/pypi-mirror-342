from typing import Final
from dataclasses import dataclass


@dataclass
class Conversion:
    """
    A dataclass to hold conversion information
    """

    src_unit: str
    dest_unit: str
    factor: float


CONVERSIONS: Final[list[Conversion]] = [
    # length
    Conversion("metre", "centimetre", 100.0),
    Conversion("metre", "millimetre", 1000.0),
    Conversion("metre", "kilometre", 0.001),
    Conversion("metre", "foot", 3.28084),
    Conversion("foot", "inch", 12),
    Conversion("inch", "centimetre", 2.54),
    # time
    Conversion("second", "millisecond", 1000),
    Conversion("minute", "second", 60),
    Conversion("hour", "minute", 60),
    Conversion("day", "hour", 24),
]

ABBREVIATIONS: Final[dict[str, str]] = {
    # length
    "km": "kilometre",
    "m": "metre",
    "cm": "centimetre",
    "mm": "millimetre",
    "ft": "foot",
    "in": "inch",
    # time
    "s": "second",
    "ms": "millisecond",
    "min": "minute",
    "h": "hour",
    "d": "day",
}
