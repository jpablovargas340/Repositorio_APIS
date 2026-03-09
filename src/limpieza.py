from __future__ import annotations

import pandas as pd


def estandarizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina espacios en nombres de columnas.
    """
    df_copia = df.copy()
    df_copia.columns = [col.strip() for col in df_copia.columns]
    return df_copia


def limpiar_iso3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y estandariza la columna ISO3.
    """
    df_copia = df.copy()
    df_copia["iso3"] = df_copia["iso3"].astype(str).str.strip().str.upper()
    return df_copia


def convertir_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte la columna year a entero nullable.
    """
    df_copia = df.copy()
    df_copia["year"] = pd.to_numeric(df_copia["year"], errors="coerce").astype("Int64")
    return df_copia


def pipeline_limpieza_basica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica la limpieza básica encadenada.
    """
    df_limpio = estandarizar_columnas(df)
    df_limpio = limpiar_iso3(df_limpio)
    df_limpio = convertir_year(df_limpio)
    return df_limpio


def pipeline_limpieza_completa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza básica únicamente.
    No modifica outliers.
    """
    return pipeline_limpieza_basica(df)