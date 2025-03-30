import os
import uuid
import boto3
import gridfs

from bson import ObjectId
from pymongo import MongoClient

from django.conf import settings
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from core.models.user import User 
from core.pagination import PaginationWithParams
from .models import Header, Gallery, Package, Review, SocialLinks
from .serializers import HeaderSerializer, GallerySerializer, PackageSerializer, ReviewSerializer, SocialLinksSerializer


client = MongoClient(settings.MONGO_URI)
db = client.get_database()
fs = gridfs.GridFS(db)


# Create a new header
# POST /api/headers/create
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def header_update_by_id(request, header_id):
    try:
        header = Header.objects.get(id=ObjectId(header_id))

        # check if there are any text updates
        serializer = HeaderSerializer(header, data=request.data, partial=True)
        if serializer.is_valid():
            header = serializer.save()

        #  Convert uploaded images to URLs 
        if 'profile_image' in request.FILES:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION,
            )

            profile_image = request.FILES['profile_image']
            
            # Generate a unique file name using uuid
            file_extension = os.path.splitext(profile_image.name)[1]  # Extract file extension
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            
            profile_image_path = f"profile-images/{unique_filename}"  # Storage path

            s3.upload_fileobj(profile_image, settings.S3_BUCKET, profile_image_path)
            profile_image_url = f"{settings.S3_CUSTOM_DOMAIN}/{profile_image_path}"
            
            # Save the URL in the database
            header.profile_image_url = profile_image_url

        if 'Background_image' in request.FILES:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION,
            )

            Background_image = request.FILES['Background_image']
            
            # Generate a unique file name using uuid
            file_extension = os.path.splitext(Background_image.name)[1]  # Extract file extension
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            
            Background_image_path = f"background-images/{unique_filename}"  # Storage path in S3

            s3.upload_fileobj(Background_image, settings.S3_BUCKET, Background_image_path)
            
            # Generate S3 URL
            Background_image_url = f"{settings.S3_CUSTOM_DOMAIN}/{Background_image_path}"
            
            # Save the URL in the database
            header.Background_image_url = Background_image_url

        header.save()
           
        return Response({
            "message": "Header updated successfully",
            "profile_image_url": header.profile_image_url,
            "Background_image_url": header.Background_image_url
            
        }, status=status.HTTP_200_OK)
    
    except Header.DoesNotExist:
        return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)


