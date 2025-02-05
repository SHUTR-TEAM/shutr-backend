from django.urls import path, re_path

from chat import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    
# ]

websocket_urlpatterns = [
    path("ws/chat/<str:room_id>", consumers.ChatConsumer.as_asgi()),
]