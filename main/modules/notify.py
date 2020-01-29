import requests
import smtplib
import ssl
from email.mime.text import MIMEText

from mam_spider.settings import MAIL_TO


class ChatWork:
    API_URL = 'https://api.chatwork.com/v2/rooms/158341952/messages?force=1'
    APIKey = 'e8bc4a6360420f894d47c83446cdc675'

    def __init__(self):
        self.headers = {'X-ChatWorkToken': ChatWork.APIKey}

    def send(self, *messages, image=None):
        messages = [str(i) for i in messages]
        payload = {
            'body': messages[0]
        }
        for message in messages[1:]:
            payload['body'] += '\n    ' + message
        files = {}
        if image is not None:
            files = {'imageFile': open(image, 'rb')}
        requests.post(
            ChatWork.API_URL,
            headers=self.headers,
            params=payload,
            files=files
        )


def mail(subject, body):
    account = "kubok.dev@gmail.com"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
    server.login(account, 'tjbqzygxxuuylrez')

    for to in MAIL_TO:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["To"] = to
        msg["From"] = account
        server.send_message(msg)
