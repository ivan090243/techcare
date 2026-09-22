from django.contrib import admin

from .models import FAQ, GalleryItem, Testimonial


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "is_featured", "is_published", "sort_order")
    list_filter = ("is_featured", "is_published")
    search_fields = ("title", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "is_featured", "is_published")
    list_filter = ("rating", "is_featured", "is_published")
    search_fields = ("customer_name", "text")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "sort_order")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")
