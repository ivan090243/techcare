from django.contrib import admin

from .models import Booking, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "customer",
        "service",
        "status",
        "preferred_date",
        "created_at",
    )
    list_filter = ("status", "preferred_date", "service")
    search_fields = ("reference", "customer__name", "customer__email")
    readonly_fields = ("reference", "created_at", "updated_at")
    date_hierarchy = "preferred_date"
