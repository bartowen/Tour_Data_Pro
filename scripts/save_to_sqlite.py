from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

def guardar_en_sqlite(df: pd.DataFrame, tabla: str, db_path="db/tour_data.db", reemplazar=False):
    """
    Guarda un DataFrame en una tabla SQLite.
    - df: el DataFrame a guardar
    - tabla: nombre de la tabla en la base de datos
    - db_path: ubicación del archivo .db
    - reemplazar: si True, borra la tabla y escribe de nuevo
    """
    modo = "replace" if reemplazar else "append"
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql(tabla, con=engine, if_exists=modo, index=False)
    print(f"✅ Datos guardados en la tabla '{tabla}'.")

# Ejemplo local para pruebas
if __name__ == "__main__":
    df = pd.read_csv("data/raw/viajes_ocasionales.csv", sep=";")
    guardar_en_sqlite(df, tabla="viajes_ocasionales", reemplazar=True)
