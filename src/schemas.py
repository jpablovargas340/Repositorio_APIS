# src/schemas.py
from __future__ import annotations

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator, StrictInt, StrictStr


class InputSchema(BaseModel):
    """
    Request para buscar una observación país-año en el dataset.
    """
    model_config = ConfigDict(extra="forbid")

    iso3: StrictStr = Field(..., description="Código ISO3 del país, ej: 'COL'")
    year: StrictInt = Field(..., ge=1800, le=2100, description="Año (ej: 1999)")

    @field_validator("iso3")
    @classmethod
    def normalize_iso3(cls, v: str) -> str:
        v2 = v.strip().upper()
        if len(v2) != 3:
            raise ValueError("iso3 debe tener longitud 3 (ej: 'COL')")
        return v2


class OutputSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    iso3: str
    year: int
    inflation: Optional[float] = None
    gdp_growth: Optional[float] = None
    unemployment: Optional[float] = None
    real_interest_rate_10y: Optional[float] = None
    crisis_any: Optional[int] = None
    banking_crisis: Optional[int] = None
    found: bool = True
    meta: Dict[str, Any] = Field(default_factory=dict)