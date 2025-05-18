from fastapi import FastAPI
from pydantic import BaseModel
import pika, json, sqlite3

app = FastAPI()

# This is your little notebook to keep messages (called a database)
conn = sqlite3.connect('notifications.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS notifications (userId TEXT, message TEXT)')
conn.commit()

class Notification(BaseModel):
    userId: str
    type: str  # email, sms, in-app
    message: str
    meta: dict = {}

def send_to_queue(notification):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(notification))
    connection.close()

@app.post("/notifications")
def add_notification(notification: Notification):
    send_to_queue(notification.dict())
    return {"status": "Your message is on its way!"}

@app.get("/users/{user_id}/notifications")
def read_notifications(user_id: str):
    cursor.execute("SELECT message FROM notifications WHERE userId=?", (user_id,))
    messages = [row[0] for row in cursor.fetchall()]
    return {"your_messages": messages}
