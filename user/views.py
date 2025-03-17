from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from .serializers import  PhotographerSerializer,  UserSerializer


def set_token_cookies(response, access_token, refresh_token=None):
    response.set_cookie(
        'access', access_token,
        max_age=settings.AUTH_COOKIE_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
    )

    if refresh_token:
        response.set_cookie(
            'refresh', refresh_token,
            max_age=settings.AUTH_COOKIE_MAX_AGE,
            path=settings.AUTH_COOKIE_PATH,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            samesite=settings.AUTH_COOKIE_SAMESITE
        )


# User Signup
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def user_signup(request):
    """Creates a new User or Photographer."""
    role = request.data.get("role", "user")
    
    if role == "photographer":
        serializer = PhotographerSerializer(data=request.data)
    else:
        serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created", "user_id": str(user.id)}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login (JWT Token Generation)
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def user_login(request):
    """Authenticate user and return JWT tokens in response cookies."""
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    response = Response({
        "message": "Login successful",
        "access": access_token,
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)

    # Set tokens in cookies
    set_token_cookies(response, access_token, refresh)

    return response


# Token Refresh (Extend Access Token)
@api_view(['POST'])
@csrf_exempt
def refresh_token(request):
    """Refresh JWT access token using the refresh token from cookies."""
    refresh_token = request.data.get('refresh') or request.COOKIES.get('refresh')

    if not refresh_token:
        return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

    response = Response({"access": new_access_token}, status=status.HTTP_200_OK)
    response.set_cookie(
        'access', new_access_token,
        max_age=settings.AUTH_COOKIE_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
    )

    return response


# Verify Token
@api_view(['POST'])
@csrf_exempt
def verify_token(request):
    """Verify if access token is valid."""
    access_token = request.COOKIES.get('access') or request.data.get('token')

    if not access_token:
        return Response({"error": "No access token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        RefreshToken(access_token)  # This will raise an error if invalid
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


# Logout (Clear Cookies)
@api_view(['POST'])
@csrf_exempt
def user_logout(request):
    """Logs out user by clearing JWT cookies."""
    response = Response({"message": "Logged out"}, status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response