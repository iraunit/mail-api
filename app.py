import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask
from flask import request

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
GMAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

GMAIL_PORT = 587
GMAIL_SMTP_SERVER = "smtp.gmail.com"

AHA_USERNAME = os.environ.get("AHA_USERNAME")
AHA_PASSWORD = os.environ.get("AHA_PASSWORD")
AHA_PORT = 587
AHA_SMTP_SERVER = 'send.ahasend.com'


def send_plain_email(smtp_server, port, username, password, from_email, to_email, subject, body, sender_name):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"{sender_name} <{from_email}>"
        msg['To'] = to_email

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(e)
        return False


def send_fancy_email(smtp_server, port, username, password, from_email, to_email, subject, plain_body, fancy_body,
                     sender_name):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message['From'] = f"{sender_name} <{from_email}>"
        message["To"] = to_email

        part1 = MIMEText(plain_body, "plain")
        part2 = MIMEText(fancy_body, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
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


@app.route('/send', methods=['POST'])
def send_mail():
    from_email = request.json.get('from')
    to_email = request.json.get('to')
    subject = request.json.get('subject')
    plain_body = request.json.get('plain_body')
    fancy_body = request.json.get('fancy_body')
    is_html = request.json.get('is_html')
    api_key = request.json.get('api_key')
    agent = request.json.get('agent')
    sender_name = request.json.get('sender_name')

    smtp_server = GMAIL_SMTP_SERVER
    port = GMAIL_PORT
    username = GMAIL_USERNAME
    password = GMAIL_PASSWORD

    if agent == 'ahasend':
        smtp_server = AHA_SMTP_SERVER
        port = AHA_PORT
        username = AHA_USERNAME
        password = AHA_PASSWORD

    if agent == 'other' or api_key != API_KEY:
        smtp_server = request.json.get('smtp_server')
        port = request.json.get('port')
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None or smtp_server is None or port is None or username == '' or password == '' or smtp_server == '' or port == '':
            print(username, password, smtp_server, from_email, to_email, subject, api_key, agent, port, sep=", ")
            return 'Missing Parameters or wrong API Key', 400

    if not isinstance(port, int):
        port = int(port)

    if from_email is None or to_email is None or subject is None or sender_name is None or (
            plain_body is None and fancy_body is None):
        print(username, password, smtp_server, from_email, to_email, subject, api_key, agent,port, sep=", ")
        return f'Missing Parameters is from_email {from_email} to_email {to_email} subject {subject} sender_name {sender_name}', 400
    else:
        if is_html:
            res = send_fancy_email(smtp_server, port, username, password, from_email, to_email, subject, plain_body,
                                   fancy_body, sender_name)
            if res:
                return 'Success', 200
            else:
                return 'Failed', 500
        else:
            res = send_plain_email(smtp_server, port, username, password, from_email, to_email, subject, plain_body,
                                   sender_name)
            if res:
                return 'Success', 200
            else:
                return 'Failed', 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5005)
