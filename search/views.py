from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

#Direct MongoDB Interaction
import pymongo


# Connect to MongoDB
MONGO_CLIENT = pymongo.MongoClient(settings.MONGO_URI) 
MONGO_DB = MONGO_CLIENT[settings.MONGO_DB_NAME]  
USER_COLLECTION = MONGO_DB["search"]  # Collection name

@api_view(['GET'])
def get_users(request):
    try:
        #
        search_term = request.GET.get("q", "").strip()  # Get search term from query params

         # If search term is empty, return all users
        if not search_term:
            portfolios = list(USER_COLLECTION.find({}, {"_id": 0, "name": 1, "price": 1,"description":1, "tags": 1, "location": 1, "reviews": 1, "rating": 1, "images": 1}))
            print(f"Returning {len(portfolios)} users")  # Debugging print
            return Response(portfolios, status=200)

        # Search query (case-insensitive match for name, tags, location)
        filter_query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},  
                {"tags": {"$regex": search_term, "$options": "i"}},  
                {"location": {"$regex": search_term, "$options": "i"}}  
            ]
        }

        portfolios = list(USER_COLLECTION.find(filter_query, {"_id": 0, "name": 1, "price": 1,"description":1, "tags": 1, "location": 1, "reviews": 1, "rating": 1, "images": 1}))
        
        return Response(portfolios, status=200)
    except Exception as e:
        print("Error:", e)
        return Response({"error": "Internal Server Error"}, status=500)

###############################
@api_view(['POST'])
def get_users_default(request):
    try:        

        portfolios = list(USER_COLLECTION.find({}, {"_id": 0, "name": 1, "description":1,"price": 1, "tags": 1, "location": 1, "reviews": 1, "rating": 1, "images": 1}))
        
        return Response(portfolios, status=200)
    
    except Exception as e:
        print("Error:-", e)
        return Response({"error": "Internal Server Error"}, status=500)
    

@api_view(['GET'])
def get_filtered_portfolios(request):
    try:
        # Get filter parameters from query params
        style = request.GET.get("style", "").strip()
        min_price = request.GET.get("minPrice", "").strip()
        max_price = request.GET.get("maxPrice", "").strip()
        availability = request.GET.get("availability", "").strip()
        experienceLevel = request.GET.get("experienceLevel", "").strip()

        # Create MongoDB filter query
        filter_query = {}

        # Filter by style (e.g., "Wedding", "Portrait")
        if style:
            filter_query["tags"] = {"$regex": style, "$options": "i"}

        # Filter by price range
        if min_price and max_price:
            filter_query["price"] = {"$gte": int(min_price), "$lte": int(max_price)}
        elif min_price:
            filter_query["minPrice"] = {"$gte": int(min_price)}
        elif max_price:
            filter_query["maxPrice"] = {"$lte": int(max_price)}

        # Filter by availability (Assuming availability is stored as a date string in the database)
        if availability:
            filter_query["availability"] = availability  # Adjust if needed for date format

        # Filter by experience level (e.g., "Beginner", "Intermediate", "Expert")
        if experienceLevel:
            filter_query["experienceLevel"] = {"$regex": experienceLevel, "$options": "i"}

        # Fetch filtered data
        portfolios = list(USER_COLLECTION.find(filter_query, {
            "_id": 0, "name": 1, "price": 1, "description": 1, "tags": 1, 
            "location": 1, "reviews": 1, "rating": 1, "images": 1
        }))

        return Response(portfolios, status=200)

    except Exception as e:
        print("Error:", e)
        return Response({"error": "Internal Server Error"}, status=500)   