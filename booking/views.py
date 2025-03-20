import datetime
import json
from bson import ObjectId
from rest_framework import status
# from booking.models import Booking
from django.http import JsonResponse
from rest_framework.response import Response
# from core.serializers import BookingSerializer
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from booking.serializer import BookingSerializer
from core.pagination import PaginationWithParams
from django.views.decorators.csrf import csrf_exempt
# from google_auth_oauthlib.flow import InstalledAppFlow
# from booking.google_calendar_integration import update_google_calendar_event, remove_google_calendar_event
from .models.booking import Booking, ToDo
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from mongoengine.queryset import DoesNotExist


# # Create a new booking
# # POST /api/bookings/create
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny]) 
# def create_booking(request):
#     # Deserialize and validate the incoming booking data
#     serializer = BookingSerializer(data=request.data)
#     if serializer.is_valid():
#         booking = serializer.save()
#         return Response({"message": "Booking created successfully", "booking_id": str(booking.id)}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Accept booking
# # POST /api/bookings/accept
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes([AllowAny]) 
# def accept_booking(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=booking_id)
#         if booking.status != "Pending":
#             return Response({"error": "Booking already confirmed or cancelled"}, status=status.HTTP_400_BAD_REQUEST)

#         photographer = booking.photographer
#         # Retrieve the photographer's credentials from the database
#         # credentials = Credentials(
#         #     token=photographer.google_access_token,
#         #     refresh_token=photographer.google_refresh_token,
#         #     token_expiry=photographer.google_token_expiry
#         # )

#         # If the token is expired, refresh it
#         # if credentials.expired:
#         #     credentials.refresh(Request())

#         # Update the booking status
#         booking.status = "Confirmed"
#         booking.save()

#         # Create the event in the photographer's Google Calendar
#         # service = build('calendar', 'v3', credentials=credentials)
#         event = {
#             'summary': booking.event.name,
#             'location': booking.event.address,
#             'description': 'Event for photography booking',
#             'start': {
#                 'dateTime': booking.event.date,
#                 'timeZone': 'America/New_York',  # Use the correct time zone
#             },
#             'end': {
#                 'dateTime': booking.event.date + datetime.timedelta(hours=booking.event.expected_guests),
#                 'timeZone': 'America/New_York',
#             },
#             'attendees': [
#                 {'email': booking.client.email},
#             ],
#         }

#         # Insert the event into Google Calendar
#         # created_event = service.events().insert(calendarId='primary', body=event).execute()

#         return JsonResponse({"message": "Booking confirmed and event added to calendar"}, status=status.HTTP_200_OK)

#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# # Find all bookings
# # GET /api/bookings
# @api_view(['GET'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_find_all(request):
#     paginator = PaginationWithParams()
#     bookings = Booking.objects.all()
#     paginated_bookings = paginator.paginate_queryset(bookings, request)
#     serializer = BookingSerializer(paginated_bookings, many=True)
#     return paginator.get_paginated_response(serializer.data)


# # Find a booking by ID
# # GET /api/bookings/:booking_id
# @api_view(['GET'])
# @csrf_exempt
# def booking_find_by_id(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
#         serializer = BookingSerializer(booking)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# # Update a booking by ID
# # POST /api/bookings/:booking_id/update
# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_update_by_id(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
#         serializer = BookingSerializer(booking, data=request.data, partial=True)
#         if serializer.is_valid():
#             booking = serializer.save()

#             # Update Google Calendar with the updated event
#             try:
#                 # update_google_calendar_event(booking.event.date, booking.event.duration_start, booking.event.duration_end, booking.client)
#                 return Response({"message": "Booking updated and Google Calendar updated"}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"error": f"Failed to update Google Calendar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# # Delete a booking by ID
# # POST /api/bookings/:booking_id/delete
# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_delete_by_id(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
        
#         # Remove the event from Google Calendar
#         try:
#             # remove_google_calendar_event(booking.event.date, booking.event.duration_start, booking.event.duration_end)
#             booking.delete()
#             return Response({"message": "Booking deleted and Google Calendar updated"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": f"Failed to remove from Google Calendar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# # Get unavailable dates (booked dates)
# # GET /api/bookings/unavailable-dates
# @api_view(['GET'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_get_unavailable_dates(request):
#     # Get all bookings and extract the booked dates
#     booked_dates = Booking.objects.all().values('event.date')
#     booked_dates = [booking['event.date'].date() for booking in booked_dates]  # Get just the date part

