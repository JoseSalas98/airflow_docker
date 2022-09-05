from decouple import AutoConfig
from constans import DAGS_DIR

config = AutoConfig(search_path=DAGS_DIR)

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_pass = config("DB_PASS")
db_host = config("DB_HOST")
db_port = config("DB_PORT")
BUKECT_NAME = config("BUKECT_NAME")
