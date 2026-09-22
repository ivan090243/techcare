from django.test import TestCase

from content.models import Testimonial


class TestimonialSubmissionTests(TestCase):
    def test_public_testimonial_submission_creates_unpublished_review(self):
        response = self.client.post(
            "/testimonials/add/",
            {
                "customer_name": "Jane Customer",
                "location": "Quezon City",
                "rating": 5,
                "text": "Very professional and fast service.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Testimonial.objects.filter(
                customer_name="Jane Customer",
                text="Very professional and fast service.",
                is_published=False,
            ).exists()
        )
