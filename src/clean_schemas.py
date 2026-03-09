from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator


class CleanRowIn(BaseModel):
    """
    Una fila (registro) que llega al endpoint /clean.
    Extra forbidden = validación estricta (no se aceptan campos inesperados).
    Strict types = no castea strings a números.
    """
    model_config = ConfigDict(extra="forbid")

    iso3: StrictStr = Field(..., description="Código ISO3, ej: COL")
    year: StrictInt = Field(..., ge=1800, le=2100, description="Año")

    inflation: Optional[StrictFloat] = None
    gdp_growth: Optional[StrictFloat] = None
    unemployment: Optional[StrictFloat] = None
    fed_funds_rate: Optional[StrictFloat] = None

    @field_validator("iso3")
    @classmethod
    def normalize_iso3(cls, v: str) -> str:
        v2 = v.strip().upper()
        if len(v2) != 3:
            raise ValueError("iso3 debe tener longitud 3 (ej: 'COL')")
        return v2


class CleanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rows: List[CleanRowIn] = Field(..., min_length=1)


class CleanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rows: list[dict]