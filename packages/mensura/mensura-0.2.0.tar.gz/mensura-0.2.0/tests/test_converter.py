import pytest
from mensura.base import Converter
from mensura.conversions import Conversion
from mensura.exceptions import UnitNotFoundException


@pytest.fixture
def converter():
    return Converter()


def test_length_conversion(converter: Converter):
    assert converter.convert(1, "kilometre", "foot") == pytest.approx(3280.84)
    assert converter.convert(1, "foot", "centimetre") == pytest.approx(30.48)
    assert converter.convert(2, "inch", "millimetre") == pytest.approx(50.8)
    assert converter.convert(2, "ft", "mm") == pytest.approx(609.6)
    with pytest.raises(UnitNotFoundException):
        converter.convert(2, "ft", "dm")


def test_time_conversion(converter: Converter):
    assert converter.convert(2, "hour", "second") == 7_200
    assert converter.convert(10.2, "second", "hour") == pytest.approx(0.002833333)
    assert converter.convert(2, "h", "s") == 7_200
    assert converter.convert(1, "d", "s") == 86_400


def test_custom_conversion(converter: Converter):
    converter.add_conversion(Conversion("mile", "kilometre", 1.60934))
    assert converter.convert(152.2, "mile", "kilometre") == pytest.approx(244.941548)
