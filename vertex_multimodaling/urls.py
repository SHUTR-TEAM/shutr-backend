from django.urls import path
from .utils import store_photo_embedding  # example
from .search import search_similar_photos  # example

urlpatterns = [
    path('test/store_photo_embedding/', store_photo_embedding, name='test_store_photo_embedding'),
    path('test/search_similar_photos/', search_similar_photos, name='test_search_similar_photos'),
]