# Delete a header by ID
# POST /api/headers/:header_id/delete
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def gallery_find_all(request):
    paginator = PaginationWithParams()
    galleries = Gallery.objects.all()
    paginated_galleries = paginator.paginate_queryset(galleries, request)
    serializer = GallerySerializer(paginated_galleries, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def gallery_create(request):
    try:
        images = request.FILES.getlist("image")
        # category = request.POST.get("category")
        categories = request.POST.getlist("category")
        photographer_id = request.POST.get("photographerID")
        portfolio_id = request.POST.get("portfolioID")

        if not images or not categories or not photographer_id:
            return Response({"error": "Missing data (images, categories, photographerID)"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate photographerID early
        if not ObjectId.is_valid(photographer_id):
            return Response({"error": "Invalid photographerID"}, status=status.HTTP_400_BAD_REQUEST)

        #  Validate number of images and categories match
        if len(images) != len(categories):
            return Response({"error": "Mismatch between number of images and categories"}, status=status.HTTP_400_BAD_REQUEST)

        
        for img, category in zip(images, categories):
            # 3. Save the file to media storage
            file_path = f"gallery/{img.name}"
            saved_path = default_storage.save(file_path, ContentFile(img.read()))

            # 4. Build the URL to access the uploaded file
            image_url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)

            # 5. Prepare data for the serializer
            data = {
                "photographerID": photographer_id,
                "url": image_url,  # Pass the path we generated
                "category": category,
                "portfolioID": portfolio_id
            }

            # 6. Validate and save the serializer
            serializer = GallerySerializer(data=data)
            if serializer.is_valid():
                gallery = serializer.save()
                # return Response({"message": "Gallery created successfully", "gallery_id": str(gallery.id)}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Gallery created successfully"}, status=status.HTTP_201_CREATED)        

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Find all photos(gallery) for a specific photographer
# GET /api/galleries/photographer/:photographer_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def gallery_find_by_photographer(request, portfolio_id):
    try:
        # portfolio = Header.objects.get(id=ObjectId(portfolio_id))
        images = Gallery.objects.filter(portfolioID=ObjectId(portfolio_id))
        
        serializer = GallerySerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Header.DoesNotExist:
        return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Find a gallery by ID
# GET /api/galleries/:gallery_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def gallery_find_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))
        serializer = GallerySerializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Gallery.DoesNotExist:
        return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)


# Delete a gallery by ID
# POST /api/galleries/:gallery_id/delete
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def gallery_delete_by_id(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=ObjectId(gallery_id))
        gallery.delete()
        return Response({"message": "gallery deleted successfully"}, status=status.HTTP_200_OK)
    except Gallery.DoesNotExist:
        return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND) 


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def gallery_delete_photo(request, participant_id):
    try:
        # Extract image URL from the request body
        image_url = request.data.get('image_url')

        if not image_url:
            return Response({"error": "No image URL provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter and delete the Gallery document with matching photographer and url
        deleted_count = Gallery.objects(photographer=ObjectId(participant_id), url=image_url).delete()

        if deleted_count == 0:
            return Response({"error": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Photo deleted successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create a new review
# POST /api/reviews/create
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def review_find_all(request):
    paginator = PaginationWithParams()
    reviews = Review.objects.all()
    paginated_reviews = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(paginated_reviews, many=True)
    return paginator.get_paginated_response(serializer.data)


# Find all reviews for a specific photographer
# GET /api/reviews/photographer/:photographer_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def review_find_by_photographer(request, photographer_id):
    try:
        photographer = User.objects.get(id=ObjectId(photographer_id))
        reviews = Review.objects.filter(photographer=photographer)
        
        if not reviews:
            return Response({"message": "No reviews found for this photographer"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Find a review by ID
# GET /api/reviews/:review_id
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def review_delete_by_id(request, review_id):
    try:
        review = Review.objects.get(id=ObjectId(review_id))
        review.delete()
        return Response({"message": "review deleted successfully"}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)       


# Create a new packages
# POST /api/packages/create
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def package_create(request):
    serializer = PackageSerializer(data=request.data)
    if serializer.is_valid():
        package = serializer.save()

        return Response({"message": "package created", "package_id": str(package.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Find all packages
# GET /api/packages
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def package_find_all(request):
    paginator = PaginationWithParams()
    packages = Review.objects.all()
    paginated_reviews = paginator.paginate_queryset(packages, request)
    serializer = PackageSerializer(paginated_reviews, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def package_find_by_id(request, package_id):
    try:
        package = Package.objects.filter(id=ObjectId(package_id)).first()
        if not package:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def package_find_by_photographerid(request, photographer_id):
    try:
        photographer = User.objects.get(id=ObjectId(photographer_id))
        packages = Package.objects.filter(photographer=photographer)

        if not packages:
            return Response({"message": "No packages found for this photographer"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def package_find_by_portfolioid(request, portfolio_id):
    try:
        # Validate portfolio ID
        if not ObjectId.is_valid(portfolio_id):
            return Response({"error": "Invalid portfolio ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the portfolio
        portfolio = Header.objects.filter(id=ObjectId(portfolio_id)).first()
        if not portfolio:
            return Response({"message": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get packages linked to the portfolio
        packages = Package.objects.filter(portfolio=portfolio)
        if not packages:
            return Response({"message": "No packages found for this portfolio"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return data
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def package_update(request, package_id):
    try:
        # Fetch the package by ID
        package = Package.objects.filter(id=ObjectId(package_id)).first()
        if not package:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate request data
        serializer = PackageSerializer(package, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Update a package by ID
# POST /api/packages/:package_id/update
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def package_update_by_id(request, package_id):
    try:
        package = Package.objects.get(id=ObjectId(package_id))
        serializer = PackageSerializer(package, data=request.data, partial=True)
        if serializer.is_valid():
            package = serializer.save()
            return Response({"message": "package updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Package.DoesNotExist:
        return Response({"error": "package not found"}, status=status.HTTP_404_NOT_FOUND)        


# Delete a package by ID
# POST /api/packages/:package_id/delete
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def package_delete_by_id(request, package_id):
    try:
        package = Package.objects.get(id=ObjectId(package_id))
        package.delete()
        return Response({"message": "package deleted successfully"}, status=status.HTTP_200_OK)
    except Package.DoesNotExist:
        return Response({"error": "package not found"}, status=status.HTTP_404_NOT_FOUND) 


# Create a new social link entry
# POST /api/SocialLinks/create
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def social_links_create(request):
    serializer = SocialLinksSerializer(data=request.data)
    
    if serializer.is_valid():
        social_links = serializer.save()
        return Response({"message": "Social links created", "social_links_id": str(social_links.id)},status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def social_links_find_by_photographer(request, portfolio_id):
    """Retrieve social links for a specific photographer."""
    try:
        # Validate if photographer_id is a valid ObjectId
        if not ObjectId.is_valid(portfolio_id):
            return Response({"error": "Invalid photographer ID format"}, status=status.HTTP_400_BAD_REQUEST)
        
        portfolio = Header.objects.get(id=ObjectId(portfolio_id))  # Fetch photographer
        social_links = SocialLinks.objects.filter(portfolio=portfolio).first()  # Get social links for the user
        
        if not social_links:
            return Response({"message": "No social links found for this photographer"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SocialLinksSerializer(social_links)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Header.DoesNotExist:
        return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Update social links for a photographer
# POST /api/SocialLinks/update/<portfolio_id>/
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def social_links_update(request, portfolio_id):
    """Update social links for a specific photographer."""
    try:
        # Validate if photographer_id is a valid ObjectId
        if not ObjectId.is_valid(portfolio_id):
            return Response({"error": "Invalid portfolio_id ID format"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the photographer
        try:
            portfolio = Header.objects.get(id=ObjectId(portfolio_id))
        except Header.DoesNotExist:
            return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the existing social links or create new if not found
        social_links = SocialLinks.objects.filter(portfolio=portfolio).first()  # Use filter and get the first match    

        if not social_links:
            # If no existing social links, create a new entry
            social_links = SocialLinks.objects.create(
                portfolio=portfolio,
                facebook=request.data.get("facebook"),
                instagram=request.data.get("instagram"),
                twitter=request.data.get("twitter"),
                linkedin=request.data.get("linkedin")
            )
            print("sdf")
        else:
            print("awda")
            # Update existing social links
            social_links.facebook = request.data.get("facebook")
            social_links.instagram = request.data.get("instagram")
            social_links.twitter = request.data.get("twitter")
            social_links.linkedin = request.data.get("linkedin")
            social_links.save()  # Save the updated instance

        # Serialize and return response
        serializer = SocialLinksSerializer(social_links)
        return Response({"message": "Social links updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DELETE /api/SocialLinks/delete/<photographer_id>/
@api_view(['DELETE'])
@csrf_exempt
@permission_classes([AllowAny])
def social_links_delete(request, photographer_id):
    """Delete social links for a specific photographer."""
    try:
        # Validate if photographer_id is a valid ObjectId
        if not ObjectId.is_valid(photographer_id):
            return Response({"error": "Invalid photographer ID format"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the photographer
        try:
            photographer = User.objects.get(id=ObjectId(photographer_id))
        except User.DoesNotExist:
            return Response({"error": "Photographer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Find social links for the photographer
        social_links = SocialLinks.objects.filter(user=photographer).first()

        if not social_links:
            return Response({"error": "No social links found for this photographer"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the social links entry
        social_links.delete()
        return Response({"message": "Social links deleted successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)