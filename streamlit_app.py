import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Explorador de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()

st.title("Explorador de operación")
st.caption("Aplicación inicial para explorar resultados por área y región.")

# TODO OBLIGATORIO: escribe tu nombre completo.
st.write("**Desarrollado por:** Gerardo Jasael Castrejon Rios**")
st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles,
)

df_filtrado = df[df["Área"].isin(areas_seleccionadas)].copy()

st.subheader("Datos disponibles")
st.dataframe(df_filtrado, width="stretch", hide_index=True)

casos_por_fecha = (
    df_filtrado.groupby("Fecha", as_index=False)["Casos"]
    .sum()
    .sort_values("Fecha")
)

fig = px.line(
    casos_por_fecha,
    x="Fecha",
    y="Casos",
    markers=True,
    title="Casos por fecha",
)
st.plotly_chart(fig, width="stretch")

st.info(
    "Esta es la versión inicial. Selecciona una opción de la actividad y agrega "
    "una mejora funcional para el usuario."
)


# ================================================================
# OPCIÓN A: TABLERO EJECUTIVO
# ================================================================

# Filtro adicional: Rango de fechas
st.sidebar.subheader("Rango de fechas")
fecha_min = df_filtrado["Fecha"].min()
fecha_max = df_filtrado["Fecha"].max()

col1, col2 = st.sidebar.columns(2)
with col1:
    fecha_inicio = st.date_input(
        "Desde",
        value=fecha_min,
        min_value=fecha_min,
        max_value=fecha_max
    )
with col2:
    fecha_fin = st.date_input(
        "Hasta",
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )

# Aplicar filtro de fechas
df_filtrado = df_filtrado[
    (df_filtrado["Fecha"].dt.date >= fecha_inicio) &
    (df_filtrado["Fecha"].dt.date <= fecha_fin)
]

# Crear dos vistas con tabs
tab1, tab2 = st.tabs(["📊 Métricas Ejecutivas", "📋 Datos Detallados"])

with tab1:
    st.subheader("Indicadores clave del período")
    
    # Calcular métricas
    total_casos = df_filtrado["Casos"].sum()
    casos_promedio = df_filtrado["Casos"].mean()
    
    # Mostrar indicadores con st.metric
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total de casos",
            value=int(total_casos),
            delta=f"{total_casos / df['Casos'].sum() * 100:.1f}% del total general"
        )
    with col2:
        st.metric(
            label="Casos promedio por fecha",
            value=f"{casos_promedio:.1f}",
            delta="Promedio del período"
        )
    
    # Gráfico de tendencia en tab 1
    st.subheader("Tendencia de casos")
    casos_por_fecha = (
        df_filtrado.groupby("Fecha", as_index=False)["Casos"]
        .sum()
        .sort_values("Fecha")
    )
    
    fig = px.line(
        casos_por_fecha,
        x="Fecha",
        y="Casos",
        markers=True,
        title="Evolución de casos en el período",
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribución por área
    st.subheader("Distribución por área")
    casos_por_area = (
        df_filtrado.groupby("Área", as_index=False)["Casos"]
        .sum()
        .sort_values("Casos", ascending=False)
    )
    
    fig_area = px.bar(
        casos_por_area,
        x="Área",
        y="Casos",
        title="Casos por área",
        color="Casos",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_area, use_container_width=True)

with tab2:
    st.subheader("Datos completos del período")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    
    # Estadísticas adicionales
    st.subheader("Resumen estadístico")
    st.write(df_filtrado[["Casos"]].describe())
