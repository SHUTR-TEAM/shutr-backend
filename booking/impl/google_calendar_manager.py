import logging

from booking.google_calendar_integration import GoogleCalendarAuth


class GoogleCalendarManager:
    """Handles Google Calendar event operations."""

    def __init__(self, user_id):
        self.service = GoogleCalendarAuth(user_id).authenticate()

    def create_event(self, event_date, start_time, end_time, client_details):
        """Creates an event in Google Calendar."""
        event = {
            'summary': f"Booking for {client_details['name']}",
            'location': client_details.get('location', 'Venue Address'),
            'description': f"Photography session for {client_details['name']}",
            'start': {'dateTime': f'{event_date}T{start_time}:00', 'timeZone': 'UTC'},
            'end': {'dateTime': f'{event_date}T{end_time}:00', 'timeZone': 'UTC'},
            'attendees': [{'email': client_details['email']}],
        }

        try:
            created_event = self.service.events().insert(calendarId='primary', body=event).execute()
            logging.info(f"Event created: {created_event.get('htmlLink')}")
            return created_event
        except Exception as e:
            logging.error(f"Error creating event: {e}")
            return None

    def delete_event(self, event_id):
        """Deletes an event from Google Calendar."""
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            logging.info(f"Event {event_id} deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting event: {e}")
