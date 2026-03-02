# src/schemas.py
from __future__ import annotations

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator


class InputSchema(BaseModel):
    """
    Request para buscar una observación país-año en el dataset.
    """
    model_config = ConfigDict(extra="forbid")

    iso3: str = Field(..., description="Código ISO3 del país, ej: 'COL'")
    year: int = Field(..., ge=1800, le=2100, description="Año (ej: 1999)")

    @field_validator("iso3")
    @classmethod
    def normalize_iso3(cls, v: str) -> str:
        v2 = v.strip().upper()
        if len(v2) != 3:
            raise ValueError("iso3 debe tener longitud 3 (ej: 'COL')")
        return v2


class OutputSchema(BaseModel):
    """
    Respuesta normalizada (serializable a JSON) de una fila del dataset.
    Ajusta campos según tus columnas reales.
    """
    model_config = ConfigDict(extra="allow")

    iso3: str
    year: int

    # Variables numéricas típicas mencionadas en tu README
    inflation: Optional[float] = None
    gdp_growth: Optional[float] = None
    unemployment: Optional[float] = None
    real_interest_rate_10y: Optional[float] = None

    # Flags de crisis (tu README menciona crisis_any, banking_crisis, etc.)
    crisis_any: Optional[int] = None
    banking_crisis: Optional[int] = None

    # Campo útil para debugging / mensajes
    found: bool = True
    meta: Dict[str, Any] = Field(default_factory=dict)