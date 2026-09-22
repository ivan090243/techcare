from django import forms

from services.models import Service

from .models import Testimonial


class TestimonialSubmissionForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["customer_name", "location", "service", "rating", "text"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.Select(
                attrs={"class": "form-select"},
                choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)],
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Share your experience with our service...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].required = False
        self.fields["service"].queryset = Service.objects.filter(is_active=True)
        self.fields["rating"].initial = 5
