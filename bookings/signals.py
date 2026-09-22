from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_booking_notification
from .models import Booking


@receiver(post_save, sender=Booking)
def notify_admin_on_booking(sender, instance, created, **kwargs):
    if created:
        send_booking_notification(instance)
