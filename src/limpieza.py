from __future__ import annotations

import pandas as pd


# -------------------------
# LIMPIEZA BÁSICA
# -------------------------

def estandarizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]
    return df


def limpiar_iso3(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "iso3" not in df.columns:
        raise KeyError("La columna 'iso3' no existe.")

    df["iso3"] = df["iso3"].astype(str).str.strip().str.upper()
    return df


def convertir_year(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "year" not in df.columns:
        raise KeyError("La columna 'year' no existe.")

    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df


def pipeline_limpieza_basica(df: pd.DataFrame) -> pd.DataFrame:
    df = estandarizar_columnas(df)
    df = limpiar_iso3(df)
    df = convertir_year(df)
    return df


# -------------------------
# VALIDACIÓN PANEL
# -------------------------

def validar_panel_base(df: pd.DataFrame) -> dict:
    """
    Valida estructura panel ISO3-YEAR.
    No modifica datos, solo reporta.
    """
    resultados = {}

    # Nulos
    resultados["nulos_iso3"] = int(df["iso3"].isnull().sum())
    resultados["nulos_year"] = int(df["year"].isnull().sum())

    # Duplicados
    resultados["duplicados_panel"] = int(df.duplicated(subset=["iso3", "year"]).sum())

    # Rango de años
    resultados["year_min"] = int(df["year"].min())
    resultados["year_max"] = int(df["year"].max())

    # Longitud ISO3
    resultados["iso3_len_dist"] = (
        df["iso3"].dropna().astype(str).str.len().value_counts().to_dict()
    )

    return resultados


# -------------------------
# PIPELINE COMPLETO
# -------------------------

def pipeline_limpieza_completa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza + validación.
    """
    df = pipeline_limpieza_basica(df)

    # Validación (solo reporte)
    resumen = validar_panel_base(df)

    print("VALIDACIÓN PANEL:")
    for k, v in resumen.items():
        print(f"{k}: {v}")

    return df