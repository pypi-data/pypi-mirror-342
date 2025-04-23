import pytest
from mensura.base import Converter
from mensura.conversions import Conversion


@pytest.fixture
def converter():
    return Converter()


def test_length_conversion(converter: Converter):
    assert converter.convert(1, "kilometre", "foot") == pytest.approx(3280.84)
    assert converter.convert(1, "foot", "centimetre") == pytest.approx(30.48)
    assert converter.convert(2, "inch", "millimetre") == pytest.approx(50.8)


def test_custom_conversion(converter: Converter):
    converter.add_conversion(Conversion("mile", "kilometre", 1.60934))
    assert converter.convert(152.2, "mile", "kilometre") == pytest.approx(244.941548)
