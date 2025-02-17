# from django.contrib import admin
# from .models import Photographer

# @admin.register(Photographer)
# class PhotographerAdmin(admin.ModelAdmin):
#     list_display = ('email', 'name', 'username', 'id_number', 'bank_account')
#     search_fields = ('email', 'username', 'name')
#     list_filter = ('username',)

#     def get_queryset(self, request):
#         # Customize the queryset if needed
#         return super().get_queryset(request)

#     def save_model(self, request, obj, form, change):
#         # Custom save logic if needed
#         super().save_model(request, obj, form, change)

#     def delete_model(self, request, obj):
#         # Custom delete logic if needed
#         super().delete_model(request, obj)
