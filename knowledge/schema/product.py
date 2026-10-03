"""Base Product — Pydantic equivalent of `product.json`.

Modelled on https://schema.org/Product.
Do not validate category products directly against this file —
use the per-category file (e.g. `ac.py`).

JSON-Schema source:
    knowledge/schema/product.json
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Base product. All category schemas inherit from this."""

    model_config = ConfigDict(
        extra="forbid",  # == unevaluatedProperties: false
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    # JSON-LD context. Maps this record onto schema.org/Product.
    # Not in `required` in product.json, defaults to schema.org on export.
    context: str = Field(
        default="https://schema.org",
        alias="@context",
        description="JSON-LD context. Maps this record onto schema.org/Product.",
    )

    # schema:Product. Required in product.json (const).
    type: str = Field(
        default="Product",
        alias="@type",
        description="schema:Product.",
        pattern=r"^Product$",
    )

    # schema:name — canonical display name. e.g. 'LG DUALCOOL AI AS-Q20JWZE'.
    name: str = Field(min_length=1, description="schema:name — canonical display name.")

    # Maps to schema:alternateName (schema.org defines it singular;
    # we use a list for search aliases).
    alias_names: list[str] = Field(
        default_factory=list,
        description="Maps to schema:alternateName (list for search aliases).",
    )

    # Maps to schema:model + schema:mpn (Manufacturer Part Number).
    model_code: str = Field(
        min_length=1,
        description="Maps to schema:model + schema:mpn.",
    )

    # Maps to schema:manufacturer / schema:brand name. e.g. 'LG'.
    manufacturer: str = Field(
        min_length=1,
        description="Maps to schema:manufacturer / schema:brand name.",
    )

    # No direct schema.org equivalent. Predecessor model_code this variant
    # replaces. Pairs with schema:isVariantOf at export time.
    parent_version: str | None = Field(
        default=None,
        description="Predecessor model_code this variant replaces.",
    )

    # This record's version (semver or OEM revision, e.g. '2025.1').
    current_version: str = Field(
        min_length=1,
        description="This record's version (e.g. '2025.1').",
    )

    # Maps to schema:category. e.g. ['home-appliances', 'cooling'].
    sector: list[str] = Field(
        min_length=1,
        description="Maps to schema:category.",
    )
