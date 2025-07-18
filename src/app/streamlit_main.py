import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

from src.utils.helpers import calcular_meses, consultar_temporada, buscar_cut, convert_df
from src.data.load_data import cargar_modelo, cargar_diccionario
from src.models.predict import predecir

def main():
    st.set_page_config(page_title="TourData Pro", layout="wide")

    # Carga de modelo y diccionarios
    model = cargar_modelo("models/xgboost_regressor_lr_0_15_mx_dp_8_n_esti_310_42.pkl")
    region_origen_dict = cargar_diccionario("data/processed/region_origen_dict.json")
    region_destino_dict = cargar_diccionario("data/processed/region_destino_dict.json")
    region_temp_dict = cargar_diccionario("data/processed/region_temp_dict.json")
    region_pib_dict = cargar_diccionario("data/processed/region_pib_dict.json")
    cut_comuna_dict = cargar_diccionario("data/processed/cut_comuna_dict.json")
    cut_provincia_dict = cargar_diccionario("data/processed/cut_provincia_dict.json")
    cut_region_dict = cargar_diccionario("data/processed/cut_region_dict.json")
    logo = "data/interim/TourData-remove-background.com.png"

    # Header
    st.image(logo, width=200)
    st.title("Predicción de Viajes Ocasionales en Chile")

    # Mapa de Chile
    col1, col2 = st.columns(2)
    mapa = folium.Map(location=[-36.5, -70.2], zoom_start=5)
    with col1:
        st_folium(mapa, width=450, height=470)
    with col2:
        st.image("data/interim/mapa-01-2.png", width=450)

    # Entrada de usuario
    st.sidebar.header("Origen")
    region_origen = st.sidebar.selectbox("Región Origen", region_origen_dict.keys())
    provincia_origen = st.sidebar.selectbox("Provincia Origen", region_origen_dict[region_origen].keys())
    comuna_origen = st.sidebar.selectbox("Comuna Origen", region_origen_dict[region_origen][provincia_origen])
    var_pib_origen = st.sidebar.slider("Var. PIB Origen (%)", -1.5, 1.5, 0.0, step=0.1)

    st.sidebar.header("Destino")
    region_destino = st.sidebar.selectbox("Región Destino", region_destino_dict.keys())
    provincia_destino = st.sidebar.selectbox("Provincia Destino", region_destino_dict[region_destino].keys())
    comuna_destino = st.sidebar.selectbox("Comuna Destino", region_destino_dict[region_destino][provincia_destino])
    var_pib_destino = st.sidebar.slider("Var. PIB Destino (%)", -1.5, 1.5, 0.0, step=0.1)

    st.sidebar.header("Predicción")
    meses_a_predecir = st.sidebar.slider("Cantidad de meses", 1, 12, 1)
    meses_anios = calcular_meses(meses_a_predecir)

    pib_o = region_pib_dict[region_origen] * (1 + var_pib_origen / 100)
    pib_d = region_pib_dict[region_destino] * (1 + var_pib_destino / 100)

    pred_df = pd.DataFrame()
    pred_trans_df = pd.DataFrame()

    for mes, anio in meses_anios:
        temporada = consultar_temporada(region_origen, mes, region_temp_dict)
        fila = {
            'Comuna Origen': comuna_origen,
            'Provincia Origen': provincia_origen,
            'Región Origen': region_origen,
            'Comuna Destino': comuna_destino,
            'Provincia Destino': provincia_destino,
            'Región Destino': region_destino,
            'Año': anio,
            'Mes': mes,
            'Temporada': temporada,
            'PIB Región Origen': pib_o,
            'PIB Región Destino': pib_d,
            'Covid': 0
        }
        fila_trans = {
            'CUT Comuna Origen': buscar_cut(cut_comuna_dict, comuna_origen),
            'CUT Provincia Origen': buscar_cut(cut_provincia_dict, provincia_origen),
            'CUT Region Origen': buscar_cut(cut_region_dict, region_origen),
            'CUT Comuna Destino': buscar_cut(cut_comuna_dict, comuna_destino),
            'CUT Provincia Destino': buscar_cut(cut_provincia_dict, provincia_destino),
            'CUT Region Destino': buscar_cut(cut_region_dict, region_destino),
            'Anio': anio,
            'CUT Mes': mes,
            'CUT Temporada': temporada,
            'PIB Region Origen': pib_o,
            'PIB Region Destino': pib_d,
            'covid_periodo_num': 0
        }
        pred_df = pd.concat([pred_df, pd.DataFrame([fila])], ignore_index=True)
        pred_trans_df = pd.concat([pred_trans_df, pd.DataFrame([fila_trans])], ignore_index=True)

    st.subheader("Datos para predicción")
    st.dataframe(pred_df)

    if st.sidebar.button("Predecir"):
        resultado = pred_trans_df.copy()
        resultado["Predicción Viajes Ocasionales"] = predecir(model, pred_trans_df)

        st.subheader("Resultados")
        st.dataframe(resultado[["Anio", "CUT Mes", "Predicción Viajes Ocasionales"]].rename(columns={"Anio": "Año", "CUT Mes": "Mes"}))

        if meses_a_predecir > 1:
            resultado["Fecha"] = pd.to_datetime(resultado["Anio"].astype(str) + "-" + resultado["CUT Mes"].astype(str) + "-01")
            resultado = resultado.sort_values("Fecha")

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(resultado["Fecha"], resultado["Predicción Viajes Ocasionales"], marker="o", linewidth=2)
            ax.set_xticks(resultado["Fecha"])
            ax.set_xticklabels(resultado["Fecha"].dt.strftime('%Y-%m'), rotation=45)
            ax.set_title("Viajes Ocasionales Predichos")
            ax.set_ylabel("Cantidad")
            st.pyplot(fig)

        # Descargar CSV
        csv = convert_df(resultado)
        st.download_button("Descargar CSV", data=csv, file_name="predicciones.csv", mime="text/csv")
