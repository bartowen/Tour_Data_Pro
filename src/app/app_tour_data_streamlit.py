
# Librerías
from pickle import load
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from pathlib import Path

# Base del proyecto
base_dir = Path(__file__).resolve().parent

# Modelo y Diccionarios
model = load(open(base_dir / 'models' / 'xgboost_regressor_lr_0_15_mx_dp_8_n_esti_310_42.pkl', 'rb'))
with open(base_dir / 'data' / 'processed' / 'region_origen_dict.json', 'r', encoding='utf-8') as f:
    region_origen_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'region_destino_dict.json', 'r', encoding='utf-8') as f:
    region_destino_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'region_temp_dict.json', 'r', encoding='utf-8') as f:
    region_temp_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'region_pib_dict.json', 'r', encoding='utf-8') as f:
    region_pib_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'cut_comuna_dict.json', 'r', encoding='utf-8') as f:
    cut_comuna_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'cut_provincia_dict.json', 'r', encoding='utf-8') as f:
    cut_provincia_dict = json.load(f)
with open(base_dir / 'data' / 'processed' / 'cut_region_dict.json', 'r', encoding='utf-8') as f:
    cut_region_dict = json.load(f)
logo = base_dir / 'data' / 'interim' / 'TourData-remove-background.com.png'

# El resto de la app permanece igual desde aquí en adelante
# (puedes pegar el resto de tu código original a partir de donde dice "# Funciones", sin cambiar)
