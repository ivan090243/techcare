from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View

from bookings.models import Booking, BookingStatus, Customer
from content.models import Testimonial
from core.models import ContactMessage
from services.models import Service

from .forms import BookingStatusForm, ServiceForm
from .mixins import StaffRequiredMixin
from .utils import export_bookings_excel


class DashboardLoginView(auth_views.LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True


class DashboardHomeView(StaffRequiredMixin, ListView):
    template_name = "dashboard/home.html"
    context_object_name = "recent_bookings"
    paginate_by = 10

    def get_queryset(self):
        return (
            Booking.objects.select_related("customer", "service")
            .order_by("-created_at")[:10]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stats"] = {
            "total_bookings": Booking.objects.count(),
            "pending": Booking.objects.filter(status=BookingStatus.PENDING).count(),
            "confirmed": Booking.objects.filter(status=BookingStatus.CONFIRMED).count(),
            "completed": Booking.objects.filter(status=BookingStatus.COMPLETED).count(),
            "customers": Customer.objects.count(),
            "services": Service.objects.filter(is_active=True).count(),
            "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
            "pending_testimonials": Testimonial.objects.filter(is_published=False).count(),
        }
        return context


class TestimonialListView(StaffRequiredMixin, ListView):
    model = Testimonial
    template_name = "dashboard/testimonials/list.html"
    context_object_name = "testimonials"
    paginate_by = 20

    def get_queryset(self):
        return Testimonial.objects.select_related("service").order_by("-created_at")


class TestimonialDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully.")
        return redirect("dashboard:testimonials")


class TestimonialApprovalView(StaffRequiredMixin, View):
    def post(self, request, pk):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        testimonial.is_published = True
        testimonial.save(update_fields=["is_published", "updated_at"])
        messages.success(request, "Testimonial approved and published.")
        return redirect("dashboard:testimonials")


class BookingListView(StaffRequiredMixin, ListView):
    model = Booking
    template_name = "dashboard/bookings/list.html"
    context_object_name = "bookings"
    paginate_by = 20

    def get_queryset(self):
        qs = Booking.objects.select_related("customer", "service").order_by("-created_at")
        search = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        date_from = self.request.GET.get("date_from", "").strip()
        date_to = self.request.GET.get("date_to", "").strip()

        if search:
            qs = qs.filter(
                Q(reference__icontains=search)
                | Q(customer__name__icontains=search)
                | Q(customer__email__icontains=search)
                | Q(customer__phone__icontains=search)
                | Q(service__name__icontains=search)
            )
        if status and status in BookingStatus.values:
            qs = qs.filter(status=status)
        if date_from:
            qs = qs.filter(preferred_date__gte=date_from)
        if date_to:
            qs = qs.filter(preferred_date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = BookingStatus.choices
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "status": self.request.GET.get("status", ""),
            "date_from": self.request.GET.get("date_from", ""),
            "date_to": self.request.GET.get("date_to", ""),
        }
        return context


class BookingUpdateView(StaffRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingStatusForm
    template_name = "dashboard/bookings/detail.html"
    context_object_name = "booking"

    def get_queryset(self):
        return Booking.objects.select_related("customer", "service")

    def get_success_url(self):
        return reverse_lazy("dashboard:booking_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Booking updated successfully.")
        return super().form_valid(form)


class CustomerListView(StaffRequiredMixin, ListView):
    model = Customer
    template_name = "dashboard/customers/list.html"
    context_object_name = "customers"
    paginate_by = 20

    def get_queryset(self):
        qs = Customer.objects.annotate(
            booking_count=Count("bookings")
        ).order_by("-created_at")
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ServiceListView(StaffRequiredMixin, ListView):
    model = Service
    template_name = "dashboard/services/list.html"
    context_object_name = "services"
    paginate_by = 20

    def get_queryset(self):
        qs = Service.objects.annotate(booking_count=Count("bookings")).order_by(
            "sort_order", "name"
        )
        search = self.request.GET.get("q", "").strip()
        active = self.request.GET.get("active", "").strip()

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(short_description__icontains=search))
        if active == "1":
            qs = qs.filter(is_active=True)
        elif active == "0":
            qs = qs.filter(is_active=False)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "active": self.request.GET.get("active", ""),
        }
        return context


class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "dashboard/services/form.html"
    success_url = reverse_lazy("dashboard:services")

    def form_valid(self, form):
        messages.success(self.request, "Service updated successfully.")
        return super().form_valid(form)


@login_required
@user_passes_test(lambda u: u.is_staff)
def export_bookings_view(request):
    qs = Booking.objects.select_related("customer", "service").order_by("-created_at")

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    if search:
        qs = qs.filter(
            Q(reference__icontains=search)
            | Q(customer__name__icontains=search)
            | Q(customer__email__icontains=search)
        )
    if status and status in BookingStatus.values:
        qs = qs.filter(status=status)

    return export_bookings_excel(qs)


@login_required
@user_passes_test(lambda u: u.is_staff)
def mark_contact_read_view(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save(update_fields=["is_read", "updated_at"])
    messages.success(request, "Message marked as read.")
    return redirect("dashboard:home")
