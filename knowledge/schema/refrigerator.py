"""Refrigerator — Pydantic equivalent of `refrigerator.json`.

Hierarchy:
    ProductBase (product.py, from product.json)
      └── Refrigerator (this file, from refrigerator.json)

JSON-Schema source (deleted, py is primary):
    knowledge/schema/refrigerator.json
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import ConfigDict, Field

from .product import ProductBase


class DoorConfiguration(str, Enum):
    SINGLE_DOOR = "single-door"
    DOUBLE_DOOR = "double-door"
    SIDE_BY_SIDE = "side-by-side"
    FRENCH_DOOR = "french-door"
    MULTI_DOOR = "multi-door"


class DefrostType(str, Enum):
    DIRECT_COOL = "direct-cool"
    FROST_FREE = "frost-free"


class RefrigeratorCompressorType(str, Enum):
    INVERTER = "inverter"
    RECIPROCATING = "reciprocating"
    LINEAR_INVERTER = "linear-inverter"
    DIGITAL_INVERTER = "digital-inverter"


class ShelfMaterial(str, Enum):
    TOUGHENED_GLASS = "toughened-glass"
    WIRE = "wire"
    PLASTIC = "plastic"


class Refrigerator(ProductBase):
    """Refrigerator product — extends ProductBase."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    product_type: Literal["refrigerator"] = Field(
        default="refrigerator",
        description="Discriminator. Export as schema:category / additionalType.",
    )

    # -- required specs --
    capacity_litres: int = Field(
        gt=0,
        description="Capacity in litres.",
        examples=[223],
    )
    door_configuration: DoorConfiguration = Field(
        description="Door configuration.",
    )
    defrost_type: DefrostType = Field(
        description="Defrost technology.",
    )

    # -- optional specs --
    star_rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="BEE energy rating.",
    )
    compressor_type: RefrigeratorCompressorType | None = Field(
        default=None,
        description="Compressor technology.",
    )
    shelf_material: ShelfMaterial | None = Field(
        default=None,
        description="Shelf material.",
    )
    convertible_modes: list[str] = Field(
        default_factory=list,
        description="Convertible / flex modes.",
    )
    warranty_compressor_years: int | None = Field(default=None, ge=0)
    warranty_product_years: int | None = Field(default=None, ge=0)


EXAMPLE_FRIDGE = Refrigerator(
    name="LG GLD2156ZHSL",
    alias_names=["GLD2156ZHSL"],
    model_code="GLD2156ZHSL",
    manufacturer="LG",
    parent_version=None,
    current_version="2025.1",
    sector=["home-appliances", "cooling"],
    product_type="refrigerator",
    capacity_litres=215,
    door_configuration=DoorConfiguration.DOUBLE_DOOR,
    defrost_type=DefrostType.FROST_FREE,
    star_rating=3,
)


if __name__ == "__main__":
    import json

    print(json.dumps(EXAMPLE_FRIDGE.model_dump(by_alias=True), indent=2, ensure_ascii=False))
