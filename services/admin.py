from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "sort_order")
    list_filter = ("category", "delivery_type", "is_active")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
