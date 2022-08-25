#   Importamos las librerias
import os
from pathlib import Path

MAIN_DIR = Path(f"{os.path.dirname(os.path.realpath(__file__))}").parent
CORE_DIR = Path(f"{os.path.dirname(os.path.realpath(__file__))}")
LOG_DIR = Path(f"{MAIN_DIR}/logs")

