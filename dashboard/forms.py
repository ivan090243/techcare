from django import forms

from bookings.models import Booking, BookingStatus
from content.models import Testimonial
from services.models import Service


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            "customer_name",
            "location",
            "service",
            "rating",
            "text",
            "is_featured",
            "is_published",
        ]
        widgets = {
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.Select(attrs={"class": "form-select"}, choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)]),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


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
