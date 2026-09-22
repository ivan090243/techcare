from content.models import Testimonial
from django.db import DatabaseError


def dashboard_notifications(request):
    pending_testimonials = Testimonial.objects.none()
    if not request.user.is_authenticated or not getattr(request.user, "is_staff", False):
        return {
            "pending_testimonials": 0,
            "pending_testimonial_items": [],
        }

    try:
        pending_testimonials = Testimonial.objects.filter(is_published=False).order_by("-created_at")
        pending_count = pending_testimonials.count()
        pending_items = pending_testimonials[:5]
    except DatabaseError:
        pending_count = 0
        pending_items = []

    return {
        "pending_testimonials": pending_count,
        "pending_testimonial_items": pending_items,
    }
