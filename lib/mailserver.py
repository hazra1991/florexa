# mail server

import smtplib
from email.message import EmailMessage
import os 
from threading import Thread

EMAIL_SERVER_ADDRESS = "florexa.dev@gmail.com"
EMAIL_SERVER_PASS = "fvuicvyaipmjmfxe"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def send_mail(subject="",body="",sendto=None,priority="1"):
    msg =  EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SERVER_ADDRESS
    msg["To"] = sendto
    msg["X-Priority"] = priority
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT,timeout=10) as smtpclient:
        smtpclient.login(EMAIL_SERVER_ADDRESS,EMAIL_SERVER_PASS)
        smtpclient.send_message(msg)

        # exception :- smtplib.SMTPRecipientsRefused:

