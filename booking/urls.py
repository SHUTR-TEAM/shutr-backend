from django.urls import path

from booking.views import accept_booking, booking_find_all, booking_update_by_id, create_booking, booking_find_by_id, get_photographer_booking_dates

urlpatterns = [
    path('create', create_booking, name='create_booking'),
    path('accept/<str:booking_id>', accept_booking, name='accept_booking'),
    path('', booking_find_all, name='booking_find_all'),
    path('get-all', booking_find_all, name='booking_find_all'),
    path('<str:booking_id>/', booking_find_by_id, name='booking_find_by_id'),
    path('update/<str:booking_id>', booking_update_by_id, name='booking_update_by_id'),
    path('photographers/<str:photographer_id>/bookings/<str:year_month>/', get_photographer_booking_dates, name='photographer_booking_dates'),
]