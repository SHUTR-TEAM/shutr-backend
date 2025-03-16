import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserSerializer
from core.models.user import User
from bson import ObjectId
from core.pagination import PaginationWithParams
from django.db.models import Q

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
# @api_view(['GET'])
# @csrf_exempt
# def user_find_all(request):
#     paginator = PaginationWithParams()
#     users = User.objects.all()
#     paginated_users = paginator.paginate_queryset(users, request)
#     serializer = UserSerializer(paginated_users, many=True)
#     return paginator.get_paginated_response(serializer.data)


#function to handle search page
@api_view(['GET'])
@csrf_exempt
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
    if search or style or min_price or max_price or availability or experienceLevel:
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
                return JsonResponse([], safe=False)  
        else:
            # Return all users when no filters are applied
            users_queryset = User.objects.all() 

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    #convert the MongoDB query results into JSON format
    users_json = []
    for user in users_queryset.as_pymongo():
        users_json.append({
            "id": str(user["_id"]),  # Convert ObjectId to string
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
            "email": user.get("email", ""),
            "nic": user.get("nic", ""),
            "phone_num": user.get("phone_num", ""),
            "address": user.get("address", ""),
            "profile_image_url": user.get("profile_image_url", ""),
            "name": user.get("name", ""),
            "price": user.get("price", 0),
            "min_price": user.get("min_price", 0),
            "max_price": user.get("max_price", 0),
            "availability": user.get("availability", ""),
            "experience_level": user.get("experience_level", ""),
            "tags": user.get("tags", []),
            "location": user.get("location", ""),
            "reviews": user.get("reviews", 0),
            "rating": user.get("rating", 0.0),
            "images": user.get("images", []),
            "description": user.get("description", ""),
            "created_at": (
                datetime.datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                if isinstance(user.get("created_at", ""), str)
                else user.get("created_at", datetime.datetime.utcnow())
            ).isoformat(),
            "updated_at": (
                datetime.datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                if isinstance(user.get("updated_at", ""), str)
                else user.get("updated_at", datetime.datetime.utcnow())
            ).isoformat(),
        })

    return JsonResponse(users_json, safe=False)





# Find a user by ID
# GET /api/users/:user_id
@api_view(['GET'])
@csrf_exempt
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

