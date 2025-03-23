
'''
from django.urls import path
from .views import HeaderListApiView,HeaderDetailsAPIView, get_packages


urlpatterns= [
    path('headers',HeaderListApiView.as_view(),name="headers"),
    path('headers/<str:slug>',HeaderDetailsAPIView.as_view(),name="campaign"),
    
]

'''
from django.urls import path
# from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PackageViewSet , get_packages



from .views import (
    header_create,
    header_find_all,
    header_find_by_id,
    header_update_by_id,
    header_delete_by_id,

    gallery_create,
    gallery_find_all,
    gallery_find_by_id,
    # gallery_update_by_id,
    gallery_delete_by_id,
    gallery_delete_photo,
    gallery_find_by_photographer,


    package_create,
    package_delete_by_id,
    package_find_all,
    package_find_by_id,
    package_update_by_id,
    package_update,
    package_find_by_photographerid,
    package_find_by_portfolioid,

    review_create,
    review_find_all,
    review_find_by_id,
    review_update_by_id,
    review_delete_by_id,
    review_find_by_photographer,

    social_links_create,
    social_links_find_by_photographer,
    social_links_update,
    social_links_delete,


)

# Initialize the router and register the viewset
router = DefaultRouter()
# router.register(r'packages', PackageViewSet, basename="package")


urlpatterns = [
    path('headers', header_find_all),
    path('headers/create', header_create),
    path('headers/<str:header_id>', header_find_by_id),
    path('headers/<str:header_id>/update', header_update_by_id),
    path('headers/<str:header_id>/delete', header_delete_by_id),

    path('galleries', gallery_find_all),
    path('galleries/create', gallery_create),
    path('galleries/<str:gallery_id>', gallery_find_by_id),
    # path('galleries/<str:gallery_id>/update', gallery_update_by_id),
    path('galleries/<str:gallery_id>/delete', gallery_delete_by_id),
    # path('galleries/<str:gallery_id>/delete_photo', gallery_delete_photo),
    path('galleries/<str:portfolio_id>/delete_photo', gallery_delete_photo),
    path('galleries/photographer/<str:portfolio_id>/',gallery_find_by_photographer),


    path('reviews', review_find_all),
    path('reviews/create', review_create),
    path('reviews/<str:review_id>', review_find_by_id),
    path('reviews/<str:review_id>/update', review_update_by_id),
    path('reviews/delete/<str:review_id>', review_delete_by_id),
    # path('reviews/photographer/<str:review_id>',review_find_by_photographer)
    path('reviews/photographer/<str:photographer_id>/', review_find_by_photographer),

    path('packages', package_find_all),
    path('packages/create', package_create),
    path('packages/<str:package_id>', package_find_by_id),
    path('packages/photographer/<str:photographer_id>', package_find_by_photographerid),
    path('packages/portfolio/<str:portfolio_id>',package_find_by_portfolioid),
    # path('packages/<str:package_id>/update', package_update_by_id),
    path('packages/<str:package_id>/update', package_update),

    path('packages/<str:package_id>/delete', package_delete_by_id),
    
    # path('packages', get_packages, name='get_packages'),


    path('SocialLinks/create', social_links_create),
    path('SocialLinks/photographer/<str:portfolio_id>/',social_links_find_by_photographer),
    path('SocialLinks/photographer/update/<str:portfolio_id>',social_links_update),
    path('SocialLinks/delete/<str:portfolio_id>', social_links_delete),

    # path('', include(router.urls)),
]
