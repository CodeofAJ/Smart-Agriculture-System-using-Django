from django.shortcuts import render


from django.contrib import messages
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

# from accounts.mixins import AdminRequiredMixin
from crops.views import AdminRequiredMixin
from .models import Harvest, Expense
from .forms import HarvestForm,ExpenseForm


class HarvestListView(AdminRequiredMixin, ListView):

    model = Harvest
    template_name = 'farm_records/harvest_list.html'
    context_object_name = 'harvests'
    paginate_by = 10

    def get_queryset(self):
        queryset = Harvest.objects.select_related(
            'crop',
            'crop__category',
            'crop__field',
        ).order_by('-harvest_date')

        search_query = self.request.GET.get('search', '').strip()
        quality = self.request.GET.get('quality', '')
        crop = self.request.GET.get('crop', '')

        if search_query:
            queryset = queryset.filter(
                Q(crop__name__icontains=search_query)
                | Q(notes__icontains=search_query)
            )

        if quality:
            queryset = queryset.filter(quality=quality)

        if crop:
            queryset = queryset.filter(crop_id=crop)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get(
            'search', ''
        )

        context['selected_quality'] = self.request.GET.get(
            'quality', ''
        )

        context['selected_crop'] = self.request.GET.get(
            'crop', ''
        )

        context['quality_choices'] = Harvest.QUALITY_CHOICES

        context['crops'] = (
            Harvest.objects
            .values('crop_id', 'crop__name')
            .distinct()
            .order_by('crop__name')
        )

        context['total_quantity'] = (
            self.object_list.aggregate(
                total=Sum('quantity')
            )['total'] or 0
        )

        context['total_records'] = self.object_list.count()

        return context


class HarvestCreateView(AdminRequiredMixin, CreateView):

    model = Harvest
    form_class = HarvestForm
    template_name = 'farm_records/harvest_form.html'
    success_url = reverse_lazy('farm_records:harvest_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Harvest record created successfully.'
        )
        return super().form_valid(form)


class HarvestDetailView(AdminRequiredMixin, DetailView):

    model = Harvest
    template_name = 'farm_records/harvest_detail.html'
    context_object_name = 'harvest'

    def get_queryset(self):
        return Harvest.objects.select_related(
            'crop',
            'crop__category',
            'crop__field',
        )


class HarvestUpdateView(AdminRequiredMixin, UpdateView):

    model = Harvest
    form_class = HarvestForm
    template_name = 'farm_records/harvest_form.html'
    context_object_name = 'harvest'

    def get_success_url(self):
        return reverse_lazy(
            'farm_records:harvest_detail',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            'Harvest record updated successfully.'
        )
        return super().form_valid(form)


class HarvestDeleteView(AdminRequiredMixin, DeleteView):

    model = Harvest
    template_name = 'farm_records/harvest_confirm_delete.html'
    context_object_name = 'harvest'
    success_url = reverse_lazy('farm_records:harvest_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Harvest record deleted successfully.'
        )
        return super().form_valid(form)




# ==========================================
# Expense Management
# ==========================================

class ExpenseListView(AdminRequiredMixin, ListView):

    model = Expense
    template_name = 'farm_records/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self):

        queryset = Expense.objects.select_related(
            'crop',
            'crop__category',
            'crop__field',
        ).order_by('-expense_date')

        search_query = self.request.GET.get(
            'search', ''
        ).strip()

        expense_type = self.request.GET.get(
            'expense_type', ''
        )

        crop = self.request.GET.get('crop', '')

        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query)
                | Q(crop__name__icontains=search_query)
            )

        if expense_type:
            queryset = queryset.filter(
                expense_type=expense_type
            )

        if crop:
            queryset = queryset.filter(crop_id=crop)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get(
            'search', ''
        )

        context['selected_type'] = self.request.GET.get(
            'expense_type', ''
        )

        context['selected_crop'] = self.request.GET.get(
            'crop', ''
        )

        context['expense_types'] = Expense.EXPENSE_TYPES

        context['crops'] = (
            Expense.objects
            .filter(crop__isnull=False)
            .values('crop_id', 'crop__name')
            .distinct()
            .order_by('crop__name')
        )

        context['total_expenses'] = (
            self.object_list.aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        context['total_records'] = self.object_list.count()

        return context


class ExpenseCreateView(AdminRequiredMixin, CreateView):

    model = Expense
    form_class = ExpenseForm
    template_name = 'farm_records/expense_form.html'
    success_url = reverse_lazy('farm_records:expense_list')

    def form_valid(self, form):

        messages.success(
            self.request,
            'Expense recorded successfully.'
        )

        return super().form_valid(form)


class ExpenseDetailView(AdminRequiredMixin, DetailView):

    model = Expense
    template_name = 'farm_records/expense_detail.html'
    context_object_name = 'expense'

    def get_queryset(self):

        return Expense.objects.select_related(
            'crop',
            'crop__category',
            'crop__field',
        )


class ExpenseUpdateView(AdminRequiredMixin, UpdateView):

    model = Expense
    form_class = ExpenseForm
    template_name = 'farm_records/expense_form.html'
    context_object_name = 'expense'

    def get_success_url(self):

        return reverse_lazy(
            'farm_records:expense_detail',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            'Expense updated successfully.'
        )

        return super().form_valid(form)


class ExpenseDeleteView(AdminRequiredMixin, DeleteView):

    model = Expense
    template_name = 'farm_records/expense_confirm_delete.html'
    context_object_name = 'expense'
    success_url = reverse_lazy('farm_records:expense_list')

    def form_valid(self, form):

        messages.success(
            self.request,
            'Expense deleted successfully.'
        )

        return super().form_valid(form)
