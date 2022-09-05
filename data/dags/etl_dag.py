# Importamos las dependencias necesarias
from fileinput import filename
from connect_dag import start_connct
from confi import db_user, BUKECT_NAME
from constans import LOG_DIR, SCHEMA_NAME
from elt_functions import get_table, transform_dts, load_data_to_s3

import logging
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

#   Definimos el formato de fecha
now = datetime.now()
year = now.year
month = now.month
day = now.day
date = f"{year}-{month:02d}-{day:02d}"  # Establecemos los place holders
today_date = date.format(year=year, month=month,
                         day=day)

#   Establecemos las configuración del log
logging.basicConfig(filename=f"{LOG_DIR}/{today_date}-{db_user}.log",  # Se generará un archivo .log el cual
                    level="DEBUG")  # tendrá en el nombre el siguiente formato
#   %Y-%m-%d - nombre_logger(usuario de
#   la base de datos)


# Definimos las propiedades del DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


#       Creamos las funciones que intervendrán en el proceso
# Declaramos las inputs de la función
schema_name = SCHEMA_NAME  # get_data(schema_name, engine)
engine = start_connct()

# Definimos los agumentos del python callable
get_data_kwargs = {
    "schema_name": schema_name,
    "engine": engine
}


def get_data(schema_name: list,
             engine: object) -> dict:
    """Esta función ejecuta consultas sql sobre la base de datos y las extrae como .csv y las 
    almacena en el directorio: ./airflow_docker/data/files...
    Args:
        schema_name (list): lista con los nombres de las tablas de la base de datos 
        (deben corresponder a los nombre de los scripts .sql)
        engine (object): conexión con la base de datos

    Returns:
        dict: diccionario con las rutas a los .csv recuperados de la base de datos
    """
    extract_path_dict = {}
    for table_name in schema_name:
        extract_path_dict[f"{table_name}"] = get_table(table_name,
                                                       engine)
        # Llamamos al log oportunamente
        logging.info(f"getting the data from {table_name}")
    return extract_path_dict


# Declaramos las inputs de la función
extract_path_dict = get_data(schema_name=SCHEMA_NAME,
                             engine=engine)  # transform_data(schema_name, path_dict)


# Definimos los agumentos del python callable
transform_data_kwargs = {
    "schema_name": schema_name,
    "path_dict": extract_path_dict
}


def transform_data(schema_name: list,
                   path_dict: dict) -> dict:
    """Esta función aplica las transformaciones requeridas a los datos recuperados de la base de 
    datos, los almacena en uno nuevo con extensión .txt y retorna la ruta a dichos archivos.

    Args:
        schema_name (list): lista con los nombres de las tablas de la base de datos 
        (deben corresponder a los nombre de los scripts .sql).
        path_dict (dict): diccionario con las rutas a los .csv recuperados de la base de datos.

    Returns:
        dict: diccionario con las rutas a los .txt transformados.
    """
    transformed_path_dict = {}
    for table_name in schema_name:
        path = path_dict[f"{table_name}"]
        transformed_path_dict[f"{table_name}"] = transform_dts(table_name,
                                                               path)

        # Llamamos al log oportunamente
        logging.info(f"transforming the data from {table_name}")
    return transformed_path_dict


# Declaramos las inputs de la función
transformed_path_dict = transform_data(
    schema_name=SCHEMA_NAME, path_dict=extract_path_dict)
bucket_name = BUKECT_NAME

# Definimos los agumentos del python callable
load_data_kwargs = {
    "path_dict": transformed_path_dict,
    "bucket_name": bucket_name
}


def load_data(path_dict: dict,
              bucket_name: str) -> None:
    """Esta función establece la conexión con el AS3 bucket y realiza la carga de los .txt 
    transformados.

    Args:
        path_dict (dict): _description_
        bucket_name (str): _description_
    """
    for table_name in schema_name:
        filename = path_dict[f"{table_name}"]
        load_data_to_s3(filename=filename, table_name=table_name,
                        bucket_name=bucket_name)
    logging.info("loading the data")


#   Creamos un diccionario gloval de argumentos a partir de los diccionarios de
op_kwargs = {"get_data": get_data_kwargs,
             "transform_data": transform_data_kwargs,
             "load_data": load_data_kwargs
             }


# Definimos el DAG
with DAG(
        "elt_dag",
        default_args=default_args,
        description="DAG para el procesamiento y carga de datos a S3",
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 8, 23),
        tags=["alkemy_acceleration_sptr01"],
) as dag:
    get_data_task = PythonOperator(task_id="get_data",
                                   python_callable=get_data,
                                   op_kwargs=op_kwargs["get_data"],
                                   retries=5,
                                   retry_delay=timedelta(minutes=5),
                                   dag=dag)
    transform_data_task = PythonOperator(task_id="transform_data",
                                         python_callable=transform_data,
                                         op_kwargs=op_kwargs["transform_data"],
                                         dag=dag)
    load_data_task = PythonOperator(task_id="load_data",
                                    python_callable=load_data,
                                    op_kwargs=op_kwargs["load_data"],
                                    dag=dag)

    get_data_task >> transform_data_task >> load_data_task
