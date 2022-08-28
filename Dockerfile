FROM apache/airflow:2.3.3
COPY requirements.txt /requirements.txt
RUN mkdir /opt/airflow/files /opt/airflow/psql_script
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt