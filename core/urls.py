from django.urls import path

from core.views.user import (
    user_create,
    user_find_all,
    user_find_by_id,
    user_update_by_id,
    user_delete_by_id,
)

urlpatterns = [
    path('users', user_find_all),
    path('users/create', user_create),
    path('users/<str:user_id>', user_find_by_id),
    path('users/<str:user_id>/update', user_update_by_id),
    path('users/<str:user_id>/delete', user_delete_by_id),
]