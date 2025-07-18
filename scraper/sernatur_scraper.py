import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import logging

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def descargar_viajes_ocasionales(guardar_en="data/raw/viajes_ocasionales.csv") -> pd.DataFrame:
    """
    Descarga el CSV de viajes ocasionales desde la página de SERNATUR y lo guarda localmente.
    Devuelve un DataFrame limpio.
    """
    url = "https://www.sernatur.cl/dataturismo/big-data-turismo-interno/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    logging.info(f"Conectando a {url}...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error al conectar con la página: {e}")
        raise

    soup = BeautifulSoup(response.content, "html.parser")
    csv_links = [a["href"] for a in soup.find_all("a", href=True)
                 if "csv" in a["href"].lower() or "download" in a["href"].lower()]

    if not csv_links:
        logging.error("No se encontró ningún enlace CSV en la página.")
        raise ValueError("No se encontró ningún enlace CSV en la página.")

    csv_url = csv_links[0]
    logging.info(f"Enlace CSV encontrado: {csv_url}")

    try:
        file_content = requests.get(csv_url, headers=headers).content
    except Exception as e:
        logging.error(f"No se pudo descargar el archivo: {e}")
        raise

    path = Path(guardar_en)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        f.write(file_content)
        logging.info(f"Archivo CSV guardado en: {path}")

    if path.stat().st_size == 0:
        logging.error("El archivo descargado está vacío.")
        raise ValueError("El archivo descargado está vacío.")

    try:
        df = pd.read_csv(path, sep=";", decimal=",")
    except Exception as e:
        logging.error(f"Error al leer el archivo CSV: {e}")
        raise

    if df.empty:
        logging.warning("El DataFrame está vacío después de leer el archivo.")
        raise ValueError("El archivo CSV no contiene datos útiles.")

    # Limpieza: solo columnas numéricas
    for col in df.columns[1:]:
        try:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .astype(float)
                .round()
                .astype("Int64")
            )
        except ValueError:
            logging.warning(f"Columna ignorada (no numérica): {col}")

    logging.info("DataFrame limpio y listo.")
    return df

if __name__ == "__main__":
    try:
        df = descargar_viajes_ocasionales()
        logging.info(f"CSV descargado correctamente. Total de filas: {len(df)}")
    except Exception as e:
        logging.error(f"Ocurrió un error durante la ejecución: {e}")

from datetime import datetime

# Guardar fecha de actualización
fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("data/raw/ultima_actualizacion.txt", "w", encoding="utf-8") as f:
    f.write(f"Última actualización: {fecha_actual}\n")
    f.write("Fuente: https://www.sernatur.cl/dataturismo/big-data-turismo-interno/")