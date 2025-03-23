from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/',include('portfolio.urls')),
    path('api/', include('chat.urls')),
    # path('auth/', include('auth.urls')),
    path('auth/', include('user.urls')),
    path('vertex_multimodaling/', include('vertex_multimodaling.urls')),
]


# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


