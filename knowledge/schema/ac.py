"""AirConditioner — Pydantic equivalent of `ac.json`.

Hierarchy:
    ProductBase (product.py, from product.json)
      └── AirConditioner (this file, from ac.json)

Extra specs map to schema:additionalProperty / specification at export time.

JSON-Schema source:
    knowledge/schema/ac.json

Regenerate JSON Schema any time with:
    AirConditioner.model_json_schema()
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import ConfigDict, Field

from .product import ProductBase


# ---------------------------------------------------------------------------
# Editable enums — add new values here instead of hunting through JSON
# ---------------------------------------------------------------------------


class CompressorType(str, Enum):
    INVERTER = "inverter"
    NON_INVERTER = "non-inverter"
    DUAL_INVERTER = "dual-inverter"


class CondenserCoil(str, Enum):
    COPPER = "copper"
    ALUMINIUM = "aluminium"


# ---------------------------------------------------------------------------
# AirConditioner
# ---------------------------------------------------------------------------


class AirConditioner(ProductBase):
    """Air conditioner product — extends ProductBase."""

    model_config = ConfigDict(
        extra="forbid",  # == unevaluatedProperties: false
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    # -- discriminator (required, const in ac.json) --
    # Export as schema:category / additionalType.
    product_type: Literal["ac"] = Field(
        default="ac",
        description="Discriminator. Export as schema:category / additionalType.",
    )

    # -- required AC specs --
    capacity_tonnage: float = Field(
        gt=0,
        description="Cooling capacity in tons. e.g. 1.5.",
        examples=[1.5],
    )
    star_rating: int = Field(
        ge=1,
        le=5,
        description="BEE energy rating. Export as schema:hasEnergyConsumptionDetails.",
        examples=[5],
    )

    # -- optional AC specs (easy to edit below) --
    compressor_type: CompressorType = Field(
        default=CompressorType.INVERTER,
        description="Compressor technology.",
    )
    refrigerant: str | None = Field(
        default=None,
        description="Refrigerant gas.",
        examples=["R32", "R410A"],
    )
    condenser_coil: CondenserCoil | None = Field(
        default=None,
        description="Condenser coil material.",
    )
    air_swing_modes: list[str] = Field(
        default_factory=list,
        description="Swing modes.",
        examples=[["4-way", "auto"]],
    )
    filters: list[str] = Field(
        default_factory=list,
        description="Filter types.",
        examples=[["HD filter", "anti-virus"]],
    )
    warranty_compressor_years: int | None = Field(
        default=None,
        ge=0,
        description="Compressor warranty in years.",
    )
    warranty_product_years: int | None = Field(
        default=None,
        ge=0,
        description="Overall product warranty in years.",
    )


# ---------------------------------------------------------------------------
# Example from ac.json $examples — stays valid, stays editable
# ---------------------------------------------------------------------------

EXAMPLE_AC = AirConditioner(
    name="LG DUALCOOL AI AS-Q20JWZE",
    alias_names=["AS-Q20JWZE", "LG Dualcool 1.6T"],
    model_code="AS-Q20JWZE",
    manufacturer="LG",
    parent_version=None,
    current_version="2025.1",
    sector=["home-appliances", "cooling"],
    product_type="ac",
    capacity_tonnage=1.6,
    star_rating=5,
    compressor_type=CompressorType.DUAL_INVERTER,
    refrigerant="R32",
)


if __name__ == "__main__":
    import json

    print(json.dumps(EXAMPLE_AC.model_dump(by_alias=True), indent=2, ensure_ascii=False))
    print("--- JSON Schema ---")
    print(json.dumps(AirConditioner.model_json_schema(), indent=2, ensure_ascii=False))
