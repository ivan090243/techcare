from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from services.models import Service

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_services"] = Service.objects.filter(is_active=True)[:6]
        return context


class PricingView(TemplateView):
    template_name = "core/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(is_active=True)
        return context


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            _notify_admin_contact(contact)
            messages.success(
                request,
                "Thank you! Your message has been sent. We'll get back to you soon.",
            )
            return redirect("core:contact")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})


def _notify_admin_contact(contact):
    send_mail(
        subject=f"[Contact] {contact.subject}",
        message=(
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Phone: {contact.phone or 'N/A'}\n\n"
            f"{contact.message}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )
