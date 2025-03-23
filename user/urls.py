from django.urls import path
from .views import (
    get_user_from_token,
    google_auth_callback,
    google_calendar_init,
    # list_calendar_events,
    refresh_token,
    user_delete_by_id,
    user_find_all,
    user_find_by_id,
    user_login,
    user_logout,
    user_signup,
    user_update_by_id,
    verify_token
)

urlpatterns = [
    path("auth/signup", user_signup, name="user-signup"),
    path("auth/signin", user_login, name="user-login"),
    path("auth/get-user", get_user_from_token, name="get_user_from_token-signup"),
    path("auth/jwt/refresh", refresh_token, name="jwt-refresh"),
    path("auth/jwt/verify", verify_token, name="jwt-verify"),
    path("auth/logout", user_logout, name="user-logout"),

    # Google calendar
    path('auth/connect-google-calendar', google_calendar_init, name='google_calendar_init'),
    path('auth/google-auth-callback', google_auth_callback, name='google_auth_callback'),
    # path('calendar-events', list_calendar_events, name='list_calendar_events'),

    path('api/users', user_find_all),
    # path('users/create', user_create),
    path('api/users/<str:user_id>', user_find_by_id),
    path('api/users/<str:user_id>/update', user_update_by_id),
    path('api/users/<str:user_id>/delete', user_delete_by_id),
]