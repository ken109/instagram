import requests
# import smtplib
# import ssl
import os
# from email.mime.text import MIMEText

# from instagram.settings import MAIL_TO


class ChatWork:
    APIKey = 'e8bc4a6360420f894d47c83446cdc675'
    headers = {'X-ChatWorkToken': APIKey}

    @staticmethod
    def send_screen(driver):
        driver.save_screenshot('screen.png')
        ChatWork.send_file(image='screen.png')
        os.remove('screen.png')

    @staticmethod
    def send_message(*messages):
        messages = [str(i) for i in messages]
        params = {'body': messages[0] if len(messages) > 0 else ''}
        if len(messages) > 1:
            for message in messages[1:]:
                params['body'] += '\n' + message
        requests.post(
            'https://api.chatwork.com/v2/rooms/175265855/messages',
            headers=ChatWork.headers,
            params=params
        )

    @staticmethod
    def send_file(image, *messages):
        messages = [str(i) for i in messages]
        files = {
            'file': (image, open(image, 'rb'), 'image/png'),
            'message': messages[0] if len(messages) > 0 else ''
        }
        if len(messages) > 1:
            for message in messages[1:]:
                files['message'] += '\n' + message
        requests.post(
            'https://api.chatwork.com/v2/rooms/175265855/files',
            headers=ChatWork.headers,
            files=files
        )


# def mail(subject, body):
#     account = "kubok.dev@gmail.com"
#
#     server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
#     server.login(account, 'tjbqzygxxuuylrez')
#
#     for to in MAIL_TO:
#         msg = MIMEText(body, "plain")
#         msg["Subject"] = subject
#         msg["To"] = to
#         msg["From"] = account
#         server.send_message(msg)
