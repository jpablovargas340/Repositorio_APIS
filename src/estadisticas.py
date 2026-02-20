from __future__ import annotations

import pandas as pd


def reporte_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve un DataFrame con porcentaje de nulos por columna.
    """
    return (
        df.isna()
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
        .rename("porcentaje_nulos")
        .to_frame()
    )


def resumen_numerico(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Resumen numérico estándar para columnas seleccionadas.
    """
    return df[columnas].describe().T


def balance_binaria(df: pd.DataFrame, columna: str) -> pd.Series:
    """
    Porcentaje por clase en una columna binaria.
    """
    return df[columna].value_counts(dropna=False, normalize=True).mul(100).round(2)