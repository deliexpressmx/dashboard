import re
import math
import calendar
from datetime import date, timedelta, datetime

import streamlit as st
import pandas as pd
import numpy as np
from supabase import create_client

# ══════════════════ CONFIGURACIÓN ══════════════════
st.set_page_config(page_title="Dashboard DeliExpress", layout="wide")

SUPABASE_URL = "https://ipwhnkvepshnbrpymwmn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwd2hua3ZlcHNobmJycHltd21uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMjA0MzksImV4cCI6MjA1OTc5NjQzOX0.R7QApURC5kdpjjXDKasQdtDQBIL_C6xnuSdqcDuZpBM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ═════════════ HELPER: CARGA POR LOTES ═════════════
def load_all(table: str, cols: str = "*", batch_size: int = 1000) -> pd.DataFrame:
    rows, start = [], 0
    while True:
        resp = supabase.table(table).select(cols).range(start, start + batch_size - 1).execute()
        data = resp.data or []
        if not data:
            break
        rows.extend(data)
        start += batch_size
    return pd.DataFrame(rows)

# ═════════════ CARGA DE DATOS ═════════════
df = load_all("dashboard_metrics", "marca,plataforma,semana,tipo,valor").rename(columns={"marca":"marcas"})
ret = load_all("user_retention", "marca,plataforma,semana,pedidos,nuevos,frecuentes,retencion")
if df.empty:
    st.error("No hay datos en dashboard_metrics")
    st.stop()

# ═════════════ LIMPIEZA DE DATOS ═════════════
df["semana"] = pd.to_numeric(df["semana"], errors="coerce")
df = df.dropna(subset=["semana"])
df["semana"] = df["semana"].astype(int)
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

ret["semana"] = pd.to_numeric(ret["semana"], errors="coerce")
ret = ret.dropna(subset=["semana"])
ret["semana"] = ret["semana"].astype(int)
for c in ["pedidos","nuevos","frecuentes","retencion"]:
    if c in ret.columns:
        ret[c] = pd.to_numeric(ret[c], errors="coerce")
if ret.get("retencion", pd.Series()).isna().all():
    ret["retencion"] = ret.apply(lambda r: (r["frecuentes"]/r["pedidos"]*100) if r["pedidos"] else pd.NA, axis=1)

# Normalizar cadenas
df["marca_norm"] = df["marcas"].apply(lambda x: re.sub(r"[^A-Za-z0-9]","",str(x)).lower())
df["plataforma_norm"] = df["plataforma"].str.strip().str.lower()
ret["marca_norm"] = ret["marca"].apply(lambda x: re.sub(r"[^A-Za-z0-9]","",str(x)).lower())
ret["plataforma_norm"] = ret["plataforma"].str.strip().str.lower()

# ═════════════ INTERFAZ ═════════════
st.title("Dashboard DeliExpress")

marcas      = ["Todos"] + sorted(df["marcas"].unique())
plataformas = ["Todos"] + sorted(df["plataforma"].unique())

marca_sel = st.sidebar.selectbox("Marca", marcas)
plat_sel  = st.sidebar.selectbox("Plataforma", plataformas)

# ═════════════ FILTRADO ═════════════
df_f = df.copy()
ret_f = ret.copy()
if marca_sel!="Todos":
    df_f = df_f[df_f["marca_norm"]==re.sub(r"[^A-Za-z0-9]","",marca_sel).lower()]
    ret_f = ret_f[ret_f["marca_norm"]==re.sub(r"[^A-Za-z0-9]","",marca_sel).lower()]
if plat_sel!="Todos":
    df_f = df_f[df_f["plataforma"]==plat_sel]
    ret_f = ret_f[ret_f["plataforma_norm"]==plat_sel.strip().lower()]

# ═════════════ NUEVO: RANGO DE FECHAS DOBLE ═════════════
st.sidebar.markdown("### Rango 1")
fecha_ini_1 = st.sidebar.date_input("Fecha Inicio", date.today() - timedelta(weeks=4), key="ini1")
fecha_fin_1 = st.sidebar.date_input("Fecha Fin", date.today() - timedelta(weeks=3), key="fin1")

st.sidebar.markdown("### Rango 2")
fecha_ini_2 = st.sidebar.date_input("Fecha Inicio2", date.today() - timedelta(weeks=2), key="ini2")
fecha_fin_2 = st.sidebar.date_input("Fecha Fin2", date.today() - timedelta(weeks=1), key="fin2")

# Convertir a semanas ISO
sem_ini_1 = fecha_ini_1.isocalendar().week
sem_fin_1 = fecha_fin_1.isocalendar().week
sem_ini_2 = fecha_ini_2.isocalendar().week
sem_fin_2 = fecha_fin_2.isocalendar().week

