
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Field
from .forms import FieldForm


# Only superusers can access Field Management
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


# Field List
class FieldListView(AdminRequiredMixin, ListView):
    model = Field
    template_name = 'fields/field_list.html'
    context_object_name = 'fields'
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('q', '').strip()
        soil_type = self.request.GET.get('soil_type', '')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search)
            )

        if soil_type:
            queryset = queryset.filter(soil_type=soil_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('q', '')
        context['selected_soil_type'] = self.request.GET.get(
            'soil_type', ''
        )
        context['soil_types'] = Field.SOIL_TYPES

        return context


# Create Field
class FieldCreateView(AdminRequiredMixin, CreateView):
    model = Field
    form_class = FieldForm
    template_name = 'fields/field_form.html'
    success_url = reverse_lazy('fields:list')

    def form_valid(self, form):
        messages.success(self.request, 'Field created successfully!')
        return super().form_valid(form)


# Field Details
class FieldDetailView(AdminRequiredMixin, DetailView):
    model = Field
    template_name = 'fields/field_detail.html'
    context_object_name = 'field'


# Update Field
class FieldUpdateView(AdminRequiredMixin, UpdateView):
    model = Field
    form_class = FieldForm
    template_name = 'fields/field_form.html'
    success_url = reverse_lazy('fields:list')

    def form_valid(self, form):
        messages.success(self.request, 'Field updated successfully!')
        return super().form_valid(form)


# Delete Field
class FieldDeleteView(AdminRequiredMixin, DeleteView):
    model = Field
    template_name = 'fields/field_confirm_delete.html'
    success_url = reverse_lazy('fields:list')

    def form_valid(self, form):
        if self.object.crops.exists():
            messages.error(
                self.request,
                'This field cannot be deleted because crops are assigned to it.'
            )
            return redirect('fields:detail', pk=self.object.pk)

        messages.success(self.request, 'Field deleted successfully!')
        return super().form_valid(form)
