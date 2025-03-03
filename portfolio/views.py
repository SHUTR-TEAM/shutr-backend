
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import HeaderSerializer, GallerySerializer, ReviewSerializer
from .models import Header, Gallery, GalleryFormat, Review
from bson import ObjectId
from core.pagination import PaginationWithParams

import os
# from django.core.files.storage import default_storages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
# from .models import Header
# from .serializers import HeaderSerializer, GallerySerializer
import gridfs
from django.conf import settings
from pymongo import MongoClient

from rest_framework import viewsets
from .models import Package
from .serializers import PackageSerializer

client = MongoClient(settings.MONGO_URI)
db = client.get_database()
fs = gridfs.GridFS(db)




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
def header_find_by_id(request, header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))
        serializer = HeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Header.DoesNotExist:
        return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

# Update a header by ID
# POST /api/headers/:header_id/update
@api_view(['POST'])
# @csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def header_update_by_id(request, header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))

        # check if there are any text updates
        serializer = HeaderSerializer(header, data=request.data, partial=True)
        if serializer.is_valid():
            header = serializer.save()

        #Handle image uploads
        # profile_image = request.FILES.get("profile_image")
        # background_image = request.FILES.get("background_image")

        #  Convert uploaded images to URLs 
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            profile_image_path = f"media/profile_images/{profile_image.name}"  # Storage path
            path = default_storage.save(profile_image_path, ContentFile(profile_image.read()))  
            # header.profile_image_url = f"/{path}"  # Convert file path to URL
            header.profile_image_url = request.build_absolute_uri(f"/media/{path}")


        if 'Background_image' in request.FILES:
            Background_image = request.FILES['Background_image']
            Background_image_path = f"media/Background_images/{Background_image.name}"
            path = default_storage.save(Background_image_path, ContentFile(Background_image.read()))
            # header.Background_image_url = f"/{path}"
            header.Background_image_url = request.build_absolute_uri(f"/media/{path}")

        # if profile_image:
        #     profile_id = fs.put(profile_image, filename=profile_image.name)
        #     profile_url = f"/api/get_image/{profile_id}"
        #     header.profile_image_url = profile_url

        # if background_image:
        #     background_id = fs.put(background_image, filename=background_image.name)
        #     background_url = f"/api/get_image/{background_id}"
        #     header.background_image_url = background_url

        header.save()
           
        return Response({
            "message": "Header updated successfully",
            "profile_image_url": header.profile_image_url,
            "Background_image_url": header.Background_image_url
            
        }, status=status.HTTP_200_OK)
    

        # return Response({"message": "header updated successfully"}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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









# Create a new gallery
# POST /api/galleries/create
@api_view(['POST'])
@csrf_exempt
def gallery_create(request):
    serializer = GallerySerializer(data=request.data)
    if serializer.is_valid():

        gallery = serializer.save()

        return Response({"message": "gallery created", "gallery_id": str(gallery.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Find all galleries
# GET /api/gallery
@api_view(['GET'])
@csrf_exempt
def gallery_find_all(request):
    paginator = PaginationWithParams()
    galleries = Gallery.objects.all()
    paginated_galleries = paginator.paginate_queryset(galleries, request)
    serializer = GallerySerializer(paginated_galleries, many=True)
    return paginator.get_paginated_response(serializer.data)



# Find a gallery by ID
# GET /api/galleries/:gallery_id
@api_view(['GET'])
@csrf_exempt
def gallery_find_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))
        serializer = GallerySerializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Gallery.DoesNotExist:
        return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)


# Update a gallery by ID
# POST /api/galleries/:gallery_id/update
# @api_view(['POST'])
# @csrf_exempt
# def gallery_update_by_id(request, gallery_id):
#     try:
#         gallery = Gallery.objects.get(id=ObjectId(gallery_id))
#         serializer = GallerySerializer(gallery, data=request.data, partial=True)
#         if serializer.is_valid():
#             gallery = serializer.save()
#             return Response({"message": "gallery updated successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Gallery.DoesNotExist:
#         return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
def gallery_update_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))

        # Extract images and categories from form-data
        images = request.FILES.getlist("Gallery")  # List of uploaded images
        categories = request.POST.getlist("category")  # Corresponding categories

        if not images or not categories:
            return Response({"error": "Missing images or categories"}, status=status.HTTP_400_BAD_REQUEST)

        new_gallery_items = []
        for img, category in zip(images, categories):
            # Save image to media storage
            # file_path = f"gallery/{gallery_id}/{img.name}"
            file_path = f"gallery/{img.name}"
            saved_path = default_storage.save(file_path, ContentFile(img.read()))
            image_url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)

            # Create new GalleryFormat entry
            new_gallery_items.append(GalleryFormat(url=image_url, category=category))

        # Append new images instead of replacing
        gallery.Gallery.extend(new_gallery_items)
        gallery.save()

        return Response({"message": "Gallery updated successfully", "Gallery": GallerySerializer(gallery).data}, status=status.HTTP_200_OK)

    except Gallery.DoesNotExist:
        return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)

    

# Delete a gallery by ID
# POST /api/galleries/:gallery_id/delete
@api_view(['GET'])
@csrf_exempt
def gallery_delete_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))
        gallery.delete()
        return Response({"message": "gallery deleted successfully"}, status=status.HTTP_200_OK)
    except Gallery.DoesNotExist:
        return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)    
    


# Create a new review
@api_view(['POST'])
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save()
        return Response({"message": "Review created", "review_id": str(review.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 







# Create a new review
# POST /api/reviews/create
@api_view(['POST'])
@csrf_exempt
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():

        review = serializer.save()

        return Response({"message": "review created", "review_id": str(review.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Find all reviews
# GET /api/review
@api_view(['GET'])
@csrf_exempt
def review_find_all(request):
    paginator = PaginationWithParams()
    reviews = Review.objects.all()
    paginated_reviews = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(paginated_reviews, many=True)
    return paginator.get_paginated_response(serializer.data)


# Find a review by ID
# GET /api/reviews/:review_id
@api_view(['GET'])
@csrf_exempt
def review_find_by_id(request, review_id):
    try:
        review = Review.objects.get(id=ObjectId(review_id))
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)


# Update a review by ID
# POST /api/reviews/:review_id/update
@api_view(['POST'])
@csrf_exempt
def review_update_by_id(request, review_id):
    try:
        review = Review.objects.get(id=ObjectId(review_id))
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            review = serializer.save()
            return Response({"message": "review updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)        


# Delete a review by ID
# POST /api/reviews/:review_id/delete
@api_view(['GET'])
@csrf_exempt
def review_delete_by_id(request, review_id):
    try:
        review = Review.objects.get(id=ObjectId(review_id))
        review.delete()
        return Response({"message": "review deleted successfully"}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)       


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer