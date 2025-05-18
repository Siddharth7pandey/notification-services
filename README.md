# Notification Service

A simple notification system built with FastAPI, RabbitMQ, and Python to send **Email**, **SMS**, and **In-app** notifications.

---

## Features

- REST API endpoints to send notifications and retrieve in-app notifications
- Supports Email via Gmail SMTP
- Supports SMS via Twilio API
- In-app notifications stored in-memory for demo purposes
- Uses RabbitMQ queue for asynchronous notification processing
- Simple retry and error logging in worker

---

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- RabbitMQ server running locally (can use Docker)
- Gmail account with App Password enabled
- Twilio account (free trial is fine)

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
3. Run RabbitMQ Server
Using Docker:

bash
Copy
Edit
docker run -d --hostname rabbit --name rabbitmq -p 5672:5672 rabbitmq:3
Or install RabbitMQ manually from https://www.rabbitmq.com/download.html

4. Configure worker.py
Edit the following variables:

python
Copy
Edit
FROM_EMAIL = "your_email@gmail.com"
EMAIL_APP_PASSWORD = "your_gmail_app_password"

TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"
YOUR_PHONE_NUMBER = "+91xxxxxxxxxx"
5. Run the FastAPI server
bash
Copy
Edit
uvicorn main:app --reload
Server will be running at: http://127.0.0.1:8000

6. Run the worker
In another terminal:

bash
Copy
Edit
python worker.py
Worker will listen for notifications from RabbitMQ and send them accordingly.

7. Test the API
Send notification (POST /notifications) with JSON body, for example:

json
Copy
Edit
{
  "userId": "user1",
  "type": "email",
  "message": "Hello from FastAPI!",
  "meta": {}
}
Get in-app notifications (GET /users/user1/notifications)

Assumptions
In-app notifications are stored in memory and will reset when the worker restarts

Email notifications are sent to your Gmail address by default (you can customize)

SMS notifications are sent to a single phone number (your number)

RabbitMQ is running locally on default port 5672

No authentication or security on API endpoints (for simplicity)

Retry logic is basic (just logs errors)
