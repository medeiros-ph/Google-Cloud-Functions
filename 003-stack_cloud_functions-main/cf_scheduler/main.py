from google.cloud import storage
from datetime import datetime

# credentials to get access google cloud storage
storage_client = storage.Client()

# write your bucket name
bucket_name = 'stack-scheduler-bucket'
BUCKET = storage_client.get_bucket(bucket_name)


def create_text_file(text, filename):
    # create a blob
    blob = BUCKET.blob(filename)
    # upload the blob
    blob.upload_from_string(text)
    result = filename + ' upload complete'
    return {'response': result}


def hello_world(request):
    # your object
    time = datetime.now()
    # set the filename
    filename = 'text_file' + str(time) + '.txt'
    text = "Esse arquivo foi criado às " + str(time)
    # run the function and pass the string
    return (create_text_file(text, filename))


