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
    Conversion("metre", "centimetre", 100.0),
    Conversion("metre", "millimetre", 1000.0),
    Conversion("metre", "kilometre", 0.001),
    Conversion("metre", "foot", 3.28084),
    Conversion("foot", "inch", 12),
    Conversion("inch", "centimetre", 2.54),
]
