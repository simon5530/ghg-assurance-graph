"""Deliberately bounded unit vocabulary. CO2e is not physical gas mass."""

from enum import StrEnum
from math import isfinite

import pint

_REGISTRY = pint.UnitRegistry()
_REGISTRY.define("kg_CO2e = [co2_equivalent]")
_REGISTRY.define("t_CO2e = 1000 * kg_CO2e")
_REGISTRY.define("USD = [currency_USD]")


class Unit(StrEnum):
    KWH = "kWh"
    MJ = "MJ"
    KG = "kg"
    TONNE = "tonne"
    LITRE = "liter"
    M3 = "meter ** 3"
    KM = "km"
    TONNE_KM = "tonne * km"
    USD = "USD"
    KG_CO2E = "kg_CO2e"
    T_CO2E = "t_CO2e"


def convert(value: float, source: Unit, target: Unit) -> float:
    """Convert compatible enumerated units; never characterize gases or currencies."""
    source, target = Unit(source), Unit(target)
    if isinstance(value, bool) or not isfinite(value) or value < 0:
        raise ValueError("amount must be finite and nonnegative")
    result = float(_REGISTRY.Quantity(value, source.value).to(target.value).magnitude)
    if not isfinite(result):
        raise ValueError("conversion overflow")
    return result
