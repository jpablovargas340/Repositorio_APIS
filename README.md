# 📊 Global Crisis Dataset — Análisis Académico

## 📌 Descripción General

Este proyecto desarrolla un pipeline reproducible y modular para el análisis del dataset de crisis financieras globales.

Incluye:

- Limpieza estructurada del dataset
- Tratamiento sistemático de outliers
- Análisis Exploratorio de Datos (EDA)
- Validación estructural y calidad de datos
- Testing automatizado con pytest
- Uso de tipado estricto y decoradores personalizados

El objetivo es garantizar un proceso transparente, reproducible y metodológicamente sólido.

---

## 🗂 Estructura del Proyecto

Repositorio_APIS/
│
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_eda.ipynb
├── docs/
│   └── img/
├── src/
│   ├── limpieza.py
│   ├── outliers.py
│   ├── estadisticas.py
│   └── decoradores.py
├── scripts/
│   └── make_dataset.py
├── tests/
├── requirements.txt
└── README.md

---

## ⚙️ Reproducibilidad

### Crear entorno virtual

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Generar dataset procesado

```bash
python -m scripts.make_dataset
```

### Ejecutar tests

```bash
pytest -q
```

---

## 📊 Análisis Exploratorio (EDA)

El análisis completo se encuentra en:

notebooks/01_eda.ipynb

---

## 🔎 Calidad de Datos

- 3864 observaciones.
- Cobertura longitudinal por país–año.
- Variables macroeconómicas con nulos relevantes (`unemployment`, `real_interest_rate_10y`).

---

## 📉 Tratamiento de Outliers

Se aplicó recorte por cuantiles (1%–99%) a:

- inflation
- gdp_growth

Evidencia empírica:

- Máx inflación RAW ≈ 11749
- Máx inflación PROCESADO ≈ 228

Este procedimiento reduce la influencia de valores extremos sin eliminar observaciones.

---

## ⚠️ Variables de Crisis

Las variables binarias presentan fuerte desbalance (predominio de no-crisis).

Esto implica que futuros modelos predictivos deberán manejar el problema de class imbalance.

---

## 📈 Relaciones Observadas

En años con crisis:

- Inflación tiende a ser mayor.
- Crecimiento del PIB tiende a ser menor.

Los resultados descriptivos son coherentes con teoría macroeconómica.

---

## 🧪 Calidad del Código

- Funciones puras
- Modularización clara
- Tipado estático estricto
- Decoradores personalizados
- Testing automatizado

---

## 🎯 Conclusión Académica

El dataset presenta estructura adecuada para análisis tipo panel y modelado predictivo.

El tratamiento de outliers mejora la estabilidad estadística y la interpretación de resultados.

Las limitaciones principales se centran en la presencia de valores faltantes y desbalance en variables de crisis.

El pipeline desarrollado garantiza reproducibilidad y trazabilidad metodológica.
