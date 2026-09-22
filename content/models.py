from django.db import models

from core.models import TimeStampedModel
from services.models import Service


class GalleryItem(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    before_image = models.ImageField(upload_to="gallery/before/")
    after_image = models.ImageField(upload_to="gallery/after/")
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gallery_items",
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "gallery item"

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    customer_name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


class FAQCategory(models.TextChoices):
    GENERAL = "general", "General"
    BOOKING = "booking", "Booking"
    SERVICES = "services", "Services"
    PRICING = "pricing", "Pricing"


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=FAQCategory.choices,
        default=FAQCategory.GENERAL,
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "question"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
