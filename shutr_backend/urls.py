from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/',include('portfolio.urls')),
    path('api/', include('chat.urls')),
    path('auth/', include('auth.urls')),
]
