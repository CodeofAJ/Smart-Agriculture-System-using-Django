
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F, Sum
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
)

from .models import Inventory, InventoryTransaction
from .forms import InventoryForm, InventoryTransactionForm


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
    
    

class StockTransactionCreateView(AdminRequiredMixin, FormView):

    template_name = 'inventory/stock_transaction_form.html'
    form_class = InventoryTransactionForm

    # Subclasses will define STOCK_IN or STOCK_OUT.
    transaction_type = None

    def get_inventory(self):
        return get_object_or_404(
            Inventory,
            pk=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['item'] = self.get_inventory()
        context['transaction_type'] = self.transaction_type

        context['is_stock_in'] = (
            self.transaction_type == 'STOCK_IN'
        )

        return context

    def form_valid(self, form):

        try:
            with transaction.atomic():

                # Lock the inventory record while processing.
                item = Inventory.objects.select_for_update().get(
                    pk=self.kwargs['pk']
                )

                quantity = form.cleaned_data['quantity']
                previous_quantity = item.quantity

                # Calculate the new stock quantity.
                if self.transaction_type == 'STOCK_IN':

                    new_quantity = previous_quantity + quantity

                elif self.transaction_type == 'STOCK_OUT':

                    if quantity > previous_quantity:
                        form.add_error(
                            'quantity',
                            'Insufficient stock! Available quantity is '
                            f'{previous_quantity} {item.unit}.'
                        )

                        return self.form_invalid(form)

                    new_quantity = previous_quantity - quantity

                else:
                    raise ValueError('Invalid transaction type.')

                # Update inventory quantity.
                item.quantity = new_quantity

                item.save(update_fields=['quantity', 'updated_at'])

                # Create transaction history.
                InventoryTransaction.objects.create(
                    inventory=item,
                    transaction_type=self.transaction_type,
                    quantity=quantity,
                    previous_quantity=previous_quantity,
                    new_quantity=new_quantity,
                    transaction_date=form.cleaned_data[
                        'transaction_date'
                    ],
                    reference=form.cleaned_data['reference'],
                    notes=form.cleaned_data['notes'],
                )

        except Inventory.DoesNotExist:
            return redirect('inventory:list')

        messages.success(
            self.request,
            f'{self.get_transaction_label()} completed successfully!'
        )

        return redirect(
            'inventory:detail',
            pk=self.kwargs['pk']
        )

    def get_transaction_label(self):
        if self.transaction_type == 'STOCK_IN':
            return 'Stock-In'

        return 'Stock-Out'


class StockInView(StockTransactionCreateView):
    transaction_type = 'STOCK_IN'


class StockOutView(StockTransactionCreateView):
    transaction_type = 'STOCK_OUT'



class InventoryTransactionListView(AdminRequiredMixin, ListView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 15

    def get_queryset(self):
        queryset = InventoryTransaction.objects.select_related(
            'inventory'
        ).order_by('-transaction_date', '-created_at')

        # Optional: show transactions for one inventory item only.
        inventory_id = self.kwargs.get('pk')

        if inventory_id:
            queryset = queryset.filter(inventory_id=inventory_id)

        # Search item name, reference number, and notes.
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(inventory__name__icontains=search_query)
                | Q(reference__icontains=search_query)
                | Q(notes__icontains=search_query)
            )

        # Filter by transaction type.
        transaction_type = self.request.GET.get(
            'transaction_type', ''
        )

        valid_types = dict(
            InventoryTransaction.TRANSACTION_TYPES
        )

        if transaction_type in valid_types:
            queryset = queryset.filter(
                transaction_type=transaction_type
            )

        # Filter by inventory item.
        selected_inventory = self.request.GET.get('inventory', '')

        if selected_inventory.isdigit():
            queryset = queryset.filter(
                inventory_id=int(selected_inventory)
            )

        # Filter by transaction date range.
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        from django.utils.dateparse import parse_date

        parsed_date_from = parse_date(date_from) if date_from else None
        parsed_date_to = parse_date(date_to) if date_to else None

        if parsed_date_from:
            queryset = queryset.filter(
                transaction_date__gte=parsed_date_from
            )

        if parsed_date_to:
            queryset = queryset.filter(
                transaction_date__lte=parsed_date_to
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Preserve filter values in the template.
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_type'] = self.request.GET.get(
            'transaction_type', ''
        )
        context['selected_inventory'] = self.request.GET.get(
            'inventory', ''
        )
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')

        context['transaction_types'] = (
            InventoryTransaction.TRANSACTION_TYPES
        )

        context['inventory_items'] = Inventory.objects.order_by('name')

        # Summary totals for the filtered result set.
        filtered_transactions = self.get_queryset()

        # context['total_stock_in'] = (
        #     filtered_transactions.filter(
        #         transaction_type='STOCK_IN'
        #     ).aggregate(total=Sum('quantity'))['total'] or 0
        # )

        # context['total_stock_out'] = (
        #     filtered_transactions.filter(
        #         transaction_type='STOCK_OUT'
        #     ).aggregate(total=Sum('quantity'))['total'] or 0
        # )

        context['total_stock_in'] = filtered_transactions.filter(
            transaction_type='STOCK_IN'
        ).count()

        context['total_stock_out'] = filtered_transactions.filter(
            transaction_type='STOCK_OUT'
        ).count()

        context['is_item_history'] = bool(self.kwargs.get('pk'))

        if self.kwargs.get('pk'):
            context['item'] = get_object_or_404(
                Inventory,
                pk=self.kwargs['pk']
            )

        return context


