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

def run_multiple_mice_panel(
    data,
    study_vars=None,
    country_col="iso3",
    time_col="year",
    random_state=0,
    max_iter=20,
    n_imputations=5
):
    if study_vars is None:
        study_vars = STUDY_VARS

    data = data.copy()
    missing_mask = data[study_vars].isnull()

    country_dummies = pd.get_dummies(
        data[country_col],
        prefix=country_col,
        drop_first=False
    )

    X = pd.concat(
        [data[[time_col] + study_vars], country_dummies],
        axis=1
    )

    imputed_datasets = []

    for i in range(n_imputations):
        imputer = IterativeImputer(
            max_iter=max_iter,
            random_state=random_state + i,
            sample_posterior=True
        )

        X_imputed = pd.DataFrame(
            imputer.fit_transform(X),
            columns=X.columns,
            index=X.index
        )

        # Restricciones económicas
        if "inflation" in study_vars:
            X_imputed["inflation"] = X_imputed["inflation"].clip(-100, 500)

        if "gdp_growth" in study_vars:
            X_imputed["gdp_growth"] = X_imputed["gdp_growth"].clip(-50, 50)

        if "unemployment" in study_vars:
            X_imputed["unemployment"] = X_imputed["unemployment"].clip(0, 40)

        data_imputed = data.copy()
        data_imputed[study_vars] = X_imputed[study_vars]

        data_imputed["imputation_id"] = i + 1
        imputed_datasets.append(data_imputed)

    return imputed_datasets, missing_mask

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

def run_multiple_mice_by_country(
    data,
    study_vars=None,
    country_col="iso3",
    time_col="year",
    random_state=0,
    max_iter=20,
    n_imputations=5
):
    if study_vars is None:
        study_vars = STUDY_VARS

    data = data.copy()
    all_imputations = []

    countries = data[country_col].unique()

    for i in range(n_imputations):
        country_results = []

        for country in countries:
            df_c = data[data[country_col] == country].copy()

            # variables con al menos 2 observaciones no nulas en ese país
            usable_vars = [var for var in study_vars if df_c[var].notnull().sum() >= 2]

            # si no hay variables suficientes, dejar el país tal cual
            if len(usable_vars) == 0:
                df_c["imputation_id"] = i + 1
                country_results.append(df_c)
                continue

            X = df_c[[time_col] + usable_vars].copy()

            imputer = IterativeImputer(
                max_iter=max_iter,
                random_state=random_state + i,
                sample_posterior=True
            )

            X_imputed_array = imputer.fit_transform(X)

            X_imputed = pd.DataFrame(
                X_imputed_array,
                columns=X.columns,
                index=X.index
            )

            # Restricciones económicas
            if "inflation" in usable_vars:
                X_imputed["inflation"] = X_imputed["inflation"].clip(-100, 500)

            if "gdp_growth" in usable_vars:
                X_imputed["gdp_growth"] = X_imputed["gdp_growth"].clip(-50, 50)

            if "unemployment" in usable_vars:
                X_imputed["unemployment"] = X_imputed["unemployment"].clip(0, 40)

            # solo reemplazar variables imputadas/usables
            df_c[usable_vars] = X_imputed[usable_vars]
            df_c["imputation_id"] = i + 1

            country_results.append(df_c)

        df_imputed = pd.concat(country_results, ignore_index=True)
        all_imputations.append(df_imputed)

    return all_imputations

def promediar_imputaciones(
    imputed_datasets: list[pd.DataFrame],
    id_cols: list[str] = ["iso3", "year"],
) -> pd.DataFrame:
    """
    Promedia múltiples imputaciones por fila identificada por id_cols.
    Devuelve un único DataFrame consolidado.
    """
    if not imputed_datasets:
        raise ValueError("La lista de imputaciones está vacía.")

    df_concat = pd.concat(imputed_datasets, ignore_index=True)

    # columnas numéricas a promediar, excluyendo identificadores e imputation_id
    numeric_cols = df_concat.select_dtypes(include="number").columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in id_cols + ["imputation_id"]]

    # promedio de variables numéricas imputadas
    df_mean = (
        df_concat.groupby(id_cols, as_index=False)[numeric_cols]
        .mean()
    )

    # conservar columnas no numéricas + identificadores desde la primera imputación
    base_cols = [col for col in imputed_datasets[0].columns if col not in numeric_cols + ["imputation_id"]]
    base_unique = imputed_datasets[0][base_cols].drop_duplicates(subset=id_cols)

    df_final = base_unique.merge(df_mean, on=id_cols, how="inner")
    df_final["year"] = df_final["year"].astype("Int64")

    return df_final