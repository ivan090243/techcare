from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@email.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+63 9XX XXX XXXX"}),
            "subject": forms.TextInput(attrs={"placeholder": "How can we help?"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Tell us more...", "rows": 5}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and len(phone) < 7:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
