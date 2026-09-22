from datetime import date

from django import forms

from services.models import DeliveryType, Service

from .models import Booking


class BookingForm(forms.ModelForm):
    name = forms.CharField(max_length=120, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone = forms.CharField(max_length=20, label="Phone Number")

    class Meta:
        model = Booking
        fields = [
            "service",
            "preferred_date",
            "preferred_time",
            "service_address",
            "device_info",
            "notes",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
            "service_address": forms.Textarea(attrs={"rows": 3}),
            "device_info": forms.TextInput(
                attrs={"placeholder": "e.g. Dell Inspiron 15, Windows 11"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Special instructions (optional)"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(
            is_active=True,
            delivery_type=DeliveryType.HOME_SERVICE,
        )

    def clean_preferred_date(self):
        preferred = self.cleaned_data["preferred_date"]
        if preferred < date.today():
            raise forms.ValidationError("Please select a future date.")
        return preferred

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
