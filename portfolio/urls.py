
'''
from django.urls import path
from .views import HeaderListApiView,HeaderDetailsAPIView, get_packages


urlpatterns= [
    path('headers',HeaderListApiView.as_view(),name="headers"),
    path('headers/<str:slug>',HeaderDetailsAPIView.as_view(),name="campaign"),
    
]

'''
<<<<<<< Updated upstream
from django.urls import path
from .views import get_packages

=======

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PackageViewSet
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

# from .views import PackageList
#from .views import PackageListCreateView, PackageRetrieveUpdateDestroyView,
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

    review_create,
    review_find_all,
    review_find_by_id,
    review_update_by_id,
    review_delete_by_id,

    PackageListCreateView, 
    PackageRetrieveUpdateDestroyView,
)

<<<<<<< Updated upstream
=======
# Initialize the router and register the viewset
# router = DefaultRouter()
# router.register(r'packages', PackageViewSet, basename="package")


>>>>>>> Stashed changes
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

    path('reviews', review_find_all),
    path('reviews/create', review_create),
    path('reviews/<str:review_id>', review_find_by_id),
    path('reviews/<str:review_id>/update', review_update_by_id),
    path('reviews/<str:review_id>/delete', review_delete_by_id),

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    path('packages/', get_packages, name='get_packages'),
=======
=======
>>>>>>> Stashed changes
    # path('', include(router.urls)),
    # path('packages/', get_packages, name='get_packages'),

    #path('packages/', PackageList.as_view(), name='package-list'),

     # Package URLs
    path('packages/', PackageListCreateView.as_view(), name='package-list-create'),
    path('packages/<int:pk>/', PackageRetrieveUpdateDestroyView.as_view(), name='package-retrieve-update-destroy'),

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
]