# Filtro para cada bloque de semanas
sum_mode = "Suma"
sem_range_2 = list(range(sem_ini_2, sem_fin_2 + 1))
if len(sem_range_2) >= 2:
    sum_mode = st.sidebar.radio("Modo de Rango 2", ["Suma", "Promedio Semanal"], key="modo_r2")
else:
    st.sidebar.warning("Para usar promedio semanal debes seleccionar mínimo dos semanas.")

# Aplicar filtro de fechas
df_r1      = df_f[df_f["semana"].between(sem_ini_1, sem_fin_1)]
df_r2_raw  = df_f[df_f["semana"].between(sem_ini_2, sem_fin_2)]
df_r2      = df_r2_raw.copy()
ret_r1     = ret_f[ret_f["semana"].between(sem_ini_1, sem_fin_1)]
ret_r2_raw = ret_f[ret_f["semana"].between(sem_ini_2, sem_fin_2)]

# ─── Promedio Semanal o Suma ───
if sum_mode == "Promedio Semanal" and len(sem_range_2) >= 2:
    # 1) Ventas, pauta y órdenes promediadas
    df_r2 = (
        df_r2_raw
        .groupby(["tipo", "marcas"])
        .agg({"valor": "sum"})
        .div(len(sem_range_2))
        .reset_index()
    )
    # 2) Retención: calcular métricas por semana...
    weekly = (
        ret_r2_raw
        .groupby("semana")
        .agg({"pedidos": "sum", "nuevos": "sum", "frecuentes": "sum"})
    )
    weekly["retencion"] = weekly["frecuentes"] / weekly["pedidos"] * 100
    # 3) …y luego promediar esas métricas semanales
    weekly_means = weekly.mean()
    # 4) Construir ret_r2 con el promedio semanal
    ret_r2 = weekly_means.to_frame().T
else:
    # Modo Suma
    df_r2  = df_r2_raw.copy()
    ret_r2 = ret_r2_raw.copy()

# Definir df2_range según el modo
df2_range = df_r2_raw if sum_mode == "Suma" else df_r2

# ═════════════ AGREGACIÓN DE MÉTRICAS ═════════════
pivot_r1 = df_r1.pivot_table(index="tipo", values="valor", aggfunc="sum").fillna(0)
pivot_r2 = df_r2.pivot_table(index="tipo", values="valor", aggfunc="sum").fillna(0)

# Derivadas y métricas
for pivot, fi, ff, df_range in [
    (pivot_r1, fecha_ini_1, fecha_fin_1, df_r1),
    (pivot_r2, fecha_ini_2, fecha_fin_2, df2_range)
]:
    if not pivot.empty:
        ventas  = df_range.loc[df_range["tipo"] == "ventas",   "valor"].sum()
        ordenes = df_range.loc[df_range["tipo"] == "ordenes", "valor"].sum()
        if "plataforma" in df_range.columns:
            mask = (df_range["tipo"] == "pauta") & df_range["plataforma"].isin(["Uber","Rappi"])
        else:
            mask = (df_range["tipo"] == "pauta")
        pauta_val = df_range.loc[mask, "valor"].sum()

        pivot.loc["ventas"]          = ventas
        pivot.loc["ordenes"]         = ordenes
        pivot.loc["pauta"]           = pauta_val
        pivot.loc["ticket_promedio"] = ventas / ordenes if ordenes else 0
        pivot.loc["ordenes_por_dia"] = ordenes / ((ff - fi).days + 1)
        pivot.loc["roas"]            = ventas / pauta_val if pauta_val else 0

types = ["ventas","pauta","ordenes","roas","ordenes_por_dia","ticket_promedio"]

st.divider()
# ═════════════ COMPARATIVA ═════════════
st.subheader("📊 Rango 1")
cols = st.columns(len(types))
for i, t in enumerate(types):
    v1 = pivot_r1.at[t,"valor"] if t in pivot_r1.index else 0
    v2 = pivot_r2.at[t,"valor"] if t in pivot_r2.index else 0
    delta = (v1-v2)/v2*100 if v2 else 0
    if t in ["ordenes","ordenes_por_dia"]:
        v1s = f"{int(v1):,}"; v2s = f"{int(v2):,}"
    elif t=="roas":
        v1s = f"{v1:.2f}"; v2s = f"{v2:.2f}"
    else:
        v1s = f"${v1:,.2f}"; v2s = f"${v2:,.2f}"
    cols[i].metric(t.replace("_"," ").title(), v1s, f"{delta:+.2f}%")

