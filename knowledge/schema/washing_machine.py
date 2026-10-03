"""WashingMachine — Pydantic equivalent of `washing-machine.json`.

Hierarchy:
    ProductBase (product.py, from product.json)
      └── WashingMachine (this file, from washing-machine.json)

JSON-Schema source (deleted, py is primary):
    knowledge/schema/washing-machine.json
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import ConfigDict, Field

from .product import ProductBase


class LoadType(str, Enum):
    FRONT_LOAD = "front-load"
    TOP_LOAD = "top-load"
    SEMI_AUTOMATIC = "semi-automatic"
    WASHER_DRYER = "washer-dryer"


class WashingMachine(ProductBase):
    """Washing machine product — extends ProductBase."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    product_type: Literal["washing-machine"] = Field(
        default="washing-machine",
        description="Discriminator. Export as schema:category / additionalType.",
    )

    # -- required specs --
    load_type: LoadType = Field(description="Load / machine type.")
    capacity_kg: float = Field(
        gt=0,
        description="Capacity in kg.",
        examples=[8],
    )

    # -- optional specs --
    max_spin_rpm: int | None = Field(
        default=None,
        gt=0,
        description="Max spin speed in RPM.",
        examples=[1200],
    )
    wash_programs: list[str] = Field(
        default_factory=list,
        description="Wash programs.",
        examples=[["cotton", "quick-wash", "delicates"]],
    )
    inverter_motor: bool = Field(default=True)
    inbuilt_heater: bool = Field(default=False)
    star_rating: int | None = Field(default=None, ge=1, le=5)
    warranty_motor_years: int | None = Field(default=None, ge=0)
    warranty_product_years: int | None = Field(default=None, ge=0)


EXAMPLE_WM = WashingMachine(
    name="LG FHB1208Z4P",
    alias_names=["FHB1208Z4P"],
    model_code="FHB1208Z4P",
    manufacturer="LG",
    parent_version=None,
    current_version="2025.1",
    sector=["home-appliances", "laundry"],
    product_type="washing-machine",
    load_type=LoadType.FRONT_LOAD,
    capacity_kg=8,
    max_spin_rpm=1200,
)


if __name__ == "__main__":
    import json

    print(json.dumps(EXAMPLE_WM.model_dump(by_alias=True), indent=2, ensure_ascii=False))
