"""
Script para generar gráficos profesionales del EDA.
Salida: docs/img/*.png
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar estilo profesional
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 7)
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12

RUTA_PROCESADO = Path("data/processed/global_crisis_data_clean.csv")
RUTA_RAW = Path("data/raw/global_crisis_data.csv")
RUTA_IMG = Path("docs/img")
RUTA_IMG.mkdir(parents=True, exist_ok=True)

def main() -> int:
    print("🎨 Generando gráficos EDA profesionales...")
    
    # Cargar datos
    if not RUTA_PROCESADO.exists():
        print(f"❌ No se encontró {RUTA_PROCESADO}")
        return 1
    
    df = pd.read_csv(RUTA_PROCESADO)
    raw = pd.read_csv(RUTA_RAW)
    
    cols_num = ["inflation", "gdp_growth", "unemployment", "fed_funds_rate", "real_interest_rate_10y"]
    
    # ========================================================
    # 1. Histograma de Inflación
    # ========================================================
    plt.figure(figsize=(12, 6))
    plt.hist(df["inflation"].dropna(), bins=50, color="#2E86AB", alpha=0.8, edgecolor="black")
    plt.xlabel("Inflación (%)", fontsize=12, fontweight="bold")
    plt.ylabel("Frecuencia", fontsize=12, fontweight="bold")
    plt.title("Distribución de Inflación (Datos Procesados)", fontsize=14, fontweight="bold", pad=20)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "inflation_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: inflation_distribution.png")
    
    # ========================================================
    # 2. Histograma de Crecimiento del PIB
    # ========================================================
    plt.figure(figsize=(12, 6))
    plt.hist(df["gdp_growth"].dropna(), bins=50, color="#A23B72", alpha=0.8, edgecolor="black")
    plt.xlabel("Crecimiento del PIB (%)", fontsize=12, fontweight="bold")
    plt.ylabel("Frecuencia", fontsize=12, fontweight="bold")
    plt.title("Distribución de Crecimiento del PIB (Datos Procesados)", fontsize=14, fontweight="bold", pad=20)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "gdp_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: gdp_distribution.png")
    
    # ========================================================
    # 3. Matriz de Correlación (Heatmap)
    # ========================================================
    corr = df[cols_num].corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"label": "Correlación"},
        vmin=-1, vmax=1
    )
    plt.title("Matriz de Correlación - Variables Numéricas", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "correlation_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: correlation_heatmap.png")
    
    # ========================================================
    # 4. Comparación Crisis vs Sin Crisis (Violín plots)
    # ========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Inflación
    sns.violinplot(data=df, x="crisis_any", y="inflation", ax=axes[0], palette=["#06A77D", "#D62839"])
    axes[0].set_xlabel("Crisis", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Inflación (%)", fontsize=11, fontweight="bold")
    axes[0].set_title("Inflación: Con vs Sin Crisis", fontsize=12, fontweight="bold")
    axes[0].set_xticklabels(["Sin Crisis", "Con Crisis"])
    axes[0].grid(axis="y", alpha=0.3)
    
    # GDP Growth
    sns.violinplot(data=df, x="crisis_any", y="gdp_growth", ax=axes[1], palette=["#06A77D", "#D62839"])
    axes[1].set_xlabel("Crisis", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Crecimiento PIB (%)", fontsize=11, fontweight="bold")
    axes[1].set_title("GDP Growth: Con vs Sin Crisis", fontsize=12, fontweight="bold")
    axes[1].set_xticklabels(["Sin Crisis", "Con Crisis"])
    axes[1].grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "crisis_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: crisis_comparison.png")
    
    # ========================================================
    # 5. Impacto del Tratamiento de Outliers
    # ========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    max_raw = pd.to_numeric(raw["inflation"], errors="coerce").max()
    max_proc = pd.to_numeric(df["inflation"], errors="coerce").max()
    
    categories = ["RAW", "PROCESADO"]
    values = [max_raw, max_proc]
    colors = ["#E74C3C", "#27AE60"]
    
    axes[0].bar(categories, values, color=colors, alpha=0.8, edgecolor="black", linewidth=2)
    axes[0].set_ylabel("Máximo de Inflación (%)", fontsize=11, fontweight="bold")
    axes[0].set_title("Efecto del Tratamiento de Outliers", fontsize=12, fontweight="bold")
    axes[0].grid(axis="y", alpha=0.3)
    for i, v in enumerate(values):
        axes[0].text(i, v + 200, f"{v:.0f}%", ha="center", va="bottom", fontweight="bold")
    
    # Percentiles
    percentiles = [1, 5, 25, 50, 75, 95, 99]
    values_raw = [pd.to_numeric(raw["inflation"], errors="coerce").quantile(p/100) for p in percentiles]
    values_proc = [df["inflation"].quantile(p/100) for p in percentiles]
    
    x = np.arange(len(percentiles))
    width = 0.35
    
    axes[1].bar(x - width/2, values_raw, width, label="RAW", color="#E74C3C", alpha=0.8, edgecolor="black")
    axes[1].bar(x + width/2, values_proc, width, label="PROCESADO", color="#27AE60", alpha=0.8, edgecolor="black")
    axes[1].set_xlabel("Percentil", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Inflación (%)", fontsize=11, fontweight="bold")
    axes[1].set_title("Comparación de Percentiles", fontsize=12, fontweight="bold")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(percentiles)
    axes[1].legend()
    axes[1].grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "outliers_treatment.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: outliers_treatment.png")
    
    # ========================================================
    # 6. Balance de Variables Binarias de Crisis
    # ========================================================
    cols_binarias = ["crisis_any", "banking_crisis", "currency_crisis", "debt_crisis"]
    balance_data = []
    
    for col in cols_binarias:
        if col in df.columns:
            counts = df[col].value_counts()
            if len(counts) == 2:
                pct_crisis = (counts.get(1, 0) / len(df)) * 100
                balance_data.append(pct_crisis)
            else:
                balance_data.append(0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(cols_binarias, balance_data, color=["#D62839", "#A23B72", "#F18F01", "#C73E1D"], alpha=0.8, edgecolor="black")
    ax.set_xlabel("Porcentaje de Eventos (%) ", fontsize=12, fontweight="bold")
    ax.set_title("Balance de Variables de Crisis", fontsize=14, fontweight="bold", pad=20)
    ax.grid(axis="x", alpha=0.3)
    
    # Agregar valores en las barras
    for i, (bar, val) in enumerate(zip(bars, balance_data)):
        ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "crisis_balance.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: crisis_balance.png")
    
    # ========================================================
    # 7. Resumen Descriptivo (valores nulos)
    # ========================================================
    nulos_pct = (df[cols_num].isnull().mean() * 100).sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_nulos = ["#E74C3C" if x > 50 else "#F39C12" if x > 20 else "#27AE60" for x in nulos_pct.values]
    bars = ax.barh(nulos_pct.index, nulos_pct.values, color=colors_nulos, alpha=0.8, edgecolor="black")
    ax.set_xlabel("Porcentaje de Valores Nulos (%)", fontsize=12, fontweight="bold")
    ax.set_title("Calidad de Datos - Valores Faltantes", fontsize=14, fontweight="bold", pad=20)
    ax.grid(axis="x", alpha=0.3)
    
    # Agregar valores en las barras
    for i, (bar, val) in enumerate(zip(bars, nulos_pct.values)):
        ax.text(val + 1, i, f"{val:.1f}%", va="center", fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "missing_data.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: missing_data.png")
    
    # ========================================================
    # 8. Serie Temporal: Crédito Bancario por Año
    # ========================================================
    crisis_by_year = df.groupby("year")["crisis_any"].mean() * 100
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(crisis_by_year.index, crisis_by_year.values, linewidth=2.5, color="#2E86AB", marker="o", markersize=4)
    ax.fill_between(crisis_by_year.index, crisis_by_year.values, alpha=0.3, color="#2E86AB")
    ax.set_xlabel("Año", fontsize=12, fontweight="bold")
    ax.set_ylabel("Porcentaje de Países en Crisis (%)", fontsize=12, fontweight="bold")
    ax.set_title("Tendencia de Crisis Financieras por Año", fontsize=14, fontweight="bold", pad=20)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(RUTA_IMG / "crisis_timeline.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Gráfico: crisis_timeline.png")
    
    print("\n✅ Todos los gráficos han sido generados exitosamente en docs/img/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
