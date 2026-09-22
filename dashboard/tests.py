from django.contrib.auth import get_user_model
from django.test import TestCase

from content.models import Testimonial


class DashboardTestimonialApprovalTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="adminstaff",
            email="adminstaff@example.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_dashboard_shows_pending_testimonials_count(self):
        Testimonial.objects.create(
            customer_name="Pending Client",
            rating=5,
            text="Waiting for approval",
            is_published=False,
        )

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stats"]["pending_testimonials"], 1)

    def test_dashboard_can_approve_testimonial(self):
        testimonial = Testimonial.objects.create(
            customer_name="Approve Me",
            rating=4,
            text="Please approve",
            is_published=False,
        )

        response = self.client.post(f"/dashboard/testimonials/{testimonial.pk}/approve/")

        self.assertEqual(response.status_code, 302)
        testimonial.refresh_from_db()
        self.assertTrue(testimonial.is_published)

    def test_dashboard_can_delete_testimonial(self):
        testimonial = Testimonial.objects.create(
            customer_name="Delete Me",
            rating=3,
            text="Remove this review",
            is_published=False,
        )

        response = self.client.post(f"/dashboard/testimonials/{testimonial.pk}/delete/")

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Testimonial.objects.filter(pk=testimonial.pk).exists())
