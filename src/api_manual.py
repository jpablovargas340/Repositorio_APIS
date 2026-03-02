from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
from pydantic import ValidationError

from src.schemas import InputSchema, OutputSchema

RUTA_PROCESADO = Path("data/processed/global_crisis_data_clean.csv")

def handle_request(json_str: str) -> dict:
    try:
        payload = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"ok": False, "status": 400, "error": "JSON inválido", "detail": str(e)}

    try:
        req = InputSchema.model_validate(payload)
    except ValidationError as e:
        return {"ok": False, "status": 422, "error": "Validación fallida", "detail": e.errors()}

    if not RUTA_PROCESADO.exists():
        return {
            "ok": False,
            "status": 500,
            "error": "Dataset procesado no existe",
            "detail": f"No se encontró {RUTA_PROCESADO.as_posix()} (ejecuta python -m scripts.make_dataset)",
        }

    df = pd.read_csv(RUTA_PROCESADO)

    # Ajusta nombres de columnas si difieren
    mask = (df["iso3"].astype(str).str.strip().str.upper() == req.iso3) & (df["year"] == req.year)
    match = df.loc[mask]

    if match.empty:
        out = OutputSchema(
            iso3=req.iso3,
            year=req.year,
            found=False,
            meta={"message": "No hay registro para ese iso3-year"},
        )
        return {"ok": True, "status": 200, "data": out.model_dump()}

    row = match.iloc[0].to_dict()
    row["iso3"] = req.iso3
    row["year"] = req.year
    row["found"] = True

    out = OutputSchema(**row)
    return {"ok": True, "status": 200, "data": out.model_dump()}