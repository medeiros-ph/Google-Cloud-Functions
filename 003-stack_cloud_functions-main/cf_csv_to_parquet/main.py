import pandas as pd
from parametros.env_configs import EnvConfigs
from google.cloud import bigquery
from google.cloud import storage
import numpy as np
from datetime import datetime
import logging
import google.cloud.logging
import os

logging_client = google.cloud.logging.Client()
logging_client.get_default_handler()
logging_client.setup_logging()

os.environ['no_proxy'] = '*'

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print(f"Blob {blob_name} deleted.")

def main(event, context):
    uri = ""

    try:

        file = event

        uri = 'gs://' + file['bucket'] + "/" + file['name']

        logging.info('Processando o arquivo "{}".'.format(uri))

        env_configs = EnvConfigs()

        blob_path = file['name'].split("/")

        project = env_configs.get_gcp_project()
        bucket_destination = env_configs.get_bucket_destination()
        bucket_source = env_configs.get_bucket_source()

        bucket = file['bucket']
        file_path = file['name']

        logging.info('Carregando o arquivo "{}" no dataframe.'.format(uri))
        df = pd.read_csv(uri)

        df["File_Source"] = file['name']

        logging.info('Carregando arquivo: "{}" no bucket historico.'.format(file['name']))

        path_destination = "gs://" + bucket_destination + "/" + str(
            datetime.now().date()) + "/" + file_path + '.parquet.gzip'

        logging.info('Convertendo e salvando o arquivo "{}" no formato parquet em "{}".'.format(uri, path_destination))

        df.to_parquet(path_destination, compression='gzip')

        logging.info('Deletando o arquivo "{}".'.format(uri))
        delete_blob(bucket, file_path)

    except Exception as e:
        logging.exception(e)
        return {"status": "error", "details": str(type(e).__name__)}, 400

    logging.info('status : success')
    return {"status": "success"}