#     return Response({"unavailable_dates": booked_dates}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_find_by_month(request):
#     month = request.GET.get('month')
#     year = request.GET.get('year')

#     if not month or not year:
#         return Response({"error": "Month and Year are required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         start_date = datetime.datetime(int(year), int(month), 1)
#         end_date = start_date + datetime.timedelta(days=32)
#         end_date = end_date.replace(day=1)  # First day of the next month

#         bookings = Booking.objects.filter(event__date__gte=start_date, event__date__lt=end_date)
#         serializer = BookingSerializer(bookings, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_add_todo(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
#         task_data = request.data.get("task")

#         if not task_data:
#             return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

#         new_task = ToDo(task=task_data)
#         booking.todos.append(new_task)
#         booking.save()

#         return Response({"message": "To-Do task added"}, status=status.HTTP_200_OK)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_edit_todo(request, booking_id, todo_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
#         task_data = request.data.get("task")

#         for todo in booking.todos:
#             if str(todo.id) == todo_id:
#                 todo.task = task_data
#                 booking.save()
#                 return Response({"message": "To-Do task updated"}, status=status.HTTP_200_OK)

#         return Response({"error": "To-Do task not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# @csrf_exempt
# def booking_delete_todo(request, booking_id, todo_id):
#     try:
#         booking = Booking.objects.get(id=ObjectId(booking_id))
#         updated_todos = [todo for todo in booking.todos if str(todo.id) != todo_id]

#         if len(updated_todos) == len(booking.todos):
#             return Response({"error": "To-Do task not found"}, status=status.HTTP_404_NOT_FOUND)

#         booking.todos = updated_todos
#         booking.save()

