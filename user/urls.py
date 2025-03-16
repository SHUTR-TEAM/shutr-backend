# from django.urls import path
# from .views import PhotographerSignUpView, PhotographerSignInView, PhotographerLogoutView

# urlpatterns = [
#     path('signup/', PhotographerSignUpView.as_view(), name='photographer-signup'),
#     path('signin/', PhotographerSignInView.as_view(), name='photographer-signin'),
#     path('logout/', PhotographerLogoutView.as_view(), name='photographer-logout'),
# ]
from django.urls import path, re_path
from .views import (
    CustomerSignupView,
    PhotographerSignupView,
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView
)

urlpatterns = [
    
    path('signup/customer/', CustomerSignupView.as_view(), name='customer-signup'),
    path('signup/photographer/', PhotographerSignupView.as_view(), name='photographer-signup'),
    
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]
