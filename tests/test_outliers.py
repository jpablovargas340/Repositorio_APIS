from __future__ import annotations

import pandas as pd

from src.outliers import recortar_cuantiles, recortar_iqr


def test_recortar_cuantiles_no_muta_df_original() -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 1000]})
    df_original = df.copy(deep=True)

    _ = recortar_cuantiles(df, "x", 0.0, 0.75)

    assert df.equals(df_original)


def test_recortar_cuantiles_recorta_extremo_superior() -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 1000]})

    # Cuantil superior esperado según pandas
    esperado = float(pd.Series([1, 2, 3, 1000]).quantile(0.75))

    df2 = recortar_cuantiles(df, "x", 0.0, 0.75)

    # Debe recortar el máximo al cuantil calculado (o menor)
    assert float(df2["x"].max()) <= esperado + 1e-9

    # Y debe ser menor que el máximo original
    assert float(df2["x"].max()) < float(df["x"].max())


def test_recortar_iqr_funciona() -> None:
    df = pd.DataFrame({"x": [10, 11, 12, 13, 1000]})
    df2 = recortar_iqr(df, "x", k=1.5)

    # el 1000 debería recortarse
    assert df2["x"].max() < 1000