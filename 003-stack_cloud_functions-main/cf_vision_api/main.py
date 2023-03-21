from google.cloud import vision, storage
import os
import tempfile

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

os.environ['no_proxy'] = '*'

def uploadToGCS(faces, file_name, bucket_output):
    _, temp_local_filename = tempfile.mkstemp()

    f = open(temp_local_filename, "w")
    f.write(str(faces))
    f.close()

    face_bucket = storage_client.bucket(bucket_output)
    uploadfilename = file_name + "-output.txt"
    new_blob = face_bucket.blob(uploadfilename)
    new_blob.upload_from_filename(temp_local_filename)
    print(f"Face Response uploaded to: gs://{face_bucket}/{uploadfilename}")

    os.remove(temp_local_filename)
def detect_face(data, context):

    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]

    print(f"Processing file: {file_name}.")
    print(f"Bucket : {bucket_name}.")

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source = vision.Image(source=vision.ImageSource(gcs_image_uri=blob_uri))

    faces = vision_client.face_detection(image=blob_source, max_results=4).face_annotations
    print(faces)

    if len(faces) > 0:
        if str(faces[0].joy_likelihood) in ('Likelihood.VERY_LIKELY', 'Likelihood.LIKELY'):
            uploadToGCS(faces, file_name, 'stack-cf-vision-api-output-joy-7564812')
        elif str(faces[0].sorrow_likelihood) in ('Likelihood.VERY_LIKELY', 'Likelihood.LIKELY'):
            uploadToGCS(faces, file_name, 'stack-cf-vision-api-output-sorrow-76538523')
        else:
            uploadToGCS(faces, file_name, 'stack-cf-vision-api-output-unkown-6458125123')

    return 0
