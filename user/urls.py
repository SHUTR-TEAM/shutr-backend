from django.urls import path
from .views import (
    get_user_from_token,
    google_auth_callback,
    google_calendar_init,
    # list_calendar_events,
    refresh_token,
    user_login,
    user_logout,
    user_signup,
    verify_token
)

urlpatterns = [
    path("signup", user_signup, name="user-signup"),
    path("signin", user_login, name="user-login"),
    path("get-user", get_user_from_token, name="get_user_from_token-signup"),
    path("jwt/refresh", refresh_token, name="jwt-refresh"),
    path("jwt/verify", verify_token, name="jwt-verify"),
    path("logout", user_logout, name="user-logout"),

    # Google calendar
    path('connect-google-calendar', google_calendar_init, name='google_calendar_init'),
    path('google-auth-callback', google_auth_callback, name='google_auth_callback'),
    # path('calendar-events', list_calendar_events, name='list_calendar_events'),
]