# src/app.py
from __future__ import annotations

from pathlib import Path
import pandas as pd

from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool

from src.schemas import InputSchema, OutputSchema
from src.clean_schemas import CleanRequest, CleanResponse
from src.limpieza import pipeline_limpieza_completa


RUTA_PROCESADO = Path("data/processed/global_crisis_data_clean.csv")

app = FastAPI(
    title="API Crisis Financieras Globales",
    version="1.0.0",
    description="FastAPI + Pydantic con documentación automática (/docs, /redoc).",
)

# =========================================================
# Root
# =========================================================

@app.get("/")
def root() -> dict:
    return {
        "message": "API Crisis Financieras - OK",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health() -> dict:
    return {"ok": True}


# =========================================================
# Endpoint: Consultar fila procesada
# =========================================================

def _lookup_row(iso3: str, year: int) -> OutputSchema:
    if not RUTA_PROCESADO.exists():
        raise HTTPException(
            status_code=500,
            detail=f"No se encontró {RUTA_PROCESADO.as_posix()} (ejecuta: python -m scripts.make_dataset)",
        )

    df = pd.read_csv(RUTA_PROCESADO)

    mask = (
        df["iso3"].astype(str).str.strip().str.upper() == iso3
    ) & (df["year"] == year)

    match = df.loc[mask]

    if match.empty:
        return OutputSchema(
            iso3=iso3,
            year=year,
            found=False,
            meta={"message": "No hay registro para ese iso3-year"},
        )

    row = match.iloc[0].to_dict()
    row["iso3"] = iso3
    row["year"] = year
    row["found"] = True

    return OutputSchema(**row)


@app.post("/row", response_model=OutputSchema)
async def get_row(payload: InputSchema) -> OutputSchema:
    """
    Consulta una fila del dataset procesado por iso3-año.
    """
    return await run_in_threadpool(_lookup_row, payload.iso3, payload.year)


# =========================================================
# Endpoint: Limpieza + Tratamiento de Outliers
# =========================================================

def _clean_rows(rows: list[dict]) -> list[dict]:
    df_in = pd.DataFrame(rows)

    # Aplicar pipeline completo
    df_out = pipeline_limpieza_completa(df_in)

    # Convertir NaN / Int64 pandas a JSON-friendly
    df_out = df_out.where(pd.notnull(df_out), None)

    return df_out.to_dict(orient="records")


@app.post("/clean", response_model=CleanResponse)
async def clean_endpoint(payload: CleanRequest) -> CleanResponse:
    """
    Aplica el pipeline de limpieza a una lista de filas.
    """
    raw_rows = [r.model_dump() for r in payload.rows]
    cleaned = await run_in_threadpool(_clean_rows, raw_rows)

    return CleanResponse(rows=cleaned)