from decouple import AutoConfig
from constans import CORE_DIR

config = AutoConfig(search_path = CORE_DIR)

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_pass = config("DB_PASS")
db_host = config("DB_HOST")
db_port = config("DB_PORT")