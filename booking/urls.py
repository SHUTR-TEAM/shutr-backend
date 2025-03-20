# from django.urls import path

# from booking.views import accept_booking, booking_find_all, create_booking

# urlpatterns = [
#     path('create', create_booking, name='create_booking'),
#     path('accept', accept_booking, name='accept_booking'),
#     path('', booking_find_all, name='booking_find_all'),

# ]

from django.urls import path
from .views import (
    create_booking, 
    accept_booking, 
    booking_find_all, 
    booking_find_by_id, 
    booking_update_by_id, 
    booking_delete_by_id, 
    booking_get_unavailable_dates
)

urlpatterns = [
    path('api/bookings/create', create_booking, name='create_booking'),
    path('api/bookings/accept/<str:booking_id>', accept_booking, name='accept_booking'),
    path('api/bookings', booking_find_all, name='booking_find_all'),
    path('api/bookings/<str:booking_id>', booking_find_by_id, name='booking_find_by_id'),
    path('api/bookings/<str:booking_id>/update', booking_update_by_id, name='booking_update_by_id'),
    path('api/bookings/<str:booking_id>/delete', booking_delete_by_id, name='booking_delete_by_id'),
    path('api/bookings/unavailable-dates', booking_get_unavailable_dates, name='booking_get_unavailable_dates'),
    path('api/bookings/', fetch_bookings, name='fetch_bookings'),#add new

    path('api/bookings/<str:booking_date>/add-task/', add_task_to_date, name='add-task'),
]
