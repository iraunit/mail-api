Flask Email Sender API

This project is a Flask-based web application that allows you to send emails via multiple SMTP servers (like Gmail and AhaSend) using both plain text and HTML formats. The API supports sending through multiple agents with optional authentication, and it provides a way to customize SMTP server credentials dynamically via requests.

This project uses **STARTTLS** for secure connections.
You can change the port number to 465 for Gmail to use SSL/TLS.

Features

	•	Send Plain Emails: Allows sending simple plain-text emails.
	•	Send Fancy Emails: Supports sending HTML-formatted emails with a plain-text fallback.
	•	Multiple SMTP Agents: Supports Gmail, AhaSend, and custom SMTP servers via request parameters.
	•	Dynamic Authentication: Allows providing credentials dynamically for different SMTP servers or agents.
	•	API Key Authentication: Basic API key authentication to secure the email-sending endpoint.

Requirements

Before running this application, you need to set up the following:

	1.	Python 3.9.6
	2.	Install required Python packages via pip:

pip install -r requirements.txt


	3.	Set the following environment variables:
	•	API_KEY: A secret key that authorizes API usage.
	•	GMAIL_USERNAME: Your Gmail username (email address).
	•	GMAIL_PASSWORD: Your Gmail password or App Password if 2FA is enabled.
	•	AHA_USERNAME: Your AhaSend username (email address).
	•	AHA_PASSWORD: Your AhaSend password.

You can configure these environment variables in your shell or using a .env file (using tools like python-dotenv).

Endpoints

GET /

A simple health-check endpoint to verify the server is running.

Response:

	•	200 OK: Returns the message 'Server is Running'.

POST /send

This is the main endpoint to send an email.

Request Body:

The request must contain the following JSON fields:

	•	from: (Required) The sender’s email address.
	•	to: (Required) The recipient’s email address.
	•	subject: (Required) The subject of the email.
	•	plain_body: (Optional) The plain-text body of the email.
	•	fancy_body: (Optional) The HTML-formatted body of the email.
	•	is_html: (Optional) Boolean value. Set to true if sending HTML-formatted email.
	•	api_key: (Required) The API key for authentication.
	•	agent: (Optional) The SMTP agent to use (either gmail, ahasend, or other). Defaults to gmail if not provided.
	•	sender_name: (Required) The sender’s display name (e.g., “John Doe”).

If the agent is set to other, the following additional fields are required:

	•	smtp_server: The SMTP server address (e.g., smtp.example.com).
	•	port: The port to connect to on the SMTP server.
	•	username: The SMTP username for authentication.
	•	password: The SMTP password for authentication.

Example Request:

For Ahasend:

```
{
    "from": "raunit@codingkaro.in",
    "to": "raunitpcs@gmail.com",
    "subject": "Testing API",
    "plain_body": "Hi from my api",
    "is_html": false,
    "api_key": "follow-me-on-twitter-@iraunit",
    "sender_name": "Raunit Verma",
    "agent": "ahasend"
}
```

For Custom SMTP Server:
```
{
    "from": "custom_email@example.com",
    "to": "recipient@example.com",
    "subject": "Custom Server Email",
    "plain_body": "Plain email",
    "fancy_body": "<b>Fancy HTML email</b>",
    "is_html": true,
    "api_key": "your_api_key",
    "agent": "other",
    "sender_name": "Custom Sender",
    "smtp_server": "smtp.customserver.com",
    "port": 587,
    "username": "your_custom_username",
    "password": "your_custom_password"
}
```

Response:

	•	200 OK: Email successfully sent. Returns 'Success'.
	•	400 Bad Request: Missing parameters or invalid API key. Returns an error message with details of missing fields.
	•	500 Internal Server Error: Failed to send the email due to server issues.

Usage

	1.	Clone the Repository:

git clone https://github.com/iraunit/mail-api.git

cd mail-api


	2.	Install Dependencies:

pip install -r requirements.txt


	3.	Set Environment Variables:
Create a .env file in the project root (or set variables manually):

API_KEY=your_api_key

GMAIL_USERNAME=your_gmail_username

GMAIL_PASSWORD=your_gmail_password

AHA_USERNAME=your_ahasend_username

AHA_PASSWORD=your_ahasend_password


	4.	Run the Application:

python app.py


	5.	The application will run on http://0.0.0.0:5005. You can access the API using POST requests to /send.

Example Usage via curl

Send a plain-text email via Gmail:

curl -X POST http://localhost:5005/send \
    -H "Content-Type: application/json" \
    -d '{
        "from": "your_email@gmail.com",
        "to": "recipient@example.com",
        "subject": "Hello",
        "plain_body": "This is a plain text email",
        "html": false,
        "api_key": "your_api_key",
        "agent": "gmail",
        "sender_name": "Your Name"
    }'

Send an HTML email via AhaSend:

curl -X POST http://localhost:5005/send \
    -H "Content-Type: application/json" \
    -d '{
        "from": "your_email@ahasend.com",
        "to": "recipient@example.com",
        "subject": "Fancy Email",
        "plain_body": "This is a plain text email",
        "fancy_body": "<h1>Fancy HTML Email</h1>",
        "html": true,
        "api_key": "your_api_key",
        "agent": "ahasend",
        "sender_name": "Your Name"
    }'

Logging

	•	The application uses logging to capture errors and debug information.
	•	Log levels can be adjusted by configuring the logger in the app.py.

Deployment

To deploy the application in a production environment, follow these steps:

	1.	Use a production-ready WSGI server such as gunicorn:

gunicorn -w 4 app:app -b 0.0.0.0:5005


	2.	Ensure that the necessary environment variables are properly configured.

Security

	1.	API Key Authentication: Always ensure your API_KEY is kept secret. Avoid hardcoding it in the code or public repositories.
	2.	Environment Variables: Store sensitive information (API keys, SMTP passwords) in environment variables or secure vaults.
	3.	Use HTTPS: If deploying this API on a remote server, make sure to configure HTTPS to secure API requests.

Contributing

Feel free to submit issues and pull requests to improve this project!

License

This project is licensed under the MIT License - see the LICENSE file for details.