# data_pipeline.py

from scraper.sernatur_scraper import descargar_viajes_ocasionales
from scraper.bcch_api import obtener_pib_regional
import logging

# Configuración de logging general
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("🔁 Iniciando pipeline de actualización de datos...")

    try:
        logging.info("📥 Descargando datos de SERNATUR...")
        df_sernatur = descargar_viajes_ocasionales()
        logging.info(f"✅ Viajes descargados: {len(df_sernatur)} filas.")
    except Exception as e:
        logging.error(f"❌ Error al descargar datos de SERNATUR: {e}")

    try:
        logging.info("📥 Descargando datos del PIB (Banco Central)...")
        df_pib = obtener_pib_regional()
        logging.info(f"✅ PIB descargado: {len(df_pib)} filas.")
    except Exception as e:
        logging.error(f"❌ Error al descargar datos del Banco Central: {e}")

    logging.info("✅ Pipeline finalizado.")

if __name__ == "__main__":
    main()
