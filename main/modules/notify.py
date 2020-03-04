import requests
import smtplib
import ssl
from email.mime.text import MIMEText

from mam.settings import MAIL_TO


class ChatWork:
    API_URL = 'https://api.chatwork.com/v2/rooms/175265855/files'
    APIKey = 'e8bc4a6360420f894d47c83446cdc675'

    def __init__(self):
        self.headers = {'X-ChatWorkToken': ChatWork.APIKey}

    def send(self, *messages, image):
        messages = [str(i) for i in messages]
        files = {
            'file': ('mam_error.png', open(image, 'rb'), 'image/png'),
            'message': messages[0]
        }
        for message in messages[1:]:
            files['message'] += '\n' + message
        requests.post(
            ChatWork.API_URL,
            headers=self.headers,
            files=files
        )


def mail(subject, body):
    account = "kubok.dev@gmail.com"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
    server.login(account, 'tjbqzygxxuuylrez')

    for to in MAIL_TO:
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["To"] = to
        msg["From"] = account
        server.send_message(msg)
