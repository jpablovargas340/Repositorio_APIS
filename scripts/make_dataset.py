from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.limpieza import pipeline_limpieza_completa

RUTA_RAW = Path("data/raw/global_crisis_data.csv")
RUTA_PROCESADO = Path("data/processed/global_crisis_data_clean.csv")


def main() -> int:
    if not RUTA_RAW.exists():
        print(f"ERROR: no se encontró el dataset en {RUTA_RAW.resolve()}")
        return 1

    df = pd.read_csv(RUTA_RAW)
    print(f"Dataset cargado con forma: {df.shape}")

    df_limpio = pipeline_limpieza_completa(df)

    RUTA_PROCESADO.parent.mkdir(parents=True, exist_ok=True)
    df_limpio.to_csv(RUTA_PROCESADO, index=False)

    print(f"Dataset procesado guardado en: {RUTA_PROCESADO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())