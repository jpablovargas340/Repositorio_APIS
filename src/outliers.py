from __future__ import annotations

import pandas as pd

from src.missing_data import STUDY_VARS


def outliers_por_pais(
    df: pd.DataFrame,
    study_vars: list[str] = STUDY_VARS,
    country_col: str = "iso3",
    time_col: str = "year",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detecta outliers por país y por variable usando criterio IQR dentro de cada país.

    Retorna:
    - detalle_outliers: observaciones outlier
    - resumen_outliers: resumen por país y variable
    """
    detalle = []
    resumen = []

    for var in study_vars:
        for country, group in df[[country_col, time_col, var]].dropna(subset=[var]).groupby(country_col):
            if group[var].shape[0] < 4:
                continue

            q1 = group[var].quantile(0.25)
            q3 = group[var].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            tmp = group.copy()
            tmp["lower_bound"] = lower
            tmp["upper_bound"] = upper
            tmp["outlier_flag"] = ((tmp[var] < lower) | (tmp[var] > upper))

            outliers = tmp[tmp["outlier_flag"]].copy()

            if not outliers.empty:
                outliers["variable"] = var
                outliers = outliers.rename(columns={var: "valor"})
                outliers["q1"] = q1
                outliers["q3"] = q3
                outliers["iqr"] = iqr

                detalle.append(
                    outliers[
                        [
                            country_col,
                            time_col,
                            "variable",
                            "valor",
                            "q1",
                            "q3",
                            "iqr",
                            "lower_bound",
                            "upper_bound",
                        ]
                    ]
                )

            resumen.append(
                pd.DataFrame(
                    {
                        country_col: [country],
                        "variable": [var],
                        "n_outliers": [int(tmp["outlier_flag"].sum())],
                        "n_obs": [int(tmp.shape[0])],
                        "pct_outliers": [float(tmp["outlier_flag"].mean() * 100)],
                    }
                )
            )

    detalle_outliers = (
        pd.concat(detalle, ignore_index=True)
        if detalle
        else pd.DataFrame(
            columns=[
                country_col,
                time_col,
                "variable",
                "valor",
                "q1",
                "q3",
                "iqr",
                "lower_bound",
                "upper_bound",
            ]
        )
    )

    resumen_outliers = (
        pd.concat(resumen, ignore_index=True)
        if resumen
        else pd.DataFrame(columns=[country_col, "variable", "n_outliers", "n_obs", "pct_outliers"])
    )

    resumen_outliers = resumen_outliers[resumen_outliers["n_outliers"] > 0].reset_index(drop=True)
    detalle_outliers = detalle_outliers.sort_values([country_col, "variable", time_col]).reset_index(drop=True)

    return detalle_outliers, resumen_outliers