from django.urls import path
from .views import (
    get_user_from_token,
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
]