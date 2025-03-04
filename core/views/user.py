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

#for search 
@api_view(['GET'])
@csrf_exempt
def user_find_all(request):
    # Get query parameters
    search = request.GET.get("q", "").strip()
    style = request.GET.get('style', "").strip()
    min_price = request.GET.get("minPrice", "").strip()
    max_price = request.GET.get("maxPrice", "").strip()
    availability = request.GET.get("availability", "").strip()
    experienceLevel = request.GET.get("experienceLevel", "").strip()

    # Build MongoEngine query filters
    filters = {}

    # Apply filters only if there are query parameters
    if search or style or min_price or max_price or availability or experienceLevel:
        
        # Search filter (by name and tags)
        if search:
            filters["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},  
                {"tags": {"$regex": search, "$options": "i"}},  
                {"location": {"$regex": search, "$options": "i"}},
            ]

         # Filter by style (e.g., "Wedding", "Portrait")
        if style:
            filters["tags"] = {"$regex": style, "$options": "i"}

        # Filter by price range
        if min_price and max_price:
            filters["price"] = {"$gte": int(min_price), "$lte": int(max_price)}
        elif min_price:
                    #database name
            filters["min_price"] = {"$gte": int(min_price)}
        elif max_price:
            filters["max_price"] = {"$lte": int(max_price)}


        # Filter by availability (Assuming availability is stored as a date string in the database)
        if availability:
            filters["availability"] = availability  # Adjust if needed for date format

        # Filter by experience level (e.g., "Beginner", "Intermediate", "Expert")
        if experienceLevel:
            filters["experience_level"] = {"$regex": experienceLevel, "$options": "i"}    


    # Fetch users using mongoengine ORM
    if filters:
        users_queryset = User.objects(__raw__=filters)  # Use __raw__ to apply direct MongoDB query
    else:
        users_queryset = User.objects.all()  # Fetch all data if no filters are applied

    # Convert users to JSON (without pagination metadata)
    users_json = [user.to_mongo().to_dict() for user in users_queryset]

    # Return only the list of users
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

