
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import HeaderSerializer
from .models import Header
from bson import ObjectId
from core.pagination import PaginationWithParams

# Create a new header
# POST /api/headers/create
@api_view(['POST'])
@csrf_exempt
def header_create(request):
    serializer = HeaderSerializer(data=request.data)
    if serializer.is_valid():

        header = serializer.save()

        return Response({"message": "Header created", "Header_id": str(header.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Find all headers
# GET /api/header
@api_view(['GET'])
@csrf_exempt
def header_find_all(request):
    paginator = PaginationWithParams()
    headers = Header.objects.all()
    paginated_headers = paginator.paginate_queryset(headers, request)
    serializer = HeaderSerializer(paginated_headers, many=True)
    return paginator.get_paginated_response(serializer.data)

# Find a header by ID
# GET /api/headers/:header_id
@api_view(['GET'])
@csrf_exempt
def header_find_by_id(header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))
        serializer = HeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Header.DoesNotExist:
        return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

# Update a header by ID
# POST /api/headers/:header_id/update
@api_view(['POST'])
@csrf_exempt
def header_update_by_id(request, header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))
        serializer = HeaderSerializer(header, data=request.data, partial=True)
        if serializer.is_valid():
            header = serializer.save()
            return Response({"message": "header updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Header.DoesNotExist:
        return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete a header by ID
# POST /api/headers/:header_id/delete
@api_view(['GET'])
@csrf_exempt
def header_delete_by_id(header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))
        header.delete()
        return Response({"message": "header deleted successfully"}, status=status.HTTP_200_OK)
    except Header.DoesNotExist:
        return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

