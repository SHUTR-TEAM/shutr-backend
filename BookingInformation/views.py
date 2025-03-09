from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import BookingInformation  # Ensure correct model name

@csrf_exempt
def search_bookings(request):
    """
    API endpoint to search for bookings based on query (client name or category) and filter by status.
    """
    query = request.GET.get('query', '').strip()  # Get search term
    filter_option = request.GET.get('filter', 'latest').strip()  # Get filter, default: latest

    if not query:
        return JsonResponse({"error": "No search query provided"}, status=400)

    # 🔹 Base query: Search in client name or category using `icontains`
    bookings = BookingInformation.objects.filter(
        Q(client__icontains=query) | Q(category__icontains=query)
    )

    # 🔹 Apply filters for status
    valid_statuses = ["Confirmed", "Pending", "Cancelled"]
    if filter_option in valid_statuses:
        bookings = bookings.filter(status=filter_option)

    # 🔹 Convert queryset to JSON response
    results = list(bookings.values("id", "client", "category", "location", "time", "status"))

    return JsonResponse({"results": results}, safe=False)
