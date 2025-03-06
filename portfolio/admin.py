# from django.contrib import admin

# Register your models here.
from django.contrib import admin
#from .models import Header, GalleryFormat, Gallery, ReviewFormat, Review, Package
from .models import Package
# @admin.register(Header)
# class HeaderAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at', 'updated_at')

# @admin.register(GalleryFormat)
# class GalleryFormatAdmin(admin.ModelAdmin):
#     list_display = ('url', 'category')

# @admin.register(Gallery)
# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ('id',)

# @admin.register(ReviewFormat)
# class ReviewFormatAdmin(admin.ModelAdmin):
#     list_display = ('name', 'rating', 'address')

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('id',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'package_type')