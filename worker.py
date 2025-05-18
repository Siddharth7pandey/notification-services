import pika
import json
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

# ======= Email Settings =======
FROM_EMAIL = "your_email@gmail.com"
EMAIL_APP_PASSWORD = "your_16_char_app_password"

# ======= Twilio Settings =======
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number
YOUR_PHONE_NUMBER = "+91xxxxxxxxxx"  # Your personal phone number to receive SMS

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)

def send_sms(to_number, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"✅ SMS sent! SID: {message.sid}")
    except Exception as e:
        print("❌ SMS failed:", e)

def send_notification(notification):
    notif_type = notification.get('type')
    user_id = notification.get('userId')
    message = notification.get('message')

    if notif_type == 'email':
        # For simplicity, send email to FROM_EMAIL (you can change this logic)
        send_email(FROM_EMAIL, f"Notification for {user_id}", message)

    elif notif_type == 'sms':
        send_sms(YOUR_PHONE_NUMBER, message)

    elif notif_type == 'in-app':
        print(f"In-app notification for {user_id}: {message}")

    else:
        print(f"Unknown notification type: {notif_type}")

def callback(ch, method, properties, body):
    notification = json.loads(body)
    print("Received notification:", notification)
    send_notification(notification)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')

    channel.basic_consume(queue='notifications', on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()

