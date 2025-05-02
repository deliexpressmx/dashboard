import streamlit as st
import pandas as pd
from supabase import create_client

# 0. Configuración de la página en modo wide
st.set_page_config(page_title="Ventas x Producto", layout="wide")

# 1. Conexión a Supabase
def get_supabase_client():
    url = "https://ipwhnkvepshnbrpymwmn.supabase.co"
    key = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwd2hua3ZlcHNobmJycHltd21uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMjA0MzksImV4cCI6MjA1OTc5NjQzOX0."
        "R7QApURC5kdpjjXDKasQdtDQBIL_C6xnuSdqcDuZpBM"
    )
    return create_client(url, key)

supabase = get_supabase_client()

# 2. Carga de datos desde la tabla 'ventas_x_producto' por batches
@st.cache_data
def load_data():
    batch_size = 1000
    offset = 0
    all_data = []
    while True:
        resp = supabase.table("ventas_x_producto").select("*").range(offset, offset + batch_size - 1).execute()
        if getattr(resp, 'error', None):
            st.error(f"Error al cargar datos: {resp.error.message}")
            return pd.DataFrame()
        chunk = resp.data or []
        all_data.extend(chunk)
        if len(chunk) < batch_size:
            break
        offset += batch_size
    df = pd.DataFrame(all_data)
    # Parsear fechas
    df['fecha_inicio'] = pd.to_datetime(df.get('fecha_inicio'), errors='coerce')
    df['fecha_final']  = pd.to_datetime(df.get('fecha_final'),  errors='coerce')
    return df

# Obtener datos
df = load_data()

# 3. Barra lateral: filtros
st.sidebar.header("Filtros")
# Botón para recargar datos
if st.sidebar.button("🔄 Actualizar datos"):
    load_data.clear()
    st.experimental_rerun()

# Selector de fechas
date_min = df['fecha_inicio'].min().date() if not df.empty else pd.Timestamp.today().date()
date_max = df['fecha_final'].max().date()  if not df.empty else pd.Timestamp.today().date()
start_date = st.sidebar.date_input("Fecha inicio:", value=date_min)
end_date   = st.sidebar.date_input("Fecha final:",  value=date_max)
start_ts = pd.Timestamp(start_date)
end_ts   = pd.Timestamp(end_date)

# Selector múltiple de productos
productos = df['producto'].dropna().unique().tolist()
seleccion = st.sidebar.multiselect("Producto(s):", options=productos, key="sel_prod")

# 4. Filtrar datos
mask = (
    (df['fecha_inicio'] >= start_ts) &
    (df['fecha_final']  <= end_ts)
)
if seleccion:
    mask &= df['producto'].isin(seleccion)
df_f = df[mask]

# 5. Métricas clave
total_unidades    = int(df_f['cantidad'].sum())
total_ingresos    = df_f['valor_venta'].sum()
total_descuentos  = df_f['descuentos'].sum()
total             = total_ingresos + total_descuentos

# 6. Mostrar título y separador
st.title("Ventas x Producto")
st.divider()

# 7. Mostrar métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Unidades vendidas", f"{total_unidades:,.0f}")
col2.metric("Ingresos",         f"${total_ingresos:,.2f}")
col3.metric("Descuentos",       f"${total_descuentos:,.2f}")
col4.metric("Total",            f"${total:,.2f}")

# 8. Tabla de detalle
df_table = df_f.copy()
# Formatear columnas monetarias
df_table['valor_venta']   = df_table['valor_venta'].map("${:,.2f}".format)
df_table['descuentos']    = df_table['descuentos'].map("${:,.2f}".format)
df_table['costo']         = df_table['costo'].map("${:,.2f}".format)
# Selección de columnas a mostrar
df_table = df_table.loc[:, [
    'fecha_inicio', 'fecha_final', 'id', 'producto',
    'cantidad', 'valor_venta', 'descuentos', 'costo'
]]

st.subheader("Detalle de ventas")
st.dataframe(df_table)