# from django.shortcuts import render

# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Event
# from .serializers import EventSerializer

# class EventViewSet(viewsets.ViewSet):

#     def list(self, request):
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             event = Event.objects.get(pk=pk)
#             serializer = EventSerializer(event)
#             return Response(serializer.data)
#         except Event.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def update(self, request, pk=None):
#         try:
#             event = Event.objects.get(pk=pk)
#             serializer = EventSerializer(event, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Event.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def destroy(self, request, pk=None):
#         try:
#             event = Event.objects.get(pk=pk)
#             event.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Event.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
