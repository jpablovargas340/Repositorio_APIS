from __future__ import annotations

import pandas as pd


def limites_iqr(serie: pd.Series, k: float = 1.5) -> tuple[float, float]:
    """
    Calcula límites inferior/superior usando IQR (Q1 - k*IQR, Q3 + k*IQR).
    """
    s = pd.to_numeric(serie, errors="coerce").dropna()
    if s.empty:
        return (float("nan"), float("nan"))

    q1 = float(s.quantile(0.25))
    q3 = float(s.quantile(0.75))
    iqr = q3 - q1
    return (q1 - k * iqr, q3 + k * iqr)


def recortar_iqr(df: pd.DataFrame, columna: str, k: float = 1.5) -> pd.DataFrame:
    """
    Recorta (clip) los valores de una columna usando límites IQR.
    Función pura: no modifica df original.
    """
    df_copia = df.copy()

    lo, hi = limites_iqr(df_copia[columna], k=k)
    if pd.isna(lo) or pd.isna(hi):
        return df_copia

    df_copia[columna] = pd.to_numeric(df_copia[columna], errors="coerce").clip(lo, hi)
    return df_copia


def recortar_cuantiles(
    df: pd.DataFrame, columna: str, q_inf: float = 0.01, q_sup: float = 0.99
) -> pd.DataFrame:
    """
    Recorta (clip) valores usando cuantiles (winsor simple).
    Recomendado para inflación si hay valores extremos muy altos.
    Función pura.
    """
    df_copia = df.copy()

    s = pd.to_numeric(df_copia[columna], errors="coerce").dropna()
    if s.empty:
        return df_copia

    lo = float(s.quantile(q_inf))
    hi = float(s.quantile(q_sup))
    df_copia[columna] = pd.to_numeric(df_copia[columna], errors="coerce").clip(lo, hi)
    return df_copia