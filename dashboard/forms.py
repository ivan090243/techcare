from django import forms

from bookings.models import Booking, BookingStatus
from services.models import Service


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status", "admin_notes"]
        widgets = {
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "category",
            "short_description",
            "description",
            "icon",
            "price",
            "duration_minutes",
            "is_active",
            "sort_order",
            "requires_customer_parts",
            "note",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "note": forms.TextInput(),
        }
