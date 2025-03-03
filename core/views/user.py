from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserSerializer
from core.models.user import User
from bson import ObjectId
from core.pagination import PaginationWithParams

# Create a new user
# POST /api/users/create
@api_view(['POST'])
@csrf_exempt
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created", "user_id": str(user.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Find all users
# GET /api/users
@api_view(['GET'])
@csrf_exempt
def user_find_all(request):
    paginator = PaginationWithParams()
    users = User.objects.all()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

# Find a user by ID
# GET /api/users/:user_id
@api_view(['GET'])
@csrf_exempt
def user_find_by_id(request, user_id):
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
def user_delete_by_id(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

