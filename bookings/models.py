from django.db import models

from core.models import TimeStampedModel
from services.models import DeliveryType, Service


class BookingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Customer(TimeStampedModel):
    """Guest customer record derived from bookings (no login)."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.name


class Booking(TimeStampedModel):
    reference = models.CharField(max_length=12, unique=True, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=DeliveryType.choices,
        default=DeliveryType.HOME_SERVICE,
    )
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    service_address = models.TextField()
    device_info = models.CharField(
        max_length=255,
        blank=True,
        help_text="Device model, specs, or notes about the equipment",
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["preferred_date"]),
            models.Index(fields=["reference"]),
        ]

    def __str__(self):
        return f"{self.reference} — {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_reference():
        import secrets
        import string

        alphabet = string.ascii_uppercase + string.digits
        return "TC" + "".join(secrets.choice(alphabet) for _ in range(8))
