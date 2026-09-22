from django.core.management.base import BaseCommand

from content.models import FAQ, FAQCategory, Testimonial
from services.models import Service, ServiceCategory


SERVICES = [
    {
        "name": "Laptop Cleaning",
        "slug": "laptop-cleaning",
        "category": ServiceCategory.CLEANING,
        "icon": "bi-laptop",
        "short_description": "Deep internal and external cleaning for laptops.",
        "description": (
            "Professional laptop cleaning including keyboard, vents, fan, "
            "and screen. Improves cooling performance and extends device life."
        ),
        "sort_order": 1,
    },
    {
        "name": "Desktop Cleaning",
        "slug": "desktop-cleaning",
        "category": ServiceCategory.CLEANING,
        "icon": "bi-pc-display",
        "short_description": "Full desktop PC dust removal and maintenance.",
        "description": (
            "Complete desktop cleaning with compressed air, thermal inspection, "
            "and cable management for optimal airflow."
        ),
        "sort_order": 2,
    },
    {
        "name": "Thermal Paste Replacement",
        "slug": "thermal-paste-replacement",
        "category": ServiceCategory.CLEANING,
        "icon": "bi-thermometer-half",
        "short_description": "Replace dried thermal paste for better cooling.",
        "description": (
            "Remove old thermal compound and apply premium paste to CPU/GPU "
            "for lower temperatures and quieter fans."
        ),
        "sort_order": 3,
    },
    {
        "name": "RAM Upgrade",
        "slug": "ram-upgrade",
        "category": ServiceCategory.HARDWARE,
        "icon": "bi-memory",
        "short_description": "Install and test additional RAM modules.",
        "description": (
            "Compatibility check, installation, and stress testing of new RAM "
            "for smoother multitasking."
        ),
        "sort_order": 4,
    },
    {
        "name": "SSD Installation",
        "slug": "ssd-installation",
        "category": ServiceCategory.HARDWARE,
        "icon": "bi-hdd",
        "short_description": "Install SSD and migrate your operating system.",
        "description": (
            "SSD installation with cloning or fresh OS setup for dramatically "
            "faster boot and load times."
        ),
        "sort_order": 5,
    },
    {
        "name": "Windows Installation",
        "slug": "windows-installation",
        "category": ServiceCategory.SOFTWARE,
        "icon": "bi-windows",
        "short_description": "Clean Windows install with drivers and updates.",
        "description": (
            "Fresh Windows installation, driver setup, and essential updates. "
            "Customer must provide a valid Windows license."
        ),
        "requires_customer_parts": True,
        "note": "Valid Windows license required",
        "sort_order": 6,
    },
    {
        "name": "Software Installation",
        "slug": "software-installation",
        "category": ServiceCategory.SOFTWARE,
        "icon": "bi-download",
        "short_description": "Install and configure essential software.",
        "description": (
            "Installation and basic configuration of productivity tools, "
            "browsers, and utilities you need."
        ),
        "sort_order": 7,
    },
    {
        "name": "Microsoft Office Installation",
        "slug": "microsoft-office-installation",
        "category": ServiceCategory.SOFTWARE,
        "icon": "bi-file-earmark-text",
        "short_description": "Install and activate Microsoft Office suite.",
        "description": (
            "Microsoft Office installation and activation. "
            "Customer must provide a valid license key."
        ),
        "requires_customer_parts": True,
        "note": "Valid Office license required",
        "sort_order": 8,
    },
    {
        "name": "Custom PC Assembly",
        "slug": "custom-pc-assembly",
        "category": ServiceCategory.CUSTOM,
        "icon": "bi-cpu",
        "short_description": "Professional assembly of your custom build.",
        "description": (
            "Expert PC assembly, cable management, BIOS setup, and stress testing. "
            "Customer provides all parts."
        ),
        "requires_customer_parts": True,
        "note": "Customer provides all parts",
        "sort_order": 9,
    },
    {
        "name": "Printer Installation & Configuration",
        "slug": "printer-installation",
        "category": ServiceCategory.SOFTWARE,
        "icon": "bi-printer",
        "short_description": "Set up printers on your home network.",
        "description": (
            "Driver installation, wireless setup, test prints, and sharing "
            "configuration for home or small office printers."
        ),
        "sort_order": 10,
    },
]

FAQS = [
    {
        "question": "Do I need to create an account to book?",
        "answer": (
            "No account is required. Simply fill out the booking form with your "
            "contact details and preferred appointment time."
        ),
        "category": FAQCategory.BOOKING,
        "sort_order": 1,
    },
    {
        "question": "What areas do you serve?",
        "answer": (
            "We currently offer home service within Metro Manila and nearby areas. "
            "Contact us to confirm availability for your location."
        ),
        "category": FAQCategory.GENERAL,
        "sort_order": 2,
    },
    {
        "question": "How long does a typical service take?",
        "answer": (
            "Most services take 1–2 hours. Complex jobs like custom PC assembly "
            "or full OS migration may take longer."
        ),
        "category": FAQCategory.SERVICES,
        "sort_order": 3,
    },
    {
        "question": "When will pricing be available?",
        "answer": (
            "Pricing is being finalized and will be posted on our Pricing page soon. "
            "You can book now and we'll confirm the rate when we contact you."
        ),
        "category": FAQCategory.PRICING,
        "sort_order": 4,
    },
    {
        "question": "What should I prepare before your visit?",
        "answer": (
            "Ensure your device is accessible, have power outlets available, and "
            "provide any licenses or parts required for your chosen service."
        ),
        "category": FAQCategory.BOOKING,
        "sort_order": 5,
    },
]

TESTIMONIALS = [
    {
        "customer_name": "Maria Santos",
        "location": "Quezon City",
        "rating": 5,
        "text": (
            "My laptop was overheating badly. After the cleaning and thermal paste "
            "replacement, it's running cool and quiet again. Highly recommend!"
        ),
        "is_featured": True,
    },
    {
        "customer_name": "James Rivera",
        "location": "Makati",
        "rating": 5,
        "text": (
            "Booked an SSD installation at home. Professional, on time, and my PC "
            "boots in seconds now. Great service!"
        ),
        "is_featured": True,
    },
    {
        "customer_name": "Anna Cruz",
        "location": "Pasig",
        "rating": 5,
        "text": (
            "They assembled my custom gaming PC perfectly. Clean cable management "
            "and everything tested before leaving. Will book again."
        ),
        "is_featured": False,
    },
]


class Command(BaseCommand):
    help = "Seed initial services, FAQs, and testimonials"

    def handle(self, *args, **options):
        for data in SERVICES:
            Service.objects.update_or_create(slug=data["slug"], defaults=data)

        for data in FAQS:
            FAQ.objects.update_or_create(question=data["question"], defaults=data)

        for data in TESTIMONIALS:
            Testimonial.objects.update_or_create(
                customer_name=data["customer_name"],
                defaults=data,
            )

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))
