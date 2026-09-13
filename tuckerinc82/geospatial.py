from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SpatialReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    horizontal_crs: str = Field(min_length=1)
    vertical_datum: str | None = None
    units: str = Field(min_length=1)


class SpatialFeature(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feature_id: str = Field(min_length=1)
    geometry_type: str = Field(min_length=1)
    coordinates: list[float]
    spatial_reference: SpatialReference
    properties: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
