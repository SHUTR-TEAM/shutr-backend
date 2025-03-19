import datetime
from bson import ObjectId
from httplib2 import Credentials
from rest_framework import status
# from booking.models import Booking
from django.http import JsonResponse
from googleapiclient.discovery import build
from rest_framework.response import Response
# from core.serializers import BookingSerializer
from rest_framework.decorators import api_view
from google.auth.credentials import Credentials
from booking.serializer import BookingSerializer
from core.pagination import PaginationWithParams
from google.auth.transport.requests import Request
from django.views.decorators.csrf import csrf_exempt
# from google_auth_oauthlib.flow import InstalledAppFlow
from booking.google_calendar_integration import update_google_calendar_event, remove_google_calendar_event
from .models.booking import Booking
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


# Create a new booking
# POST /api/bookings/create
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) 
def create_booking(request):
    # Deserialize and validate the incoming booking data
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        return Response({"message": "Booking created successfully", "booking_id": str(booking.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Accept booking
# POST /api/bookings/accept
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) 
def accept_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if booking.status != "Pending":
            return Response({"error": "Booking already confirmed or cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        photographer = booking.photographer
        # Retrieve the photographer's credentials from the database
        credentials = Credentials(
            token=photographer.google_access_token,
            refresh_token=photographer.google_refresh_token,
            token_expiry=photographer.google_token_expiry
        )

        # If the token is expired, refresh it
        if credentials.expired:
            credentials.refresh(Request())

        # Update the booking status
        booking.status = "Confirmed"
        booking.save()

        # Create the event in the photographer's Google Calendar
        service = build('calendar', 'v3', credentials=credentials)
        event = {
            'summary': booking.event.name,
            'location': booking.event.venue.address,
            'description': 'Event for photography booking',
            'start': {
                'dateTime': booking.event.date,
                'timeZone': 'America/New_York',  # Use the correct time zone
            },
            'end': {
                'dateTime': booking.event.date + datetime.timedelta(hours=booking.event.expected_guests),
                'timeZone': 'America/New_York',
            },
            'attendees': [
                {'email': booking.client.email},
            ],
        }

        # Insert the event into Google Calendar
        created_event = service.events().insert(calendarId='primary', body=event).execute()

        return JsonResponse({"message": "Booking confirmed and event added to calendar", "event_id": created_event['id']}, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# Find all bookings
# GET /api/bookings
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_find_all(request):
    paginator = PaginationWithParams()
    bookings = Booking.objects.all()
    paginated_bookings = paginator.paginate_queryset(bookings, request)
    serializer = BookingSerializer(paginated_bookings, many=True)
    return paginator.get_paginated_response(serializer.data)


# Find a booking by ID
# GET /api/bookings/:booking_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_find_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# Update a booking by ID
# POST /api/bookings/:booking_id/update
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_update_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            booking = serializer.save()

            # Update Google Calendar with the updated event
            try:
                update_google_calendar_event(booking.event.date, booking.event.duration_start, booking.event.duration_end, booking.client)
                return Response({"message": "Booking updated and Google Calendar updated"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to update Google Calendar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# Delete a booking by ID
# POST /api/bookings/:booking_id/delete
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_delete_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        
        # Remove the event from Google Calendar
        try:
            remove_google_calendar_event(booking.event.date, booking.event.duration_start, booking.event.duration_end)
            booking.delete()
            return Response({"message": "Booking deleted and Google Calendar updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to remove from Google Calendar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# Get unavailable dates (booked dates)
# GET /api/bookings/unavailable-dates
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_get_unavailable_dates(request):
    # Get all bookings and extract the booked dates
    booked_dates = Booking.objects.all().values('event.date')
    booked_dates = [booking['event.date'].date() for booking in booked_dates]  # Get just the date part

    return Response({"unavailable_dates": booked_dates}, status=status.HTTP_200_OK)

