# 🧭 TourData — Occasional Trips Prediction in Chile 🇨🇱

TourData is a predictive analytics application created to support tourism planning in Chile. It forecasts the number of **occasional trips** between regions using official data and machine learning models.

---

## 📊 What does this app do?

- Predicts occasional trips between Chilean regions, by month and season.
- Visualizes results on an interactive map (Folium).
- Displays time series charts color-coded by high or low tourism season.
- Allows custom queries by origin, destination, month, and economic variables.
- Uses public data from **SERNATUR** and the **Central Bank of Chile**.

---

## 🧠 Prediction Model

The model used is an **XGBoost Regressor**, trained to predict the monthly number of occasional trips between Chilean regions. The prediction is based on:

- Origin region  
- Destination region  
- Month of the year  
- Tourism season (high or low)  
- Regional GDP (origin and destination)

The model was trained using data from 2019 to 2024, and the main evaluation metric was **R² (coefficient of determination)**.

---

## 🧪 Data Sources

- **SERNATUR** – Occasional trip database at the regional level.  
- **Central Bank of Chile** – Annual regional Gross Domestic Product (GDP).  
- Data was cleaned, structured, and transformed for predictive use.

---

## ⚙️ Setup

### ✅ Prerequisites

- Python 3.10 or higher  
- pip

### 🧩 Installation


git clone https://github.com/youruser/Tour_Data_Pro.git
cd Tour_Data_Pro
pip install -r requirements.txt


### 🧩 Running the App

streamlit run src/TourDataApp.py

### 🎯 Features

- Region and month-based prediction
- Interactive map visualization
- Seasonally color-coded time series
- Exportable results table
- Dynamic filtering by month and season

### 👨‍💻 Contributors
Felipe Browne and Luis Camacho
Developed during the Data Science and Machine Learning program at 4Geeks Academy Chile.