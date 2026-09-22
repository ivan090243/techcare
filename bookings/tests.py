from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings

from bookings.models import Booking, Customer
from services.models import DeliveryType, Service


class BookingEmailRegressionTests(TestCase):
    @override_settings(DEBUG=True, ALLOWED_HOSTS=["localhost", "testserver"])
    @patch("bookings.emails.send_mail", side_effect=OSError(22, "Invalid argument"))
    def test_booking_post_does_not_crash_when_console_email_fails(self, mock_send_mail):
        service = Service.objects.create(
            name="Laptop Cleaning",
            slug="laptop-cleaning",
            short_description="Laptop cleaning and tune-up",
            description="Laptop cleanup and maintenance service.",
            delivery_type=DeliveryType.HOME_SERVICE,
            is_active=True,
        )

        response = self.client.post(
            "/book/?service=laptop-cleaning",
            {
                "service": service.pk,
                "preferred_date": (date.today() + timedelta(days=1)).isoformat(),
                "preferred_time": "10:00",
                "service_address": "Test address",
                "device_info": "Test device",
                "notes": "Regression check",
                "name": "Regression User",
                "email": "regression@example.com",
                "phone": "09171234567",
            },
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/book/success/", response["Location"])
        self.assertTrue(Booking.objects.filter(customer__email="regression@example.com").exists())
        self.assertTrue(mock_send_mail.called)

        Booking.objects.filter(customer__email="regression@example.com").delete()
        Customer.objects.filter(email="regression@example.com").delete()
