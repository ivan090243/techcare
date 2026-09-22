from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class ServiceCategory(models.TextChoices):
    CLEANING = "cleaning", "Cleaning & Maintenance"
    HARDWARE = "hardware", "Hardware Upgrades"
    SOFTWARE = "software", "Software & OS"
    CUSTOM = "custom", "Custom Builds"


class DeliveryType(models.TextChoices):
    """Future-ready delivery channel."""

    HOME_SERVICE = "home_service", "Home Service"
    WALK_IN = "walk_in", "Walk-in"
    PICKUP_DELIVERY = "pickup_delivery", "Pick-up & Delivery"


class Service(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.CharField(
        max_length=20,
        choices=ServiceCategory.choices,
        default=ServiceCategory.CLEANING,
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=DeliveryType.choices,
        default=DeliveryType.HOME_SERVICE,
    )
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        default="bi-tools",
        help_text="Bootstrap Icons class, e.g. bi-laptop",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave blank for TBA pricing",
    )
    duration_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    requires_customer_parts = models.BooleanField(
        default=False,
        help_text="Customer must provide parts or license",
    )
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("services:list") + f"#{self.slug}"

    @property
    def price_display(self):
        if self.price is not None:
            return f"₱{self.price:,.2f}"
        return "TBA"
