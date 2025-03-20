# import os
# import json
# import logging
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

# from booking.models.google_auth_token import GoogleOAuthToken


# # Setup logging
# logging.basicConfig(level=logging.INFO)

# # Google API Scope
# SCOPES = ['https://www.googleapis.com/auth/calendar']


# class GoogleCalendarAuth:
#     """Handles Google Calendar API authentication securely using Django models."""

#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.credentials = self.load_credentials()

#     def load_credentials(self):
#         """Load OAuth credentials from MongoDB via Django model."""
#         try:
#             stored_token = GoogleOAuthToken.objects.filter(user_id=self.user_id).first()

#             if stored_token:
#                 creds = Credentials.from_authorized_user_info(stored_token.token)
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
#                     self.save_credentials(creds)  # Update refreshed token
#                 return creds

#         except Exception as e:
#             logging.error(f"Error loading credentials: {e}")

#         return None

#     def save_credentials(self, creds):
#         """Save OAuth credentials to MongoDB via Django model."""
#         try:
#             GoogleOAuthToken.objects.update_or_create(
#                 user_id=self.user_id,
#                 defaults={"token": json.loads(creds.to_json())}
#             )
#         except Exception as e:
#             logging.error(f"Error saving credentials: {e}")

#     def authenticate(self):
#         """Authenticate and return Google Calendar service."""
#         creds = self.load_credentials()

#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"), SCOPES
#                 )
#                 creds = flow.run_local_server(port=0)
#             self.save_credentials(creds)

#         return build('calendar', 'v3', credentials=creds)
