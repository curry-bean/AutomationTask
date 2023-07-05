from flask import Flask, request, session
import africastalking
import os
import datetime
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText

# Initialize Africa's Talking SMS service
africastalking_username = "sandbox"
africastalking_api_key = "36e295766b1cc1af7c6db221683bd7322272f1d7f18e1243b9da5597436428e0"
africastalking.initialize(africastalking_username, africastalking_api_key)
sms = africastalking.SMS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your-secret-key"

# Google Calendar authentication and service setup
google_api_key = "AIzaSyCQ09S8skpBmSh3wmVnkv32YzM2PRvuBdM"
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_calendar():
    creds = None
    if os.environ.get('GOOGLE_API_KEY'):
        creds = os.environ.get('GOOGLE_API_KEY')
    else:
        creds = google_api_key
    service = build('calendar', 'v3', developerKey=creds)
    return service


service = authenticate_google_calendar()


def create_calendar_event(email, event_name, start_time, end_time):
    event = {
        'summary': event_name,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Your Time Zone',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Your Time Zone',
        },
        'attendees': [
            {'email': email}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 1440}  # Send email notification 24 hours before the event
            ]
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Reminder created:', event['htmlLink'])


def send_email_notification(email, event_date):
    sender_email = "snclrn@gmail.com"  # Replace with your email address
    receiver_email = email
    smtp_server = "smtp.example.com"  # Replace with your SMTP server details
    smtp_port = 587
    smtp_username = "snclrn@gmail.com"  # Replace with your email username
    smtp_password = "fhdeitvsvaaohefa"  # Replace with your email password

    subject = "Monthly Reminder"
    body = f"You have a monthly reminder on {event_date}."

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email notification sent successfully.")
    except Exception as e:
        print("Error sending email notification:", str(e))


@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == "":
        # First USSD request
        response = "CON Welcome to the USSD application!\nPlease enter your email address:"
    elif "@" in text:
        email = text

        # Save email in session
        session['email'] = email

        # Determine the last Wednesday of the month
        today = datetime.date.today()
        last_day = datetime.date(today.year, today.month, 1) - datetime.timedelta(days=1)
        while last_day.weekday() != 2:  # 2 represents Wednesday
            last_day -= datetime.timedelta(days=1)

        # Calculate start and end times for the event
        start_time = datetime.datetime.combine(last_day, datetime.time(10, 0))
        end_time = datetime.datetime.combine(last_day, datetime.time(12, 0))

        # Create the Google Calendar reminder event
        create_calendar_event(email, "Monthly Reminder", start_time, end_time)

        # Send SMS using Africa's Talking
        message = f"Reminder created for {email} on {start_time.date()}"
        sms.send(message, [phone_number])

        # Send email notification
        send_email_notification(email, start_time.date())

        response = "END Calendar reminder successfully set! SMS and email notifications sent."
    else:
        response = "CON Invalid input. Please enter a valid email address:"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
