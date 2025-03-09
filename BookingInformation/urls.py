from django.urls import path
from .views import search_bookings

urlpatterns = [
    path('search/', search_bookings, name='search_bookings'),
]