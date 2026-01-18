
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText

# Load configuration
with open('/Users/antonioreid/FOD_ATS/reminder_config.json') as f:
    config = json.load(f)

# Email settings (UPDATE THESE BEFORE USE)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USER = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = config['email']
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)

def check_reminders():
    today = datetime.now().strftime('%Y-%m-%d')
    for item in config['schedule']:
        if item['date'] == today:
            subject = f"Reminder: {item['name']}"
            body = f"FOD ATS Plan Reminder\n\n{item['message']}\n\nDate: {today}"
            send_email(subject, body)
            print(f"Reminder sent: {item['name']}")

if __name__ == "__main__":
    check_reminders()
