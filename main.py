import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask
from flask import request

app = Flask(__name__)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get("API_KEY")
GMAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

GMAIL_PORT = 465
GMAIL_SMTP_SERVER = "smtp.gmail.com"

AHA_USERNAME = os.environ.get("AHA_USERNAME")
AHA_PASSWORD = os.environ.get("AHA_PASSWORD")
AHA_PORT = 587
AHA_SMTP_SERVER = 'send.ahasend.com'


def send_plain_email_through(smtp_server, port, username, password, from_email, to_email, subject, body):
    try:
        message = f"""\
        Subject: ${subject}
    
        ${body}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.sendmail(from_email, to_email, message)
        return True
    except Exception as e:
        logger.error(e)
        return False


def send_fancy_email(smtp_server, port, username, password, from_email, to_email, subject, plain_body, fancy_body):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email

        part1 = MIMEText(plain_body, "plain")
        part2 = MIMEText(fancy_body, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.sendmail(
                from_email, to_email, message.as_string()
            )
        return True
    except Exception as e:
        logger.error(e)
        return False


@app.route('/')
def hello_world():
    return 'Server is Running'


@app.route('/sendMail')
def send_mail(method='POST'):
    if method != 'POST':
        return 'Not Allowed'
    else:
        logger.debug(request.json, request.method, request.headers, request.remote_addr, request.url)
        from_email = request.json.get('from')
        to_email = request.json.get('to')
        subject = request.json.get('subject')
        plain_body = request.json.get('plain_body')
        fancy_body = request.json.get('fancy_body')
        is_html = request.json.get('html')
        api_key = request.json.get('api_key')
        agent = request.json.get('agent')
        if api_key != API_KEY:
            return 'Invalid API Key', 403

        smtp_server = GMAIL_SMTP_SERVER
        port = GMAIL_PORT
        username = GMAIL_USERNAME
        password = GMAIL_PASSWORD

        if agent == 'ahasend':
            smtp_server = AHA_SMTP_SERVER
            port = AHA_PORT
            username = AHA_USERNAME
            password = AHA_PASSWORD

        if from_email is None or to_email is None or subject is None or (plain_body is None and fancy_body is None):
            return 'Missing Parameters', 400
        else:
            if is_html:
                res = send_fancy_email(smtp_server, port, username, password, from_email, to_email, subject, plain_body,
                                       fancy_body)
                if res:
                    return 'Success', 200
                else:
                    return 'Failed', 500
            else:
                res = send_plain_email_through(smtp_server, port, username, password, from_email, to_email, subject,
                                               plain_body)
                if res:
                    return 'Success', 200
                else:
                    return 'Failed', 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
