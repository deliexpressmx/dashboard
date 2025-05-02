import streamlit as st
import pandas as pd
from supabase import create_client

# 0. Configuración de la página en modo wide
st.set_page_config(page_title="Uso y Costo por Ingrediente", layout="wide")

# 1. Conexión a Supabase
def get_supabase_client():
    url = "https://ipwhnkvepshnbrpymwmn.supabase.co"
    key = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwd2hua3ZlcHNobmJycHltd21uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMjA0MzksImV4cCI6MjA1OTc5NjQzOX0."
        "R7QApURC5kdpjjXDKasQdtDQBIL_C6xnuSdqcDuZpBM"
    )
    return create_client(url, key)

supabase = get_supabase_client()

# 2. Carga de datos desde la tabla 'inventario' por batches
@st.cache_data
def load_data():
    batch_size = 1000
    offset = 0
    all_data = []
    while True:
        resp = supabase.table("inventario").select("*").range(offset, offset + batch_size - 1).execute()
        if getattr(resp, "error", None):
            st.error(f"Error al cargar datos de inventario: {resp.error.message}")
            return pd.DataFrame()
        data = resp.data or []
        all_data.extend(data)
        if len(data) < batch_size:
            break
        offset += batch_size
    df = pd.DataFrame(all_data)
    df["fecha_inicio"] = pd.to_datetime(df.get("fecha_inicio"), errors="coerce")
    df["fecha_final"]  = pd.to_datetime(df.get("fecha_final"),  errors="coerce")
    return df

# Obtener datos
df = load_data()

# 3. Sidebar: filtros
st.sidebar.header("Filtros")

# 4. Selector de fecha inicio y fecha final
date_min, date_max = df["fecha_inicio"].min(), df["fecha_final"].max()
start_date = st.sidebar.date_input("Fecha inicio:", value=date_min.date())
end_date   = st.sidebar.date_input("Fecha final:",  value=date_max.date())
start_ts, end_ts = pd.Timestamp(start_date), pd.Timestamp(end_date)

# 5. Selector múltiple de ingredientes
ingredientes = df["ingrediente"].dropna().unique().tolist()
seleccionados = st.sidebar.multiselect(
    "Ingrediente(s):",
    options=ingredientes,
    key="ingredientes_filter"
)

# 6. Filtrado de datos por solapamiento de rangos
df_filtrado = df[
    (df["fecha_inicio"] <= end_ts) &
    (df["fecha_final"]  >= start_ts) &
    (df["ingrediente"].isin(seleccionados))
]

# 7. Agrupar y resumir
resumen = (
    df_filtrado
    .groupby("ingrediente", as_index=False)
    .agg(
        medida=("medida", "first"),
        cantidad_usada=("cantidad", "sum"),
        costo_total=("costo", "sum")
    )
)

# 8. Cálculo de métricas y unidad
if not resumen.empty:
    total_cant = resumen["cantidad_usada"].sum()
    total_cost = resumen["costo_total"].sum()
    unidad = resumen["medida"].iloc[0] if len(seleccionados) == 1 else ""
else:
    total_cant, total_cost, unidad = 0, 0, ""

# 9. Mostrar título y métricas
st.title("Dashboard de Uso y Costo por Ingrediente")
st.divider()
col1, col2 = st.columns(2)
col1.metric("Total Cantidad", f"{total_cant:,.2f} {unidad}")
col2.metric("Total Costo",    f"${total_cost:,.2f}")

# 10. Tabla de detalle autoajustable
resumen_display = resumen.copy()
resumen_display["cantidad_usada"] = resumen_display["cantidad_usada"].map("{:,.2f}".format)
resumen_display["costo_total"]    = resumen_display["costo_total"].map("${:,.2f}".format)

st.subheader(
    f"Detalle {'Ingrediente' if len(seleccionados)==1 else 'Ingredientes'}: {', '.join(seleccionados)}"
)
st.dataframe(resumen_display)
