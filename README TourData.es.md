# 🧭 TourData — Predicción de Viajes Ocasionales en Chile 🇨🇱

TourData es una aplicación de análisis predictivo creada para apoyar la planificación turística en Chile. Predice la cantidad de **viajes ocasionales** entre regiones utilizando datos oficiales y modelos de aprendizaje automático.

---

## 📊 ¿Qué hace esta app?

- Predice viajes ocasionales entre regiones chilenas, por mes y temporada.
- Visualiza los resultados en un mapa interactivo (Folium).
- Muestra series de tiempo codificadas por temporada alta o baja.
- Permite consultas personalizadas según origen, destino, mes y variables económicas.
- Utiliza datos públicos de **SERNATUR** y el **Banco Central de Chile**.

---

## 🧠 Modelo de Predicción

El modelo utilizado es un **XGBoost Regressor**, entrenado para predecir la cantidad de viajes ocasionales mensuales entre regiones de Chile. La predicción se realiza en función de:

- Región de origen  
- Región de destino  
- Mes del año  
- Temporada turística (alta o baja)  
- PIB regional de origen y destino

El entrenamiento se realizó con datos desde 2019 a 2024, y la métrica principal utilizada fue **R² (coeficiente de determinación)**.

---

## 🧪 Origen de los Datos

- **SERNATUR** – Base de datos de viajes ocasionales a nivel regional.  
- **Banco Central de Chile** – Producto Interno Bruto (PIB) regional anual.  
- Datos estructurados, limpiados y transformados para uso predictivo.

---

## ⚙️ Configuración

### ✅ Prerrequisitos

- Python 3.10 o superior  
- pip

### 🧩 Instalación


git clone https://github.com/tuusuario/Tour_Data_Pro.git
cd Tour_Data_Pro
pip install -r requirements.txt


### 🧩 Ejecución App

streamlit run src/TourDataApp.py

### 🎯 Funcionalidades

- Predicción por región y mes
- Visualización en mapa interactivo
- Serie de tiempo coloreada por temporada
- Tabla de resultados exportable
- Ajuste dinámico por mes y temporada

### Contribuyentes

Felipe Browne  y Luis Camacho duranta el curso de Data Science y Maching Learling de 4Geeks Chile.

