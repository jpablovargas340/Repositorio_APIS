from __future__ import annotations

import pandas as pd

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

STUDY_VARS = ["inflation", "gdp_growth", "unemployment", "fed_funds_rate"]


def filtrar_paises_exceso_missing(
    df: pd.DataFrame,
    study_vars: list[str] = STUDY_VARS,
    country_col: str = "iso3",
    threshold: float = 0.50,
    min_vars: int = 2,
) -> tuple[pd.DataFrame, list[str], pd.DataFrame]:
    """
    Elimina países con más del threshold de datos faltantes
    en al menos min_vars variables de estudio.
    """
    miss_by_country = df.groupby(country_col)[study_vars].apply(lambda x: x.isnull().mean())
    bad_country_count = (miss_by_country > threshold).sum(axis=1)
    countries_to_drop = bad_country_count[bad_country_count >= min_vars].index.tolist()
    df_filtered = df[~df[country_col].isin(countries_to_drop)].copy()

    return df_filtered, countries_to_drop, miss_by_country


def run_mice_panel(
    data: pd.DataFrame,
    study_vars: list[str] = STUDY_VARS,
    country_col: str = "iso3",
    time_col: str = "year",
    random_state: int = 0,
    max_iter: int = 20,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica imputación MICE incorporando estructura de panel:
    - year como variable temporal
    - dummies de país para distinguir países
    """
    data = data.copy()
    missing_mask = data[study_vars].isnull()

    country_dummies = pd.get_dummies(data[country_col], prefix=country_col, drop_first=False)
    X = pd.concat([data[[time_col] + study_vars], country_dummies], axis=1)

    imputer = IterativeImputer(
        max_iter=max_iter,
        random_state=random_state,
        sample_posterior=False,
    )

    X_imputed = pd.DataFrame(
        imputer.fit_transform(X),
        columns=X.columns,
        index=X.index,
    )

    data_imputed = data.copy()
    data_imputed[study_vars] = X_imputed[study_vars]

    if "unemployment" in study_vars:
        data_imputed["unemployment"] = data_imputed["unemployment"].clip(lower=0)

    return data_imputed, missing_mask


def resumen_imputacion(
    original_df: pd.DataFrame,
    imputed_df: pd.DataFrame,
    study_vars: list[str] = STUDY_VARS,
    base_name: str = "base",
) -> pd.DataFrame:
    """
    Resume medias, desviaciones y diferencias entre
    datos originales e imputados.
    """
    summary = pd.DataFrame({
        "variable": study_vars,
        "mean_original": original_df[study_vars].mean().values,
        "mean_imputed": imputed_df[study_vars].mean().values,
        "std_original": original_df[study_vars].std().values,
        "std_imputed": imputed_df[study_vars].std().values,
        "min_imputed": imputed_df[study_vars].min().values,
        "max_imputed": imputed_df[study_vars].max().values,
    })

    summary["diff_mean"] = summary["mean_imputed"] - summary["mean_original"]
    summary["diff_std"] = summary["std_imputed"] - summary["std_original"]
    summary["base"] = base_name

    return summary


def outliers_por_pais(
    df: pd.DataFrame,
    study_vars: list[str] = STUDY_VARS,
    country_col: str = "iso3",
) -> pd.DataFrame:
    """
    Detecta outliers por país usando criterio IQR.
    Solo diagnóstico: no modifica los datos.
    """
    results = []

    for var in study_vars:
        q1 = df[var].quantile(0.25)
        q3 = df[var].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        tmp = df.copy()
        tmp["outlier_flag"] = ((tmp[var] < lower) | (tmp[var] > upper)).astype(int)

        country_outliers = tmp.groupby(country_col)["outlier_flag"].agg(["sum", "count"]).reset_index()
        country_outliers["variable"] = var
        country_outliers["pct_outliers"] = (country_outliers["sum"] / country_outliers["count"]) * 100
        country_outliers = country_outliers.rename(columns={"sum": "n_outliers", "count": "n_obs"})

        results.append(country_outliers)

    final_table = pd.concat(results, ignore_index=True)
    final_table = final_table[final_table["n_outliers"] > 0]

    return final_table.sort_values(by=[country_col, "variable"]).reset_index(drop=True)