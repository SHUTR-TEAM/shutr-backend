from django.urls import path

from .views import get_users

urlpatterns = [
    #http://127.0.0.1:8000/api/users/
     path('users/', get_users), 

]