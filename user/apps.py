# #from django.apps import AppConfig


# #class AuthConfig(AppConfig):
# #    default_auto_field = 'django.db.models.BigAutoField'
# #   name = 'auth'

# from rest_framework import generics
# from .models import Photographer
# from .serializers import PhotographerSerializer

# class PhotographerListCreateView(generics.ListCreateAPIView):
#     queryset = Photographer.objects.all()
#     serializer_class = PhotographerSerializer

# class PhotographerDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Photographer.objects.all()
#     serializer_class = PhotographerSerializer
class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
