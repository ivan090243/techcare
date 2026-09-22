from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.book_service_view, name="book"),
    path("success/<str:reference>/", views.booking_success_view, name="success"),
]
