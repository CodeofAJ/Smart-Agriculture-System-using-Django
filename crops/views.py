from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Crop, Category
from .forms import CropForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


class CropListView(AdminRequiredMixin, ListView):

    model = Crop
    template_name = 'crops/crop_list.html'
    context_object_name = 'crops'
    ordering = ['-planting_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '')
        status = self.request.GET.get('status', '')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(variety__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.select_related('category', 'field')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')

        return context


class CropCreateView(AdminRequiredMixin, CreateView):

    model = Crop
    form_class = CropForm
    template_name = 'crops/crop_form.html'
    success_url = reverse_lazy('crops:list')


class CropDetailView(AdminRequiredMixin, DetailView):

    model = Crop
    template_name = 'crops/crop_detail.html'
    context_object_name = 'crop'


class CropUpdateView(AdminRequiredMixin, UpdateView):

    model = Crop
    form_class = CropForm
    template_name = 'crops/crop_form.html'
    success_url = reverse_lazy('crops:list')


class CropDeleteView(AdminRequiredMixin, DeleteView):

    model = Crop
    template_name = 'crops/crop_confirm_delete.html'
    success_url = reverse_lazy('crops:list')