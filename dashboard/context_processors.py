from content.models import Testimonial


def dashboard_notifications(request):
    pending_testimonials = Testimonial.objects.none()
    if request.user.is_authenticated and getattr(request.user, "is_staff", False):
        pending_testimonials = Testimonial.objects.filter(is_published=False).order_by("-created_at")

    return {
        "pending_testimonials": pending_testimonials.count(),
        "pending_testimonial_items": pending_testimonials[:5],
    }