st.subheader("📘 Rango 2")
cols2 = st.columns(len(types))
for i, t in enumerate(types):
    v2 = pivot_r2.at[t,"valor"] if t in pivot_r2.index else 0
    if t in ["ordenes","ordenes_por_dia"]:
        v2s = f"{int(v2):,}"
    elif t == "roas":
        v2s = f"{v2:.2f}"
    else:
        v2s = f"${v2:,.2f}"
    cols2[i].metric(t.replace("_"," ").title(), v2s)

st.divider()
# ═════════════ RETENCIÓN ═════════════
def agg_ret(df_):
    if df_.empty:
        return pd.Series({"pedidos":pd.NA,"nuevos":pd.NA,"frecuentes":pd.NA,"retencion":pd.NA})
    s = df_[["pedidos","nuevos","frecuentes"]].sum(min_count=1)
    s["retencion"] = df_["retencion"].mean()
    return s

base_ret = agg_ret(ret_r1)
comp_ret = agg_ret(ret_r2)
delta_ret = (base_ret - comp_ret)/comp_ret.replace(0,pd.NA)*100
keys_ret = ["pedidos","nuevos","frecuentes","retencion"]
labels = ["Pedidos","Nuevos","Frecuentes","Retención %"]

st.subheader("👥 Retención Rango 1")
cols_rb = st.columns(4)
for i,k in enumerate(keys_ret):
    v = base_ret[k]; dv = delta_ret[k]
    vs = "-" if pd.isna(v) else (f"{v:.2f}%" if k=="retencion" else f"{int(v):,}")
    ds = "-" if pd.isna(dv) else f"{dv:+.2f}%"
    cols_rb[i].metric(labels[i],vs,ds)

st.subheader("📘 Retención Rango 2")
cols_rc = st.columns(4)
for i,k in enumerate(keys_ret):
    v = comp_ret[k]
    vs = "-" if pd.isna(v) else (f"{v:.2f}%" if k=="retencion" else f"{int(v):,}")
    cols_rc[i].metric(labels[i], vs)

st.divider()
# ═════════════ RUN RATE (proyección mensual) ═════════════
sales_month = df_f[(df_f["tipo"]=="ventas") & (df_f["semana"].between(sem_ini_1, sem_fin_1))]
if not sales_month.empty:
    dias_observados = ((fecha_fin_1 - fecha_ini_1).days + 1)
    run_rate_ventas = sales_month["valor"].sum() / dias_observados * 30
    pauta_month = df_f[(df_f["tipo"]=="pauta") & (df_f["semana"].between(sem_ini_1, sem_fin_1))]
    run_rate_pauta = pauta_month["valor"].sum() / dias_observados * 30 if dias_observados else 0
    st.subheader("🏃‍♂️ Run Rate Ventas y Pauta")
    cols_rr = st.columns(2)
    cols_rr[0].metric("Run Rate Ventas", f"${run_rate_ventas:,.2f}")
    cols_rr[1].metric("Run Rate Pauta", f"${run_rate_pauta:,.2f}")

st.divider()
# ═════════════ CRECIMIENTO POR MARCA ═════════════
st.subheader("📈 Crecimiento por Marca")
base_sales = df_r1[df_r1["tipo"]=="ventas"].groupby("marcas")["valor"].sum()
if sum_mode == "Promedio Semanal" and len(sem_range_2) >= 2:
    comp_sales = df_r2[df_r2["tipo"]=="ventas"]
    if "marcas" in comp_sales.columns:
        comp_sales = comp_sales.groupby("marcas")["valor"].sum()
    else:
        comp_sales = df_r2_raw[df_r2_raw["tipo"]=="ventas"].groupby("marcas")["valor"].sum().div(len(sem_range_2))
else:
    comp_sales = df_r2_raw[df_r2_raw["tipo"]=="ventas"].groupby("marcas")["valor"].sum()
growth = pd.concat([base_sales, comp_sales], axis=1, keys=["Ventas Base","Ventas Comparativo"]).fillna(0)
growth["Crecimiento %"] = ((growth["Ventas Base"] - growth["Ventas Comparativo"]) / growth["Ventas Comparativo"].replace(0,np.nan) * 100)
growth = growth.reset_index().rename(columns={"marcas":"Marca"})
def color_pct(val):
    if pd.isna(val): return ""
    return "color: green" if val>0 else "color: red" if val<0 else "color: orange"
styled = (growth.style
          .format({"Ventas Base":"${:,.2f}","Ventas Comparativo":"${:,.2f}","Crecimiento %":"{:+.2f}%"})
          .applymap(color_pct, subset=["Crecimiento %"]))
st.dataframe(styled)
