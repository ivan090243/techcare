from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_booking_notification(booking):
    context = {"booking": booking, "site_name": settings.SITE_NAME}
    subject = f"New Booking: {booking.reference} — {booking.service.name}"
    message = render_to_string("bookings/emails/new_booking.txt", context)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=settings.DEBUG,
    )
