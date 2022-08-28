#   Importamos las librerias
import os
from pathlib import Path

MAIN_DIR = Path(f"{os.path.dirname(os.path.realpath(__file__))}").parent.parent
DATA_DIR = Path(f"{os.path.dirname(os.path.realpath(__file__))}").parent
SQL_SCRIPT_DIR = LOG_DIR = Path(f"{DATA_DIR}/psql_script")
DAGS_DIR = Path(f"{os.path.dirname(os.path.realpath(__file__))}")
LOG_DIR = Path(f"{DATA_DIR}/logs")
DATASET_DIR = Path(f"{DATA_DIR}/files")

#   Declaramos los nombres de las tablas
TABLE01 = "jfk_uni"
TABLE02 = "lat_social_uni"

#   Creamos una lista con los esquemas a disponibilizar
SCHEMA_NAME = [
    TABLE01,
    TABLE02
]