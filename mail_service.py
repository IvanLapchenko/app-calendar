from . import app
from flask_mail import Mail
from .credintials import *
from flask_mail import Message
import time
from .communicate_with_db import check_for_near_events, get_user_email_by_id


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
        events = check_for_near_events()
        if len(events) > 0:
            for event in events:
                recipient = get_user_email_by_id(event.user)
                header = event.header
                body = f"{event.time} \n {event.describe}"

                send_email(recipient, header, body)
        time.sleep(3600)

