from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import BookingForm
from .models import Customer


def book_service_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = _create_booking(form)
            messages.success(
                request,
                f"Booking confirmed! Your reference number is {booking.reference}. "
                "We'll contact you shortly to confirm your appointment.",
            )
            return redirect("bookings:success", reference=booking.reference)
    else:
        service_slug = request.GET.get("service")
        initial = {}
        if service_slug:
            from services.models import Service

            try:
                initial["service"] = Service.objects.get(
                    slug=service_slug, is_active=True
                )
            except Service.DoesNotExist:
                pass
        form = BookingForm(initial=initial)

    return render(request, "bookings/book.html", {"form": form})


def booking_success_view(request, reference):
    from .models import Booking

    try:
        booking = Booking.objects.select_related("service", "customer").get(
            reference=reference
        )
    except Booking.DoesNotExist:
        return redirect("bookings:book")

    return render(request, "bookings/success.html", {"booking": booking})


@transaction.atomic
def _create_booking(form):
    from services.models import DeliveryType

    from .models import Booking, Customer

    data = form.cleaned_data
    customer, _ = Customer.objects.get_or_create(
        email=data["email"].lower(),
        defaults={
            "name": data["name"],
            "phone": data["phone"],
            "address": data["service_address"],
        },
    )
    if customer.name != data["name"] or customer.phone != data["phone"]:
        customer.name = data["name"]
        customer.phone = data["phone"]
        customer.address = data["service_address"]
        customer.save(update_fields=["name", "phone", "address", "updated_at"])

    return Booking.objects.create(
        customer=customer,
        service=data["service"],
        delivery_type=DeliveryType.HOME_SERVICE,
        preferred_date=data["preferred_date"],
        preferred_time=data["preferred_time"],
        service_address=data["service_address"],
        device_info=data.get("device_info", ""),
        notes=data.get("notes", ""),
    )
