import re
import calendar
from datetime import date, timedelta

import streamlit as st
import pandas as pd
from supabase import create_client

# ------------------------------------------------------
# Conexión a Supabase
# ------------------------------------------------------
URL  = "https://ipwhnkvepshnbrpymwmn.supabase.co"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwd2hua3ZlcHNobmJycHltd21uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMjA0MzksImV4cCI6MjA1OTc5NjQzOX0.R7QApURC5kdpjjXDKasQdtDQBIL_C6xnuSdqcDuZpBM"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Dashboard Tráfico / Conversión", layout="wide")

# ──────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────
def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(" ", "_", regex=False)
    )
    return df

def clean_brand(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", str(name)).lower()

@st.cache_data(ttl=300)
def load_data():
    res1 = supabase.table("traffic_conversion").select("*").execute()
    df_tc = pd.DataFrame(res1.data or [])
    df_tc = normalize_cols(df_tc)
    df_tc["marca"] = df_tc["marca"].apply(clean_brand)

    res2 = supabase.table("bitacora").select("*").execute()
    df_bit = pd.DataFrame(res2.data or [])
    df_bit = normalize_cols(df_bit)
    df_bit["marca"] = df_bit["marca"].apply(clean_brand)

    return df_tc, df_bit

trafico_df, bitacora_df = load_data()
if trafico_df.empty:
    st.error("⚠️ No hay datos en `traffic_conversion`")
    st.stop()

# ──────────────────────────────────────────────────────
# Sidebar: filtros y comparadores con rangos de fechas
# ──────────────────────────────────────────────────────
st.sidebar.markdown("### Filtros")
marcas = ["Todos"] + sorted(trafico_df["marca"].unique())
marca_sel = st.sidebar.selectbox("Marca", marcas)

df_filtrado = (
    trafico_df
    if marca_sel == "Todos"
    else trafico_df[trafico_df["marca"] == marca_sel]
)

st.sidebar.markdown("### Rango Base")
hoy = date.today()
# por defecto, rango base: últimas 1 semana
base_ini = st.sidebar.date_input("Inicio Rango Base", hoy - timedelta(weeks=1), key="b_ini")
base_fin = st.sidebar.date_input("Fin Rango Base",    hoy - timedelta(days=1), key="b_fin")

st.sidebar.markdown("### Rango Comparativo")
comp_ini = st.sidebar.date_input("Inicio Rango Comp.", hoy - timedelta(weeks=2), key="c_ini")
comp_fin = st.sidebar.date_input("Fin Rango Comp.",    hoy - timedelta(weeks=1), key="c_fin")

# seleccionar modo de agregación para rango comparativo
sum_mode = st.sidebar.radio("Modo Rango Comp.", ["Suma", "Promedio Semanal"], key="modo_cmp")

# convertir fechas a semanas ISO
def to_iso_weeks(d: date):
    w = d.isocalendar().week
    y = d.isocalendar().year
    return (y, w)

y1, wb1 = to_iso_weeks(base_ini)
_, wb2     = to_iso_weeks(base_fin)
y2, wc1    = to_iso_weeks(comp_ini)
_, wc2     = to_iso_weeks(comp_fin)

# si cruza año, podemos ignorar y agrupar solo por número de semana
sem_base = list(range(wb1, wb2 + 1))
sem_comp = list(range(wc1, wc2 + 1))

# ──────────────────────────────────────────────────────
# Cálculo de métricas
# ──────────────────────────────────────────────────────
def metrics_for(df: pd.DataFrame, *, weekly_mean: bool=False) -> pd.Series:
    if df.empty:
        return pd.Series({
            "trafico": 0,
            "vieron_menu": 0,
            "agregaron_articulos": 0,
            "pedidos_realizados": 0,
            "conversion": 0
        })
    # sumas
    t   = df["trafico"].sum()
    v   = df["vieron_menu"].sum()
    a   = df["agregaron_articulos"].sum()
    p   = df["pedidos_realizados"].sum()
    if weekly_mean:
        n = df["semana"].nunique() or 1
        t /= n; v /= n; a /= n; p /= n
    conv = p / v if v else 0
    return pd.Series({
        "trafico": t,
        "vieron_menu": v,
        "agregaron_articulos": a,
        "pedidos_realizados": p,
        "conversion": conv
    })

# filtrar por semanas
df_base = df_filtrado[df_filtrado["semana"].isin(sem_base)]
df_comp = df_filtrado[df_filtrado["semana"].isin(sem_comp)]

# métricas base (siempre suma de rango base)
met_base = metrics_for(df_base, weekly_mean=False)
# métricas comparativas
met_comp = metrics_for(df_comp, weekly_mean=(sum_mode=="Promedio Semanal"))

# ──────────────────────────────────────────────────────
# Mostrar métricas
# ──────────────────────────────────────────────────────
st.title("📊 Trafico y Conversion")
st.divider()
delta = lambda x, y: (x - y) / y if y else None

labels = [
    ("Tráfico", "trafico"),
    ("Vieron menú", "vieron_menu"),
    ("Agregaron artículos", "agregaron_articulos"),
    ("Pedidos realizados", "pedidos_realizados"),
    ("Conversión", "conversion")
]

cols = st.columns(2)
for label, key in labels:
    base_val = met_base[key]
    cmp_val  = met_comp[key]
    d = delta(base_val, cmp_val)
    # formateo
    if key == "conversion":
        b_str = f"{base_val:.2%}"
        c_str = f"{cmp_val:.2%}"
        d_str = f"{d:+.2%}" if d is not None else "-"
    else:
        b_str = f"{int(base_val):,}"
        if sum_mode=="Promedio Semanal" and key!="conversion":
            c_str = f"{cmp_val:,.0f}"
        else:
            c_str = f"{int(cmp_val):,}"
        d_str = f"{d:+.2%}" if d is not None else "-"

    col1, col2 = st.columns(2)
    col1.metric(f"{label} (Base)", b_str, d_str)
    col2.metric(f"{label} (Comp.)", c_str)

# ──────────────────────────────────────────────────────
# Bitácora
# ──────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📜 Bitácora de Cambios")
df_bit = (
    bitacora_df
    if marca_sel == "Todos"
    else bitacora_df[bitacora_df["marca"] == marca_sel]
)
st.dataframe(df_bit, use_container_width=True)
