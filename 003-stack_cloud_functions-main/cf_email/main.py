import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import abort

def send_email(request):

    if request.method != "POST":
        abort(405)

    bearer_token = request.headers.get('Authorization').split()[1]
    secret_key = os.environ.get('ACCESS_KEY')

    if bearer_token != secret_key:
        abort(401)

    request_json = request.get_json(silent=True)

    parameters = ('sender', 'receiver', 'subject', 'message')

    sender, receiver, subject, message = '', '', '', ''

    if request_json and all(k in request_json for k in parameters):
        sender = request_json['sender']
        receiver = request_json['receiver']
        subject = request_json['subject']
        message = request_json['message']
    else:
        abort(400)

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('SEND_GRID_API_KEY'))
        sg.send(message)
        return 'OK', 200
    except Exception as e:
        return e, 400

