from django.db.models import Q
from django.views.generic import ListView

from .models import FAQ, FAQCategory, GalleryItem, Testimonial


class GalleryListView(ListView):
    model = GalleryItem
    template_name = "content/gallery.html"
    context_object_name = "items"
    paginate_by = 9

    def get_queryset(self):
        qs = GalleryItem.objects.filter(is_published=True).select_related("service")
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(service__name__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class TestimonialListView(ListView):
    model = Testimonial
    template_name = "content/testimonials.html"
    context_object_name = "testimonials"

    def get_queryset(self):
        return Testimonial.objects.filter(is_published=True).select_related("service")


class FAQListView(ListView):
    model = FAQ
    template_name = "content/faq.html"
    context_object_name = "faqs"

    def get_queryset(self):
        qs = FAQ.objects.filter(is_active=True)
        search = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()

        if search:
            qs = qs.filter(
                Q(question__icontains=search) | Q(answer__icontains=search)
            )
        if category and category in FAQCategory.values:
            qs = qs.filter(category=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = FAQCategory.choices
        context["current_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context
