import base64
import os
from twilio.rest import Client
from google.cloud import secretmanager


def hello_pubsub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    client = secretmanager.SecretManagerServiceClient()

    TWILIO_ACCOUNT_SID_secret = "TWILIO_ACCOUNT_SID"
    TWILIO_AUTH_TOKEN_secret = "TWILIO_AUTH_TOKEN"
    project_id = "cloud-functions01"

    TWILIO_ACCOUNT_SID_request = {"name": f"projects/{project_id}/secrets/{TWILIO_ACCOUNT_SID_secret}/versions/latest"}

    TWILIO_AUTH_TOKEN_request = {"name": f"projects/{project_id}/secrets/{TWILIO_AUTH_TOKEN_secret}/versions/latest"}

    TWILIO_ACCOUNT_SID_response = client.access_secret_version(TWILIO_ACCOUNT_SID_request)

    TWILIO_AUTH_TOKEN_response = client.access_secret_version(TWILIO_AUTH_TOKEN_request)

    TWILIO_ACCOUNT_SID_secret_payload = TWILIO_ACCOUNT_SID_response.payload.data.decode("UTF-8")

    TWILIO_AUTH_TOKEN_secret_payload = TWILIO_AUTH_TOKEN_response.payload.data.decode("UTF-8")

    account_sid = TWILIO_ACCOUNT_SID_secret_payload
    auth_token = TWILIO_AUTH_TOKEN_secret_payload

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Mensagem: " + pubsub_message,
        from_='+16812461902',
        to='+5521982930075'
    )

    print(message.sid)
