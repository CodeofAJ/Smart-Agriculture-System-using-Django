from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import FarmActivity
from .forms import FarmActivityForm


# --------------------------------------------------
# Admin-only access
# --------------------------------------------------

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


# --------------------------------------------------
# Activity List View
# --------------------------------------------------

class FarmActivityListView(AdminRequiredMixin, ListView):
    model = FarmActivity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 10

    def get_queryset(self):
        queryset = FarmActivity.objects.select_related(
            'crop',
            'crop__category',
            'crop__field',
        ).order_by('-activity_date', '-created_at')

        # Search by crop name or description
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(crop__name__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        # Filter by activity type
        activity_type = self.request.GET.get('activity_type', '')

        if activity_type:
            queryset = queryset.filter(
                activity_type=activity_type
            )

        # Filter by crop
        crop_id = self.request.GET.get('crop', '')

        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get(
            'search', ''
        )
        context['selected_activity_type'] = self.request.GET.get(
            'activity_type', ''
        )
        context['selected_crop'] = self.request.GET.get(
            'crop', ''
        )

        context['activity_types'] = FarmActivity.ACTIVITY_TYPES

        # Crop options for the filter
        from crops.models import Crop
        context['crops'] = Crop.objects.all().order_by('name')

        # Total cost of all activities matching current filters
        context['total_cost'] = self.get_queryset().aggregate(
            total=Sum('cost')
        )['total'] or 0

        return context


# --------------------------------------------------
# Activity Create View
# --------------------------------------------------

class FarmActivityCreateView(AdminRequiredMixin, CreateView):
    model = FarmActivity
    form_class = FarmActivityForm
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Farm activity created successfully!'
        )
        return super().form_valid(form)


# --------------------------------------------------
# Activity Detail View
# --------------------------------------------------

class FarmActivityDetailView(AdminRequiredMixin, DetailView):
    model = FarmActivity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'


# --------------------------------------------------
# Activity Update View
# --------------------------------------------------

class FarmActivityUpdateView(AdminRequiredMixin, UpdateView):
    model = FarmActivity
    form_class = FarmActivityForm
    template_name = 'activities/activity_form.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activities:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Farm activity updated successfully!'
        )
        return super().form_valid(form)


# --------------------------------------------------
# Activity Delete View
# --------------------------------------------------

class FarmActivityDeleteView(AdminRequiredMixin, DeleteView):
    model = FarmActivity
    template_name = 'activities/activity_confirm_delete.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activities:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Farm activity deleted successfully!'
        )
        return super().form_valid(form)

# Create your views here.
