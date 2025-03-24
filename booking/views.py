from datetime import datetime
from datetime import timedelta
from bson import ObjectId
# from httplib2 import Credentials
from google.oauth2.credentials import Credentials
from rest_framework import status
# from booking.models import Booking
from django.http import JsonResponse
from googleapiclient.discovery import build
from rest_framework.response import Response
# from core.serializers import BookingSerializer
from rest_framework.decorators import api_view
# from google.auth.credentials import Credentials
from booking.serializer import BookingSerializer
from core.pagination import PaginationWithParams
from google.auth.transport.requests import Request
from django.views.decorators.csrf import csrf_exempt
# from google_auth_oauthlib.flow import InstalledAppFlow
from booking.google_calendar_integration import update_google_calendar_event, remove_google_calendar_event
from user.models import User
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

        photographer = User.objects.get(id=ObjectId("67dd71aee5948704445e32f0"))
        # photographer = booking.photographer
        # Retrieve the photographer's credentials from the database
        credentials = Credentials(
            token=photographer.google_access_token,
            refresh_token=photographer.refresh_token,
            expiry=datetime.strptime(photographer.google_token_expiry, '%Y-%m-%dT%H:%M:%S.%f'),
            token_uri='https://oauth2.googleapis.com/token',  # Google OAuth2 token URI
            client_id="35440314571-ktdqppuvs0a53fan7f7tfsa4ch76m6bi.apps.googleusercontent.com",        # Your client ID
            client_secret="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",
        )

        # If the token is expired, refresh it
        if credentials.expired:
            credentials.refresh(Request())

        # Update the booking status
        booking.status = "Confirmed"
        booking.photographer_id = ObjectId("67dd71aee5948704445e32f0")
        booking.client_id = ObjectId("67dd71aee5948704445e32f0")
        booking.save()

        # Create the event in the photographer's Google Calendar
        service = build('calendar', 'v3', credentials=credentials)
        
        # Assuming booking.event.date is in string format like 'YYYY-MM-DD HH:MM:SS'
        start_time = datetime.strptime(booking.event.date, '%Y-%m-%d')

        # Calculate end time (assuming event duration is 5 hours)
        end_time = start_time + timedelta(hours=5)

        # Prepare the event data
        event = {
            'summary': booking.event.type,
            'location': booking.event.address,
            'description': 'Event for photography booking',
            'start': {
                'dateTime': start_time.isoformat(),  # Convert start_time to ISO format
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time.isoformat(),  # Convert end_time to ISO format
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

# # Find all bookings
# # GET /api/bookings
# @api_view(['GET'])
# @csrf_exempt
# @permission_classes([AllowAny]) 
# def booking_find_all(request):
#     paginator = PaginationWithParams()
#     bookings = Booking.objects.all()
#     serializer = BookingSerializer(bookings, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def booking_find_all(request):
    # Get query parameters
    photographer_id = request.query_params.get('photographer_id', None)
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    
    # Start with all bookings
    bookings = Booking.objects.all()
    
    # Apply filters if provided
    if photographer_id:
        bookings = bookings.filter(photographer_id=photographer_id)
    
    # Filter by month and year if provided
    if month and year:
        # Convert to integers
        try:
            month_int = int(month)
            year_int = int(year)
            
            # Since event.date is a StringField, we need to use regex to match
            # Assuming event.date format contains year and month (e.g., "2025-03-15")
            # This regex pattern looks for year-month at the beginning of the date string
            date_pattern = f"^{year_int}-{month_int:02d}"
            bookings = bookings.filter(event__date__regex=date_pattern)
        except ValueError:
            # Handle invalid month or year values
            return Response(
                {"error": "Invalid month or year format"},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif month:
        # Filter by month only
        try:
            month_int = int(month)
            # Match month part in date string (assumes format like "YYYY-MM-DD")
            date_pattern = f"-{month_int:02d}-"
            bookings = bookings.filter(event__date__regex=date_pattern)
        except ValueError:
            return Response(
                {"error": "Invalid month format"},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif year:
        # Filter by year only
        try:
            year_int = int(year)
            # Match year part in date string
            date_pattern = f"^{year_int}-"
            bookings = bookings.filter(event__date__regex=date_pattern)
        except ValueError:
            return Response(
                {"error": "Invalid year format"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Use pagination if needed
    # paginator = PaginationWithParams()
    # result_page = paginator.paginate_queryset(bookings, request)
    # serializer = BookingSerializer(result_page, many=True)
    # return paginator.get_paginated_response(serializer.data)

    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_find_by_id(request, booking_id):
    try:
        # Ensure valid ObjectId
        if not ObjectId.is_valid(booking_id):
            return JsonResponse({"error": "Invalid booking ID format"}, status=400)

        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def get_photographer_booking_dates(request, photographer_id, year_month):
    try:
        try:
            year, month = year_month.split('-')
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12")
        except ValueError as e:
            return Response({"error": f"Invalid year-month format. Should be YYYY-MM. {str(e)}"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate start and end dates for the month
        start_date = datetime.datetime(year, month, 1)
        
        # Determine the last day of the month
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
        
        # Find bookings for the photographer in the given month
        bookings = Booking.objects.filter(
            photographer_id=photographer_id,
            event__date__gte=start_date.strftime('%Y-%m-%d'),
            event__date__lte=end_date.strftime('%Y-%m-%d')
        )
        
        # Extract dates from bookings
        booking_dates = [booking.event.date for booking in bookings]
        
        return Response({
            "photographer_id": photographer_id, 
            "year_month": year_month, 
            "booking_dates": booking_dates
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)