
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import HeaderSerializer, GallerySerializer, ReviewSerializer, PackageSerializer
from .models import Header, Gallery, Review, Package
from bson import ObjectId
from core.pagination import PaginationWithParams
from rest_framework import viewsets

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
@api_view(['POST'])
@csrf_exempt
def gallery_update_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))
        serializer = GallerySerializer(gallery, data=request.data, partial=True)
        if serializer.is_valid():
            gallery = serializer.save()
            return Response({"message": "gallery updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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




# @api_view(['GET'])
# def get_packages(request):
#     packages = Package.objects.all()
#     serializer = PackageSerializer(packages, many=True)
#     return Response(serializer.data)


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def create(self, request, *args, **kwargs):
        """Create a new package"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Get a single package by ID"""
        try:
            package = Package.objects.get(pk=pk)
            serializer = PackageSerializer(package)
            return Response(serializer.data)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update an existing package"""
        try:
            package = Package.objects.get(pk=pk)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PackageSerializer(package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a package"""
        try:
            package = Package.objects.get(pk=pk)
            package.delete()
            return Response({"message": "Package deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)