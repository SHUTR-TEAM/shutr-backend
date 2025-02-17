
'''
from django.urls import path
from .views import HeaderListApiView,HeaderDetailsAPIView


urlpatterns= [
    path('headers',HeaderListApiView.as_view(),name="headers"),
    path('headers/<str:slug>',HeaderDetailsAPIView.as_view(),name="campaign"),
    
]

'''

from django.urls import path

from .views import (
    header_create,
    header_find_all,
    header_find_by_id,
    header_update_by_id,
    header_delete_by_id,

    gallery_create,
    gallery_find_all,
    gallery_find_by_id,
    gallery_update_by_id,
    gallery_delete_by_id,

)

urlpatterns = [
    path('headers', header_find_all),
    path('headers/create', header_create),
    path('headers/<str:header_id>', header_find_by_id),
    path('headers/<str:header_id>/update', header_update_by_id),
    path('headers/<str:header_id>/delete', header_delete_by_id),

    path('galleries', gallery_find_all),
    path('galleries/create', gallery_create),
    path('galleries/<str:gallery_id>', gallery_find_by_id),
    path('galleries/<str:gallery_id>/update', gallery_update_by_id),
    path('galleries/<str:gallery_id>/delete', gallery_delete_by_id),
]
