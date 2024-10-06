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

    if api_key != API_KEY:
        print("Wrong API Key", api_key, sep=", ")
        return 'Wrong API Key', 400

    if agent == 'other':
        print("other agent", agent, sep=", ")
        smtp_server = request.json.get('smtp_server')
        port = request.json.get('port')
        username = request.json.get('username')
        password = request.json.get('password')
        if not smtp_server or smtp_server == '':
            print("missing smtp server",smtp_server, sep=", ")
            return 'Missing smtp server', 400
        if not port or port == '':
            print("missing port", port, sep=", ")
            return 'Missing port', 400
        if not username or username == '':
            print("missing username", username, sep=", ")
            return 'Missing username', 400
        if not password or password == '':
            print("missing password", password, sep=", ")
            return 'Missing password', 400

    if not isinstance(port, int):
        port = int(port)

    if from_email is None or from_email == '':
        print("missing from email", from_email, sep=", ")
        return 'Missing from email', 400
    elif to_email is None or to_email == '':
        print("missing to email", to_email, sep=", ")
        return 'Missing to email', 400
    elif subject is None or subject == '':
        print("missing subject", subject, sep=", ")
        return 'Missing subject', 400

    if sender_name is None or sender_name == '':
        print("missing sender name", sender_name, sep=", ")
        return 'Missing sender name', 400

    if is_html is None:
        print("missing is_html", is_html, sep=", ")
        return 'Missing is_html', 400

    if (is_html and (not fancy_body or fancy_body == '')) or (not is_html and (not plain_body or plain_body == '')):
        print("missing body", plain_body, fancy_body, sep=", ")
        return 'Missing body', 400

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
