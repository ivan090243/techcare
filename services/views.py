from django.db.models import Q
from django.views.generic import ListView

from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        qs = Service.objects.filter(is_active=True)
        search = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(short_description__icontains=search)
                | Q(description__icontains=search)
            )
        if category and category in ServiceCategory.values:
            qs = qs.filter(category=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.choices
        context["current_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context
