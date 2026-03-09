# src/app.py
from __future__ import annotations

from pathlib import Path
import pandas as pd

from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool

from src.schemas import InputSchema, OutputSchema
from src.clean_schemas import CleanRequest, CleanResponse
from src.limpieza import pipeline_limpieza_completa

from src.missing_data import (
    filtrar_paises_exceso_missing,
    run_mice_panel,
    resumen_imputacion,
)

RUTA_PROCESADO = Path("data/processed/global_crisis_data_clean.csv")

RUTA_RAW = Path("data/raw/global_crisis_data.csv")

RUTA_IMPUTED_ORIGINAL = Path(
    "data/processed/global_crisis_data_imputed_original.csv"
)

RUTA_IMPUTED_FILTERED = Path(
    "data/processed/global_crisis_data_imputed_filtered.csv"
)

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

def _run_missing_pipeline() -> dict:

    if not RUTA_RAW.exists():
        raise HTTPException(
            status_code=500,
            detail="No se encontró el dataset raw"
        )

    df = pd.read_csv(RUTA_RAW)

    # -------------------
    # Filtrar países
    # -------------------
    df_filtered, countries_to_drop, _ = filtrar_paises_exceso_missing(df)

    # -------------------
    # MICE base original
    # -------------------
    df_imputed_orig, _ = run_mice_panel(df)

    # -------------------
    # MICE base filtrada
    # -------------------
    df_imputed_filt, _ = run_mice_panel(df_filtered)

    # -------------------
    # Guardar datasets
    # -------------------
    RUTA_IMPUTED_ORIGINAL.parent.mkdir(parents=True, exist_ok=True)

    df_imputed_orig.to_csv(RUTA_IMPUTED_ORIGINAL, index=False)
    df_imputed_filt.to_csv(RUTA_IMPUTED_FILTERED, index=False)

    # -------------------
    # Resumen imputación
    # -------------------
    summary_orig = resumen_imputacion(df, df_imputed_orig, base_name="original")
    summary_filt = resumen_imputacion(df_filtered, df_imputed_filt, base_name="filtered")

    summary = pd.concat([summary_orig, summary_filt], ignore_index=True)

    return {
        "countries_removed": countries_to_drop,
        "rows_original": len(df),
        "rows_filtered": len(df_filtered),
        "summary": summary.to_dict(orient="records"),
        "saved_files": [
            str(RUTA_IMPUTED_ORIGINAL),
            str(RUTA_IMPUTED_FILTERED),
        ],
    }

@app.post("/clean", response_model=CleanResponse)
async def clean_endpoint(payload: CleanRequest) -> CleanResponse:
    """
    Aplica el pipeline de limpieza a una lista de filas.
    """
    raw_rows = [r.model_dump() for r in payload.rows]
    cleaned = await run_in_threadpool(_clean_rows, raw_rows)

    return CleanResponse(rows=cleaned)

@app.post("/impute-missing")
async def impute_missing() -> dict:
    """
    Ejecuta el pipeline de imputación MICE
    sobre el dataset completo.
    """

    result = await run_in_threadpool(_run_missing_pipeline)

    return result