from flask import Flask, request
import africastalking
import os
import datetime
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Initialize Africa's Talking SMS service
username = ""
api_key = ""
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Initialize Flask app
app = Flask(__name__)

# Google Calendar authentication and service setup
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
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


@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == "default":
        response = "CON Welcome to the USSD application!\nPlease enter your email address:"
    elif "@" in text:
        email = text

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

        response = "END Calendar reminder successfully set!"
    else:
        response = "CON Invalid input. Please enter a valid email address:"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
