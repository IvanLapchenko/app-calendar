import time
from flask import Flask
from flask_mail import Mail
from credintials import *
from flask_mail import Message
import requests

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.ukr.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_DEFAULT_SENDER'] = email
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def send_email(recipient, header, body):
    msg = Message('Subject', recipients=[recipient])
    msg.body = header
    msg.html = body
    mail.send(msg)
    print('Email sent')


def check_for_events_every_hour():
    while True:

        events = requests.get("http://127.0.0.1:5000/check_for_near_events").json()
        if len(events) > 0:
            for event in events:
                recipient = requests.get("http://127.0.0.1:5000/get_user_email_by_id").json()
                header = event.header
                body = f"{event.time} \n {event.describe}"

                send_email(recipient, header, body)
        time.sleep(30)


check_for_events_every_hour()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)