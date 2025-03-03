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
            products = list(USER_COLLECTION.find({}, {"_id": 0, "name": 1, "price": 1,"description":1, "tags": 1, "location": 1, "reviews": 1, "rating": 1, "images": 1}))
            print(f"Returning {len(products)} users")  # Debugging print
            return Response(products, status=200)

        # Search query (case-insensitive match for name, tags, location)
        filter_query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},  
                {"tags": {"$regex": search_term, "$options": "i"}},  
                {"location": {"$regex": search_term, "$options": "i"}}  
            ]
        }

        products = list(USER_COLLECTION.find(filter_query, {"_id": 0, "name": 1, "price": 1,"description":1, "tags": 1, "location": 1, "reviews": 1, "rating": 1, "images": 1}))
        
        return Response(products, status=200)
    except Exception as e:
        print("Error:", e)
        return Response({"error": "Internal Server Error"}, status=500)
    