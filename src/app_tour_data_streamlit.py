# src/app/app_tour_data_streamlit.py

from pathlib import Path
from pickle import load
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import folium
from streamlit_folium import st_folium

# ==== RUTAS DINÁMICAS ====
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data" / "processed"
INTERIM_DIR = BASE_DIR / "data" / "interim"

# ==== CARGA MODELO Y DICCIONARIOS ====
model = load(open(MODEL_DIR / "xgboost_regressor_lr_0_15_mx_dp_8_n_esti_310_42.pkl", "rb"))
with open(DATA_DIR / "region_origen_dict.json", encoding="utf-8") as f:
    region_origen_dict = json.load(f)
with open(DATA_DIR / "region_destino_dict.json", encoding="utf-8") as f:
    region_destino_dict = json.load(f)
with open(DATA_DIR / "region_temp_dict.json", encoding="utf-8") as f:
    region_temp_dict = json.load(f)
with open(DATA_DIR / "region_pib_dict.json", encoding="utf-8") as f:
    region_pib_dict = json.load(f)
with open(DATA_DIR / "cut_comuna_dict.json", encoding="utf-8") as f:
    cut_comuna_dict = json.load(f)
with open(DATA_DIR / "cut_provincia_dict.json", encoding="utf-8") as f:
    cut_provincia_dict = json.load(f)
with open(DATA_DIR / "cut_region_dict.json", encoding="utf-8") as f:
    cut_region_dict = json.load(f)

logo = INTERIM_DIR / "TourData-remove-background.com.png"
mapa_path = INTERIM_DIR / "mapa-01-2.png"

# ==== FUNCIONES UTILITARIAS ====
def obtener_info(region, region_dict, tipo="provincias", provincia=None): 
    if region not in region_dict:
        return []
    if tipo == "provincias" and provincia is None:
        return list(region_dict[region].keys())
    elif tipo == "comunas" and provincia is None:
        return [c for p in region_dict[region].values() for c in p]
    elif tipo == "comunas" and provincia:
        return region_dict[region].get(provincia, [])
    return []

def calcular_meses(n):
    fecha_base = datetime(2024, 7, 1)
    return [(fecha_base + relativedelta(months=i)).month, (fecha_base + relativedelta(months=i)).year] for i in range(n)

def consultar_temporada(region, mes, region_mes_dict):
    return region_mes_dict.get(f"({region}, {mes})", 0)

def buscar_cut(diccionario, clave):
    return diccionario.get(clave, 0)

def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

# ==== INTERFAZ STREAMLIT ====
st.set_page_config(page_title="Predicción de Viajes", layout="wide")

col1, col2 = st.columns([1, 4])
with col1:
    st.image(str(logo), width=110)
with col2:
    st.title("Predicción Viajes Ocasionales en Chile")

# ==== MAPA ====
col1, col2 = st.columns(2)
with col1:
    st_map = st_folium(folium.Map(location=[-36.5, -70.2], zoom_start=5), width=450, height=470)
with col2:
    st.image(str(mapa_path), width=450)

# ==== SIDEBAR ORIGEN ====
st.sidebar.title("Origen del Viaje")
region_origen = st.sidebar.selectbox("Región Origen", list(region_origen_dict))
provincia_origen = st.sidebar.selectbox("Provincia Origen", obtener_info(region_origen, region_origen_dict, "provincias"))
comuna_origen = st.sidebar.selectbox("Comuna Origen", obtener_info(region_origen, region_origen_dict, "comunas", provincia_origen))
pib_variacion_origen = st.sidebar.slider("Variación mensual PIB Origen (%)", -1.5, 1.5, 0.0, 0.1)
pib_origen = region_pib_dict.get(region_origen, 0) * (1 + pib_variacion_origen / 100)

# ==== SIDEBAR DESTINO ====
st.sidebar.title("Destino del Viaje")
region_destino = st.sidebar.selectbox("Región Destino", list(region_destino_dict))
provincia_destino = st.sidebar.selectbox("Provincia Destino", obtener_info(region_destino, region_destino_dict, "provincias"))
comuna_destino = st.sidebar.selectbox("Comuna Destino", obtener_info(region_destino, region_destino_dict, "comunas", provincia_destino))
pib_variacion_destino = st.sidebar.slider("Variación mensual PIB Destino (%)", -1.5, 1.5, 0.0, 0.1)
pib_destino = region_pib_dict.get(region_destino, 0) * (1 + pib_variacion_destino / 100)

# ==== SIDEBAR MESES ====
n_meses = st.sidebar.slider("Meses a predecir", 1, 12, 1)
meses = calcular_meses(n_meses)

# ==== PREDICCIÓN ====
df_pred, df_model = pd.DataFrame(), pd.DataFrame()
for mes, anio in meses:
    temporada = consultar_temporada(region_origen, mes, region_temp_dict)
    df_pred = pd.concat([df_pred, pd.DataFrame([{
        "Región Origen": region_origen,
        "Provincia Origen": provincia_origen,
        "Comuna Origen": comuna_origen,
        "Región Destino": region_destino,
        "Provincia Destino": provincia_destino,
        "Comuna Destino": comuna_destino,
        "Año": anio,
        "Mes": mes,
        "Temporada": temporada,
        "PIB Región Origen": pib_origen,
        "PIB Región Destino": pib_destino,
        "Covid": 0
    }])], ignore_index=True)

    df_model = pd.concat([df_model, pd.DataFrame([{
        "CUT Region Origen": buscar_cut(cut_region_dict, region_origen),
        "CUT Provincia Origen": buscar_cut(cut_provincia_dict, provincia_origen),
        "CUT Comuna Origen": buscar_cut(cut_comuna_dict, comuna_origen),
        "CUT Region Destino": buscar_cut(cut_region_dict, region_destino),
        "CUT Provincia Destino": buscar_cut(cut_provincia_dict, provincia_destino),
        "CUT Comuna Destino": buscar_cut(cut_comuna_dict, comuna_destino),
        "Anio": anio,
        "CUT Mes": mes,
        "CUT Temporada": temporada,
        "PIB Region Origen": pib_origen,
        "PIB Region Destino": pib_destino,
        "covid_periodo_num": 0
    }])], ignore_index=True)

st.subheader("Consulta")
st.dataframe(df_pred)

# ==== PREDICCIÓN MODELO ====
if st.sidebar.button("Predecir"):
    pred = model.predict(df_model)
    df_model["Predicción Viajes Ocasionales"] = [max(0, round(p)) for p in pred]

    st.subheader("Predicciones")
    df_model["Fecha"] = pd.to_datetime(df_model["Anio"].astype(str) + "-" + df_model["CUT Mes"].astype(str) + "-01")
    df_show = df_model[["Fecha", "Predicción Viajes Ocasionales"]].sort_values("Fecha")
    st.line_chart(df_show.set_index("Fecha"))

    csv = convert_df(df_model)
    st.download_button("Descargar CSV", csv, "predicciones.csv", "text/csv")
