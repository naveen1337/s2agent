"""Product schemas — Pydantic models, py is primary.

Lazy re-exports so `python -m knowledge.schema.<mod>` stays warning-free.
Usage: `from knowledge.schema import AirConditioner, ...`
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ac import AirConditioner
    from .product import ProductBase
    from .refrigerator import Refrigerator
    from .washing_machine import WashingMachine

__all__ = ["AirConditioner", "ProductBase", "Refrigerator", "WashingMachine"]


def __getattr__(name: str):
    if name == "ProductBase":
        from .product import ProductBase

        return ProductBase
    if name == "AirConditioner":
        from .ac import AirConditioner

        return AirConditioner
    if name == "Refrigerator":
        from .refrigerator import Refrigerator

        return Refrigerator
    if name == "WashingMachine":
        from .washing_machine import WashingMachine

        return WashingMachine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
