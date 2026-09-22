from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.DashboardHomeView.as_view(), name="home"),
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonials"),
    path("testimonials/create/", views.TestimonialCreateView.as_view(), name="testimonial_create"),
    path("testimonials/<int:pk>/edit/", views.TestimonialUpdateView.as_view(), name="testimonial_edit"),
    path("testimonials/<int:pk>/delete/", views.TestimonialDeleteView.as_view(), name="testimonial_delete"),
    path("testimonials/<int:pk>/approve/", views.TestimonialApprovalView.as_view(), name="testimonial_approve"),
    path("bookings/", views.BookingListView.as_view(), name="bookings"),
    path("bookings/export/", views.export_bookings_view, name="bookings_export"),
    path("bookings/<int:pk>/", views.BookingUpdateView.as_view(), name="booking_detail"),
    path("customers/", views.CustomerListView.as_view(), name="customers"),
    path("services/", views.ServiceListView.as_view(), name="services"),
    path("services/<int:pk>/edit/", views.ServiceUpdateView.as_view(), name="service_edit"),
    path("messages/<int:pk>/read/", views.mark_contact_read_view, name="message_read"),
]
