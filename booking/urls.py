from django.urls import path

from booking.views import accept_booking, booking_find_all, create_booking, booking_find_by_id

urlpatterns = [
    path('create', create_booking, name='create_booking'),
    path('accept', accept_booking, name='accept_booking'),
    path('', booking_find_all, name='booking_find_all'),
    path('<str:booking_id>/', booking_find_by_id, name='booking_find_by_id'),
]