
from django.contrib import messages
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

from .models import Inventory
from .forms import InventoryForm


# --------------------------------------------------
# Admin Access Protection
# --------------------------------------------------

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


# --------------------------------------------------
# Inventory List View
# --------------------------------------------------

class InventoryListView(AdminRequiredMixin, ListView):
    model = Inventory
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = Inventory.objects.all().order_by('name')

        # Search by item name or description
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        # Filter by item type
        item_type = self.request.GET.get('item_type', '')

        valid_item_types = dict(Inventory.ITEM_TYPES)

        if item_type in valid_item_types:
            queryset = queryset.filter(item_type=item_type)

        # Filter by stock status
        stock_status = self.request.GET.get('stock_status', '')

        if stock_status == 'LOW':
            queryset = queryset.filter(
                quantity__lte=F('minimum_quantity')
            )

        elif stock_status == 'AVAILABLE':
            queryset = queryset.filter(
                quantity__gt=F('minimum_quantity')
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['selected_item_type'] = self.request.GET.get(
            'item_type', ''
        )
        context['selected_stock_status'] = self.request.GET.get(
            'stock_status', ''
        )

        context['item_types'] = Inventory.ITEM_TYPES

        return context


# --------------------------------------------------
# Inventory Create View
# --------------------------------------------------

class InventoryCreateView(AdminRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Inventory item created successfully!'
        )
        return super().form_valid(form)


# --------------------------------------------------
# Inventory Detail View
# --------------------------------------------------

class InventoryDetailView(AdminRequiredMixin, DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'item'


# --------------------------------------------------
# Inventory Update View
# --------------------------------------------------

class InventoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    context_object_name = 'item'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Inventory item updated successfully!'
        )
        return super().form_valid(form)


# --------------------------------------------------
# Inventory Delete View
# --------------------------------------------------

class InventoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'inventory/inventory_confirm_delete.html'
    context_object_name = 'item'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Inventory item deleted successfully!'
        )
        return super().form_valid(form)