#         return Response({"message": "To-Do task deleted"}, status=status.HTTP_200_OK)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# ///////////////////////////////////////////////////
# Helper function for date formatting
def format_datetime(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None

# Fetch bookings by view type (month, week, day)
@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_bookings(request):
    view_type = request.GET.get("view", "month")
    date_str = request.GET.get("date")
    if not date_str:
        return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    date = format_datetime(date_str)
    if not date:
        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if view_type == "month":
            start_date = date.replace(day=1)
            end_date = (start_date + datetime.timedelta(days=32)).replace(day=1)
        elif view_type == "week":
            start_date = date - datetime.timedelta(days=date.weekday())
            end_date = start_date + datetime.timedelta(days=6)
        elif view_type == "day":
            start_date = date
            end_date = date + datetime.timedelta(days=1)
        else:
            return Response({"error": "Invalid view type"}, status=status.HTTP_400_BAD_REQUEST)
        
        bookings = Booking.objects.filter(event__date__gte=start_date, event__date__lt=end_date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch a booking by ID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# Create a new booking
@api_view(['POST'])
@permission_classes([AllowAny])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        return Response({"message": "Booking created", "booking_id": str(booking.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update booking details
@api_view(['POST'])
@permission_classes([AllowAny])
def update_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete a booking
@api_view(['POST'])
@permission_classes([AllowAny])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        booking.delete()
        return Response({"message": "Booking deleted"}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

# To-Do List Management
@api_view(['POST'])
@permission_classes([AllowAny])
def add_todo(request, booking_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        task_data = request.data.get("task")
        if not task_data:
            return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)
        new_task = ToDo(task=task_data)
        booking.todos.append(new_task)
        booking.save()
        return Response({"message": "To-Do task added"}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_todo(request, booking_id, todo_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        task_data = request.data.get("task")
        for todo in booking.todos:
            if str(todo.id) == todo_id:
                todo.task = task_data
                booking.save()
                return Response({"message": "To-Do task updated"}, status=status.HTTP_200_OK)
        return Response({"error": "To-Do task not found"}, status=status.HTTP_404_NOT_FOUND)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def delete_todo(request, booking_id, todo_id):
    try:
        booking = Booking.objects.get(id=ObjectId(booking_id))
        updated_todos = [todo for todo in booking.todos if str(todo.id) != todo_id]
        if len(updated_todos) == len(booking.todos):
            return Response({"error": "To-Do task not found"}, status=status.HTTP_404_NOT_FOUND)
        booking.todos = updated_todos
        booking.save()
        return Response({"message": "To-Do task deleted"}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_task_to_date(request, booking_date):
    try:
        task_data = request.data.get("task")
        if not task_data:
            return Response({"error": "Task is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find or create a booking for the date
        booking, created = Booking.objects.get_or_create(event__date=booking_date)

        new_task = ToDo(task=task_data)
        booking.todos.append(new_task)
        booking.save()

        return Response({"message": "Task added successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# /////////////////////////////////////////////////////
# @csrf_exempt
# def get_bookings(request):
#     """ Fetch bookings for a given photographer in a specific month, including To-Dos. """
#     if request.method == "GET":
#         photographer_id = request.GET.get("photographer_id")
#         year = int(request.GET.get("year", datetime.datetime.utcnow().year))
#         month = int(request.GET.get("month", datetime.datetime.utcnow().month))

#         if not photographer_id:
#             return JsonResponse({"error": "Photographer ID is required"}, status=400)

#         # Find bookings for the specified month
#         bookings = Booking.objects(
#             photographer_id=photographer_id,
#             event__date__startswith=f"{year}-{str(month).zfill(2)}"
#         )

#         # Convert MongoDB documents to JSON serializable format
#         bookings_list = []
#         for booking in bookings:
#             bookings_list.append({
#                 "id": str(booking.id),
#                 "title": f"{booking.event.type} - {booking.client.first_name} {booking.client.last_name}",
#                 "start": booking.event.date,  # ISO format
#                 "address": booking.event.address,
#                 "todos": [{"task": todo.task} for todo in booking.todos]  # Include To-Dos
#             })

#         return JsonResponse({"events": bookings_list}, safe=False)



# @csrf_exempt
# def add_todo(request, booking_id):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             task = data.get("task")

#             if not task:
#                 return JsonResponse({"error": "Task is required"}, status=400)

#             booking = Booking.objects.get(id=booking_id)
#             new_todo = ToDo(task=task)
#             booking.todos.append(new_todo)
#             booking.save()

#             return JsonResponse({"message": "To-Do added successfully!", "todo": task}, status=200)

#         except DoesNotExist:
#             return JsonResponse({"error": "Booking not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
        

# @csrf_exempt
# def update_todo(request, booking_id):
#     if request.method == "PUT":
#         try:
#             data = json.loads(request.body)
#             task_index = data.get("task_index")
#             new_task = data.get("task")

#             if task_index is None or new_task is None:
#                 return JsonResponse({"error": "Task index and new task are required"}, status=400)

#             booking = Booking.objects.get(id=booking_id)

#             if task_index < 0 or task_index >= len(booking.todos):
#                 return JsonResponse({"error": "Invalid task index"}, status=400)

#             booking.todos[task_index].task = new_task
#             booking.save()

#             return JsonResponse({"message": "To-Do updated successfully!", "task": new_task}, status=200)

#         except DoesNotExist:
#             return JsonResponse({"error": "Booking not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
        

# @csrf_exempt
# def delete_todo(request, booking_id):
#     if request.method == "DELETE":
#         try:
#             data = json.loads(request.body)
#             task_index = data.get("task_index")

#             if task_index is None:
#                 return JsonResponse({"error": "Task index is required"}, status=400)

#             booking = Booking.objects.get(id=booking_id)

#             if task_index < 0 or task_index >= len(booking.todos):
#                 return JsonResponse({"error": "Invalid task index"}, status=400)

#             deleted_task = booking.todos.pop(task_index)
#             booking.save()

#             return JsonResponse({"message": "To-Do deleted successfully!", "task": deleted_task.task}, status=200)

#         except DoesNotExist:
#             return JsonResponse({"error": "Booking not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# def get_todos(request, booking_id):
#     if request.method == "GET":
#         try:
#             booking = Booking.objects.get(id=booking_id)
#             todos = [{"task": todo.task} for todo in booking.todos]

#             return JsonResponse({"todos": todos}, status=200)

#         except DoesNotExist:
#             return JsonResponse({"error": "Booking not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
