import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_booking_notification(booking):
    context = {"booking": booking, "site_name": settings.SITE_NAME}
    subject = f"New Booking: {booking.reference} — {booking.service.name}"
    message = render_to_string("bookings/emails/new_booking.txt", context)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=settings.DEBUG,
        )
    except OSError:
        logger.warning(
            "Booking notification email failed for reference %s. "
            "The booking was still created successfully.",
            booking.reference,
            exc_info=True,
        )
