import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import logging
from datetime import datetime
import bcchapi  # Asegúrate de tener instalada esta librería

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def obtener_pib_regional(guardar_en="data/raw/pib_regional.csv") -> pd.DataFrame:
    """
    Descarga los datos de PIB regional desde la API del Banco Central de Chile (bcchapi)
    y guarda un CSV con formato largo: Fecha | Región | PIB
    """

    # Cargar variables de entorno
    load_dotenv()
    client_id = os.getenv("USUARIO_BCC")
    client_secret = os.getenv("SECRET_BCC")

    if not client_id or not client_secret:
        logging.error("Faltan credenciales en el archivo .env (USUARIO_BCC, SECRET_BCC).")
        raise ValueError("Credenciales no encontradas.")

    # Conexión con la API
    siete = bcchapi.Siete(client_id, client_secret)

    # Diccionario serie ↔ región
    dic_serie_region = {
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.15.0.T": "Arica y Parinacota",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.01.0.T": "Tarapacá",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.02.0.T": "Antofagasta",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.03.0.T": "Atacama",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.04.0.T": "Coquimbo",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.05.0.T": "Valparaíso",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.13.0.T": "Metropolitana de Santiago",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.06.0.T": "Libertador Gral. Bernardo O'Higgins",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.07.0.T": "Maule",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.16.0.T": "Ñuble",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.08.0.T": "Biobío",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.09.0.T": "La Araucanía",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.14.0.T": "Los Ríos",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.10.0.T": "Los Lagos",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.11.0.T": "Aysén del General Carlos Ibáñez del Campo",
        "F035.PIB.FLU.R.CLP.2018.Z.Z.Z.12.0.T": "Magallanes y de la Antártica Chilena"
    }

    try:
        df = siete.cuadro(
            series=list(dic_serie_region.keys()),
            nombres=list(dic_serie_region.values())
        )
    except Exception as e:
        logging.error(f"Error al consultar API del Banco Central: {e}")
        raise

    # Procesamiento final
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Fecha"}, inplace=True)

    # Guardar CSV
    path = Path(guardar_en)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep=";", index=False)
    logging.info(f"Archivo PIB guardado en: {path}")

    # Guardar metadata de actualización
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data/raw/ultima_actualizacion_pib.txt", "w", encoding="utf-8") as f:
        f.write(f"Última actualización: {fecha_actual}\n")
        f.write("Fuente: API Banco Central\n")

    logging.info("PIB regional actualizado correctamente.")
    return df


if __name__ == "__main__":
    try:
        df = obtener_pib_regional()
        logging.info(f"Total de filas descargadas: {len(df)}")
    except Exception as e:
        logging.error(f"Ocurrió un error durante la ejecución: {e}")
