import pandas as pd
from parametros.env_configs import EnvConfigs
from google.cloud import bigquery
from google.cloud import storage
import datetime
from datetime import datetime
import logging
import google.cloud.logging
import os
import pandas_gbq

logging_client = google.cloud.logging.Client()
logging_client.get_default_handler()
logging_client.setup_logging()

os.environ['no_proxy'] = '*'

def main(event, context):
    uri = ""

    try:

        file = event

        uri = 'gs://' + file['bucket'] + "/" + file['name']

        logging.info('Processando o arquivo "{}".'.format(uri))

        env_configs = EnvConfigs()

        project = env_configs.get_gcp_project()
        dataset = env_configs.get_destination_dataset()
        table = env_configs.get_destination_table()

        table_id = project + "." + dataset + "." + table

        logging.info('Interface : {}'.format(table))

        logging.info('Carregando o arquivo "{}" no dataframe.'.format(uri))
        df = pd.read_parquet(uri)

        df["Ingestion_Date"] = pd.Timestamp.today().strftime('%Y-%m-%d')
        df['Ingestion_Date'] = pd.to_datetime(df['Ingestion_Date'], format='%Y-%m-%d')

        logging.info('Carregando o dataframe na tabela "{}".'.format(table_id))

        pandas_gbq.to_gbq(df, table_id, project_id=project, if_exists='append')


    except Exception as e:
        logging.exception(e)
        return {"status": "error", "details": str(type(e).__name__)}, 400

    logging.info('status : success')
    return {"status": "success"}