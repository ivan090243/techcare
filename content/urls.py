from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("gallery/", views.GalleryListView.as_view(), name="gallery"),
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonials"),
    path("testimonials/add/", views.TestimonialCreateView.as_view(), name="testimonial_add"),
    path("faq/", views.FAQListView.as_view(), name="faq"),
]
