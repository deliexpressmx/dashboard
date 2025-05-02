import streamlit as st
import pandas as pd
import re
from supabase import create_client



# ======================================================
# Conexión a Supabase
# ======================================================
url = "https://ipwhnkvepshnbrpymwmn.supabase.co"
key = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwd2hua3ZlcHNobmJycHltd21uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyMjA0MzksImV4cCI6MjA1OTc5NjQzOX0."
    "R7QApURC5kdpjjXDKasQdtDQBIL_C6xnuSdqcDuZpBM"
)

supabase = create_client(url, key)

st.set_page_config(page_title="Carga de Datos a Supabase", layout="centered")
st.write("Conexión a Supabase establecida.")

# ------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------

def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))


def clean_brand(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", str(name))

# ------------------------------------------------------
# Helper inserción
# ------------------------------------------------------

def insert_records(table: str, records: list):
    if not records:
        st.warning(f"No hay registros para insertar en {table}.")
        return
    resp = supabase.table(table).insert(records).execute()
    if getattr(resp, "error", None) is None:
        st.success(f"✅ {len(records)} registros cargados en {table}.")
    else:
        st.error(f"❌ Error al insertar en {table}: {resp.error}")

# ======================================================
# Página principal
# ======================================================

st.title("🔄 Carga de Datos a Supabase SQL")

# ------------------------------------------------------
# 1) Tráfico & Conversión
# ------------------------------------------------------

st.subheader("1. Tráfico & Conversión (.xlsx)")
file_tc = st.file_uploader("Selecciona el archivo de Tráfico & Conversión", type=["xlsx"], key="tc")
if st.button("Subir Tráfico & Conversión"):
    if file_tc:
        df_tc = normalize_cols(pd.read_excel(file_tc))
        df_tc["marca"] = df_tc["marca"].apply(clean_brand)
        for col in ["fecha_inicio", "fecha_fin"]:
            if col in df_tc.columns:
                df_tc[col] = pd.to_datetime(df_tc[col], errors="coerce").dt.strftime("%Y-%m-%d")
        insert_records("traffic_conversion", df_tc.where(pd.notnull(df_tc), None).to_dict("records"))
    else:
        st.warning("Sube un archivo .xlsx primero.")

st.markdown("---")

# ------------------------------------------------------
# 2) Bitácora
# ------------------------------------------------------

st.subheader("2. Bitácora (.xlsx)")
file_bit = st.file_uploader("Selecciona el archivo de Bitácora", type=["xlsx"], key="bit")
if st.button("Subir Bitácora"):
    if file_bit:
        # Lee Excel en lugar de CSV
        df_bit = normalize_cols(pd.read_excel(file_bit))
        # Elimina columnas “unnamed”
        df_bit = df_bit.loc[:, ~df_bit.columns.str.startswith("unnamed")]
        # Limpia la marca
        df_bit["marca"] = df_bit["marca"].apply(clean_brand)
        # Formatea fecha si existe
        if "fecha" in df_bit.columns:
            df_bit["fecha"] = pd.to_datetime(df_bit["fecha"], errors="coerce").dt.strftime("%Y-%m-%d")
        # Inserta registros en la BD
        insert_records("bitacora", df_bit.where(pd.notnull(df_bit), None).to_dict("records"))
        st.success("Bitácora subida correctamente.")
    else:
        st.warning("Sube un archivo .xlsx primero.")

st.markdown("---")

# ------------------------------------------------------
# 3) Dashboard Metrics
# ------------------------------------------------------

st.subheader("3. Dashboard Metrics (.xlsx)")
file_dm = st.file_uploader("Selecciona el archivo de Dashboard Metrics", type=["xlsx"], key="dm")
if st.button("Subir Dashboard Metrics"):
    if file_dm:
        df_dm = normalize_cols(pd.read_excel(file_dm))
        df_dm = df_dm.rename(columns={"marcas": "marca"}) if "marcas" in df_dm.columns else df_dm
        df_dm["valor"] = pd.to_numeric(df_dm["valor"], errors="coerce")
        df_dm = df_dm[["marca", "plataforma", "semana", "tipo", "valor"]]
        df_dm = df_dm.dropna(subset=["valor"])
        insert_records("dashboard_metrics", df_dm.where(pd.notnull(df_dm), None).to_dict("records"))
    else:
        st.warning("Sube un archivo .xlsx primero.")

st.markdown("---")

# ------------------------------------------------------
# 4) User Retention
# ------------------------------------------------------

st.subheader("4. User Retention (.xlsx)")
file_ur = st.file_uploader("Selecciona el archivo de Retención de Usuarios", type=["xlsx"], key="ur")
if st.button("Subir Retención Usuarios"):
    if file_ur:
        df_ur = normalize_cols(pd.read_excel(file_ur))
        required = ["marca", "plataforma", "semana", "pedidos", "nuevos"]
        missing = [c for c in required if c not in df_ur.columns]
        if missing:
            st.error("Faltan columnas necesarias: " + ", ".join(missing))
            st.stop()
        df_ur["marca"] = df_ur["marca"].apply(clean_brand)
        df_ur["plataforma"] = df_ur["plataforma"].str.strip().str.lower()
        df_ur["semana"] = df_ur["semana"].astype(str).str.extract(r"(\d+)")[0].astype(int)
        for c in ["pedidos", "nuevos"]:
            df_ur[c] = pd.to_numeric(df_ur[c], errors="coerce").astype(int)
        df_ur["frecuentes"] = df_ur["pedidos"] - df_ur["nuevos"]
        df_ur["retencion"] = df_ur.apply(
            lambda r: (r["frecuentes"] / r["pedidos"] * 100) if r["pedidos"] else None,
            axis=1,
        )
        df_ur = df_ur.dropna()
        insert_records("user_retention", df_ur.to_dict("records"))
    else:
        st.warning("Sube un archivo .xlsx primero.")

st.markdown("---")

# ------------------------------------------------------
# 5) Quejas Órdenes
# ------------------------------------------------------

st.subheader("5. Quejas Órdenes (.csv)")
file_qo = st.file_uploader("Selecciona el archivo de Quejas de Órdenes", type=["csv"], key="qo")
if st.button("Subir Quejas Órdenes"):
    if file_qo:
        df_qo = normalize_cols(pd.read_csv(file_qo))
        if "fecha" in df_qo.columns:
            df_qo["fecha"] = pd.to_datetime(df_qo["fecha"], errors="coerce").dt.strftime("%Y-%m-%d")
        if "hora" in df_qo.columns:
            df_qo["hora"] = df_qo["hora"].astype(str)
        insert_records("quejas_ordenes", df_qo.where(pd.notnull(df_qo), None).to_dict("records"))
    else:
        st.warning("Sube un archivo .csv primero.")

st.markdown("---")

st.success("🎉 Carga de datos finalizada. Revisa Supabase para confirmar los registros.")


# ------------------------------------------------------
# 6) Inventario (.xlsx)
# ------------------------------------------------------
st.subheader("6. Inventario (.xlsx)")
file_inv = st.file_uploader("Selecciona el archivo de Inventario", type=["xlsx"], key="inv")

if st.button("Subir Inventario"):
    if not file_inv:
        st.warning("🗒️ Primero sube el archivo de Inventario (.xlsx).")
        st.stop()

    # 1) Leer y normalizar columnas
    df_inv = normalize_cols(pd.read_excel(file_inv))

    # 2) Validar columnas obligatorias
    required = ["fecha_inicio", "fecha_final", "ingrediente", "cantidad", "medida", "costo"]
    faltantes = [c for c in required if c not in df_inv.columns]
    if faltantes:
        st.error(f"❌ Faltan columnas en Inventario: {', '.join(faltantes)}")
        st.stop()

    # 3) Parseo estricto de fechas (YYYY-MM-DD)
    df_inv["fecha_inicio"] = pd.to_datetime(
        df_inv["fecha_inicio"], format="%Y-%m-%d", errors="coerce"
    )
    df_inv["fecha_final"]   = pd.to_datetime(
        df_inv["fecha_final"],  format="%Y-%m-%d", errors="coerce"
    )

    # 4) Detectar y abortar si hay fechas inválidas
    mask_invalid = df_inv["fecha_inicio"].isna() | df_inv["fecha_final"].isna()
    if mask_invalid.any():
        filas = df_inv[mask_invalid].index.tolist()
        st.error(f"❌ Filas con fecha inválida (deben ser YYYY-MM-DD): {filas}")
        st.stop()

    # 5) Eliminar filas que tengan NaN en alguna columna obligatoria
    df_inv = df_inv.dropna(subset=required)

    # 6) Convertir fechas a string en el mismo formato
    df_inv["fecha_inicio"] = df_inv["fecha_inicio"].dt.strftime("%Y-%m-%d")
    df_inv["fecha_final"]  = df_inv["fecha_final"].dt.strftime("%Y-%m-%d")

    # 7) Reemplazar NaN en el resto de las columnas por None
    df_inv = df_inv.where(pd.notnull(df_inv), None)

    # 8) Serializar y limpiar cualquier NaN residual
    records = df_inv.to_dict("records")
    import numpy as np
    clean_records = []
    for rec in records:
        clean = {
            k: (None if (isinstance(v, float) and np.isnan(v)) else v)
            for k, v in rec.items()
        }
        clean_records.append(clean)

    # 9) Insertar en la tabla "inventario"
    insert_records("inventario", clean_records)

    st.markdown("---")
# ------------------------------------------------------
# 7) Ventas x Producto (.xlsx)
# ------------------------------------------------------
st.subheader("7. Ventas x Producto (.xlsx)")
file_vp = st.file_uploader("Selecciona el archivo de Ventas x Producto", type=["xlsx"], key="vp")

if st.button("Subir Ventas x Producto"):
    if not file_vp:
        st.warning("🗒️ Primero sube el archivo de Ventas x Producto (.xlsx).")
        st.stop()

    # 1) Leer y normalizar
    df_vp = normalize_cols(pd.read_excel(file_vp))

    # 2) Validar que exista cada columna
    required = [
        "fecha_inicio", "fecha_final",
        "id", "producto",
        "cantidad", "valor_venta",
        "descuentos", "costo"
    ]
    miss = [c for c in required if c not in df_vp.columns]
    if miss:
        st.error(f"❌ Faltan columnas: {', '.join(miss)}")
        st.stop()

    # 3) Parsear fechas en YYYY-MM-DD
    for col in ("fecha_inicio", "fecha_final"):
        df_vp[col] = pd.to_datetime(
            df_vp[col], format="%Y-%m-%d", errors="coerce"
        )
    invalid = df_vp[ df_vp["fecha_inicio"].isna() | df_vp["fecha_final"].isna() ]
    if not invalid.empty:
        st.error(f"❌ Filas con fecha inválida (YYYY-MM-DD): {invalid.index.tolist()}")
        st.stop()

    # 4) Asegurar tipos numéricos
    df_vp["cantidad"]     = pd.to_numeric(df_vp["cantidad"],     errors="coerce").astype('Int64')
    df_vp["valor_venta"]  = pd.to_numeric(df_vp["valor_venta"],  errors="coerce")
    df_vp["descuentos"]   = pd.to_numeric(df_vp["descuentos"],   errors="coerce")
    df_vp["costo"]        = pd.to_numeric(df_vp["costo"],        errors="coerce")

    # 5) Eliminar filas con NaN en campos obligatorios
    df_vp = df_vp.dropna(subset=required)

    # 6) Formatear fechas a texto
    df_vp["fecha_inicio"] = df_vp["fecha_inicio"].dt.strftime("%Y-%m-%d")
    df_vp["fecha_final"]  = df_vp["fecha_final"].dt.strftime("%Y-%m-%d")

    # 7) Reemplazar NaN residuales y serializar
    df_vp = df_vp.where(pd.notnull(df_vp), None)
    records = df_vp.to_dict("records")

    # 8) Limpiar cualquier NaN flotante
    import numpy as np
    clean = []
    for r in records:
        clean.append({k: (None if isinstance(v, float) and np.isnan(v) else v)
                      for k,v in r.items()})

    # 9) Insertar en Supabase
    insert_records("ventas_x_producto", clean)
