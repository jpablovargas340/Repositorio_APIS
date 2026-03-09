# 🌐 GitHub Pages - Global Crisis Analyzer

## Cómo Activar GitHub Pages

Esta página web está alojada en la carpeta `/docs` del repositorio. Para activarla en GitHub Pages:

### Paso 1: Configurar GitHub Pages en Settings

1. Ve a tu repositorio en GitHub
2. Click en **Settings** → **Pages**
3. En **Source**, selecciona:
   - **Branch:** `main` (o `master`)
   - **Folder:** `/docs`
4. Click en **Save**

GitHub automáticamente construirá y publicará tu sitio en:
```
https://<tu-usuario>.github.io/Repositorio_APIS/
```

### Paso 2: Verificar la Publicación

El sitio estará disponible en pocos minutos. GitHubPages enviará un email de confirmación.

## Estructura de Archivos

```
docs/
├── index.html              # Página principal (entrada)
├── css/
│   └── style.css          # Estilos profesionales (900+ líneas)
├── img/                    # Gráficos EDA
│   ├── inflation_distribution.png
│   ├── gdp_distribution.png
│   ├── correlation_heatmap.png
│   ├── crisis_comparison.png
│   ├── outliers_treatment.png
│   ├── crisis_balance.png
│   ├── missing_data.png
│   └── crisis_timeline.png
├── _config.yml            # Configuración Jekyll (opcional)
└── README.md              # Este archivo
```

## Características de la Página

✅ **Responsive Design** - Se adapta a móvil, tablet y desktop
✅ **Documentación Completa** - Explicación del proyecto, EDA, APIs
✅ **Gráficos Profesionales** - Histogramas, correlaciones, comparativas
✅ **Documentación API** - Endpoints, requests/responses, ejemplos
✅ **Sin Dependencias Externas** - HTML5 puro + CSS custom (sin Bootstrap)
✅ **Navegación Smooth** - Links internos con scroll suave
✅ **Accesibilidad** - Semantic HTML, colores conformes WCAG

## Contenidos Incluidos

1. **Header Sticky** - Navegación siempre visible
2. **Hero Section** - Presentación del proyecto con estadísticas
3. **About** - Contexto, motivación, objetivos
4. **Features** - Características técnicas y stack
5. **EDA Section** - 7 gráficos profesionales comentados:
   - Distribuciones (Inflación, GDP)
   - Tratamiento de outliers
   - Matriz de correlación
   - Comparación Crisis vs Sin Crisis
   - Balance de variables
   - Calidad de datos
   - Timeline histórica
6. **API Documentation** - 5 endpoints documentados con ejemplos
7. **Technical Section** - Detalles de arquitectura, supuestos, reproducción
8. **Authors** - Información de Juan Pablo Vargas y Edward Mora
9. **Footer** - Enlaces, contacto, créditos

## Estilo Visual

### Paleta de Colores
- **Primario:** #2E86AB (Azul profesional)
- **Secundario:** #A23B72 (Púrpura académico)
- **Accent:** #F18F01 (Naranja dinámico)
- **Success:** #06A77D (Verde de validación)
- **Danger:** #D62839 (Rojo de alerta)

### Tipografía
- **Fuente:** System fonts (Apple, Google, sans-serif)
- **Tamaños:** H1=2.5rem, H2=2rem, H3=1.5rem, Body=1rem
- **Espaciado:** Generoso (1.8 line-height) para legibilidad

### Componentes
- Cards con hover effect (elevación)
- Alertas coloreadas (info, success, warning, danger)
- Botones con gradientes y transiciones
- Tablas con zebra striping
- Código preformateado con syntax coloring

## Prueba Local (Opcional)

Para probar antes de pushear:

```powershell
# Opción 1: Usar un servidor HTTP simple
cd docs
python -m http.server 8000

# Opción 2: Usar Live Server extension en VS Code
# Click derecho en index.html → Open with Live Server

# Luego navega a http://localhost:8000
```

## Personalización Futura

Si deseas personalizar la página:

1. **Colores:** Modifica `:root` en `css/style.css`
2. **Contenido:** Edita secciones directamente en `index.html`
3. **Gráficos:** Regenera con `python scripts/generate_eda_plots.py`
4. **Tema Jekyll:** Cambia `theme:` en `_config.yml`

## Notas Importantes

- ⚠️ Los cambios en `/docs` se publican automáticamente en ~1-2 minutos
- 🔒 El sitio es público (cualquiera puede verlo)
- 📱 Asegúrate de probar en móvil antes de mergear
- 🚀 Para vanity domain personalizado, configura en Settings → Pages → Custom Domain

## Soporte

Para más info sobre GitHub Pages:
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Configurar un sitio GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

---

**Creado:** Marzo 2025
**Autores:** Juan Pablo Vargas, Edward Mora
**Proyecto:** Global Crisis Analyzer - Análisis de Crisis Financieras Globales
