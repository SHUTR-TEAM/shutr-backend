from datetime import datetime, timedelta
from bson import ObjectId
import re
import calendar
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
    photographer_id = request.query_params.get('photographer_id', None)
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    
    bookings = Booking.objects.all()
    
    if photographer_id:
        bookings = bookings.filter(photographer_id=photographer_id)

    if month and year:
        try:
            month_int = int(month)
            year_int = int(year)
            
            # Convert month number to abbreviation dynamically
            month_abbr = calendar.month_abbr[month_int]
            
            date_pattern = rf"\b{month_abbr} \d{{1,2}} {year_int}\b"
            
            bookings = bookings.filter(event__date__regex=date_pattern)
        except (ValueError, IndexError):
            return Response(
                {"error": "Invalid month or year format"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    elif month:
        try:
            month_int = int(month)
            month_abbr = calendar.month_abbr[month_int]
            
            date_pattern = rf"\b{month_abbr} \d{{1,2}} \d{{4}}\b"
            bookings = bookings.filter(event__date__regex=date_pattern)
        except (ValueError, IndexError):
            return Response(
                {"error": "Invalid month format"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    elif year:
        try:
            year_int = int(year)
            date_pattern = rf"\b\d{{3}} \w{{3}} \d{{1,2}} {year_int}\b"
            bookings = bookings.filter(event__date__regex=date_pattern)
        except ValueError:
            return Response(
                {"error": "Invalid year format"},
                status=status.HTTP_400_BAD_REQUEST
            )

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
@api_view(['PATCH'])
@csrf_exempt
@permission_classes([AllowAny]) 
def booking_update_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        # if serializer.is_valid():
        booking = serializer.save()

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
    booked_dates = Booking.objects.all().values('event.date')
    booked_dates = [booking['event.date'].date() for booking in booked_dates]

    return Response({"unavailable_dates": booked_dates}, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def get_photographer_booking_dates(request, photographer_id, year_month):
    try:
        # Parse year and month
        year, month = map(int, year_month.split('-'))
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")

        start_date = datetime(year, month, 1)

        end_date = datetime(year, month, 1) + timedelta(days=32)  # Move to next month
        end_date = datetime(end_date.year, end_date.month, 1) - timedelta(seconds=1)

        all_bookings = Booking.objects.filter(photographer_id=photographer_id)

        # Regex pattern to extract the date (ignores timezone)
        date_pattern = r"([A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})"

        filtered_bookings = []
        for booking in all_bookings:
            try:
                match = re.search(date_pattern, booking.event.date)
                if match:
                    date_str = match.group(1)
                    parsed_date = datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S")
                    
                    if start_date <= parsed_date <= end_date:
                        filtered_bookings.append(parsed_date.strftime("%Y-%m-%d"))  # Format as YYYY-MM-DD
                else:
                    print(f"Skipping invalid date format: {booking.event.date}")

            except ValueError:
                print(f"Skipping invalid date format: {booking.event.date}")

        print(f"Found {len(filtered_bookings)} bookings for photographer {photographer_id}")

        return Response({
            "photographer_id": photographer_id, 
            "year_month": year_month, 
            "booking_dates": filtered_bookings
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)