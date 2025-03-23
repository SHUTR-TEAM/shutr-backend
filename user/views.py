import os
import datetime

from bson import ObjectId
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.models import Photographer, User
from user.serializers import PhotographerSerializer, UserSerializer

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


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

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "message": "User created",
            "access": access_token,
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)

        # Set tokens in cookies
        set_token_cookies(response, access_token, refresh)

        return response

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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny]) 
@csrf_exempt
def user_logout(request):
    """Logs out user by clearing JWT cookies."""
    response = Response({"message": "Logged out"}, status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
def get_user_from_token(request):
    """Fetch user details based on the access token in cookies."""
    access_token = request.COOKIES.get('access')

    if not access_token:
        return Response({"error": "Access token not provided in cookies"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Decode the token to get the user ID
        decoded_token = AccessToken(access_token)
        user_id = decoded_token["user_id"]

        try:
            user = Photographer.objects.get(id=user_id)
            serializer = PhotographerSerializer(user)
        except ObjectDoesNotExist:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)

        # Serialize and return user data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Invalid token or error occurred: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def user_find_all(request):
    
    #Extracts query parameters and saves them to variables
    search = request.GET.get("q", "").strip()
    style = request.GET.get('style', "").strip()
    min_price = request.GET.get("minPrice", "").strip()
    max_price = request.GET.get("maxPrice", "").strip()
    availability = request.GET.get("availability", "").strip()
    experienceLevel = request.GET.get("experienceLevel", "").strip()

    filters = {}

    #Builds a filter dictionary based on provided query parameters for searching and filtering users
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}},
            {"location": {"$regex": search, "$options": "i"}},
        ]
    
    if style:
        filters["tags"] = {"$regex": style, "$options": "i"}

    if min_price and max_price:
        filters["price"] = {"$gte": int(min_price), "$lte": int(max_price)}
    elif min_price:
        filters["price"] = {"$gte": int(min_price)}
    elif max_price:
        filters["price"] = {"$lte": int(max_price)}

    if availability:
        filters["availability"] = availability  

    if experienceLevel:
        filters["experience_level"] = {"$regex": experienceLevel, "$options": "i"}

    try:
        if filters:
            #directly apply MongoDB's raw query filters.
            users_queryset = User.objects(__raw__=filters)

            # Return empty list when no results
            if not users_queryset.count():
                return Response([], status=status.HTTP_200_OK)
        else:
            # Return all users when no filters are applied
            users_queryset = User.objects.all() 

        serializer = UserSerializer(users_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Find a user by ID
# GET /api/users/:user_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def user_find_by_id(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Update a user by ID
# POST /api/users/:user_id/update
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def user_update_by_id(request, user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete a user by ID
# POST /api/users/:user_id/delete
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def user_delete_by_id(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


CLIENT_SECRETS_FILE = "client_secret.json" 
SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = 'http://localhost:3000/google-auth-callback' 

# Google Calendar Integration
# GET /auth/google_calendar/init
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def google_calendar_init(request):
    access_token = request.COOKIES.get('access')

    if not access_token:
        return Response({"error": "Access token not provided in cookies"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Decode the token to get the user ID
        decoded_token = AccessToken(access_token)
        user_id = decoded_token["user_id"]

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            # If not found in User, check the Photographer collection
            user = Photographer.objects.get(id=user_id)

        if os.path.exists(CLIENT_SECRETS_FILE):
            print("File exists")
        else:
            print("File does not exist")

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        # Generate the authorization URL
        state = f"user_id:{user.id}"
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=state
        )

        # Redirect the user to the Google authorization URL
        # return redirect(authorization_url)
        return Response({'authorization_url': authorization_url}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Invalid token or error occurred: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def google_auth_callback(request):
    """Callback handler for the OAuth2 response."""
    # Get state from query params
    state = request.query_params.get('state', '')
    
    # Extract user_id from state
    if not state.startswith('user_id:'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = state.split('user_id:')[1]
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create flow instance with same parameters as in google_calendar_init
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    
    # Process the authorization response
    # Need to convert to standard HttpRequest build_absolute_uri
    authorization_response = request._request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    
    # Get credentials from flow
    credentials = flow.credentials
    
    # Store tokens in the database
    user.google_access_token = credentials.token
    user.refresh_token = credentials.refresh_token
    user.google_token_expiry = credentials.expiry.isoformat()
    user.save()

    serializer = UserSerializer(data=user)
    if serializer.is_valid():
        saved_user = serializer.save()
    
    # Return success response
    return Response({
        'success': True,
        'message': 'Google Calendar connected successfully'
    })


# def list_calendar_events(request):
#     """View to list Google Calendar events for the authenticated user."""
#     user = request.user
    
#     # Check if the user has connected their Google Calendar
#     if not user.google_access_token:
#         return redirect('google_calendar_init')
    
#     # Create credentials object
#     from google.oauth2.credentials import Credentials
    
#     credentials = Credentials(
#         token=user.google_access_token,
#         refresh_token=user.refresh_token,
#         token_uri="https://oauth2.googleapis.com/token",
#         client_id=settings.GOOGLE_CLIENT_ID,
#         client_secret=settings.GOOGLE_CLIENT_SECRET,
#         scopes=SCOPES
#     )
    
#     # Check if token is expired and needs refreshing
#     expiry = datetime.datetime.fromisoformat(user.google_token_expiry)
#     if expiry <= datetime.datetime.utcnow():
#         # Token expired, refresh it
#         from google.auth.transport.requests import Request
#         credentials.refresh(Request())
        
#         # Update the stored tokens
#         user.google_access_token = credentials.token
#         user.google_token_expiry = credentials.expiry.isoformat()
#         user.save()
    
#     # Build the Calendar service
#     service = build('calendar', 'v3', credentials=credentials)
    
#     # Get calendar events
#     events_result = service.events().list(
#         calendarId='primary',
#         timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
#         maxResults=10,
#         singleEvents=True,
#         orderBy='startTime'
#     ).execute()
    
#     events = events_result.get('items', [])
    
#     return render(request, 'calendar_events.html', {
#         'events': events
#     })