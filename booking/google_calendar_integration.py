# import os
# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request

# # If modifying calendar events, we need this scope
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def authenticate_google_account():
#     """Authenticate and return the Google Calendar service."""
#     creds = None
#     # Token is saved in token.pickle for reuse
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     # If no credentials are available, prompt the user to log in
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('calendar', 'v3', credentials=creds)
#     return service

# def update_google_calendar_event(event_date, start_time, end_time, client_details):
#     service = authenticate_google_account()
    
#     # Prepare the event details
#     event = {
#         'summary': f"Booking for {client_details['name']}",
#         'location': 'Venue Address',
#         'description': f"Photography session for {client_details['name']}",
#         'start': {
#             'dateTime': f'{event_date}T{start_time}:00',
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': f'{event_date}T{end_time}:00',
#             'timeZone': 'UTC',
#         },
#         'attendees': [
#             {'email': client_details['email']},
#         ],
#     }

#     # Create or update event
#     created_event = service.events().insert(calendarId='primary', body=event).execute()
#     return created_event

# def remove_google_calendar_event(event_id):
#     service = authenticate_google_account()
#     service.events().delete(calendarId='primary', eventId=event_id).execute()

