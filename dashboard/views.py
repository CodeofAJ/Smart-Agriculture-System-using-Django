from django.shortcuts import render
import calendar
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.views.generic import TemplateView

from crops.models import Crop
from fields.models import Field
from activities.models import FarmActivity
from inventory.models import Inventory, InventoryTransaction
from farm_records.models import Harvest, Expense

from decimal import Decimal


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        # 

        context = super().get_context_data(**kwargs)

        today = timezone.localdate()



        # ----------------------------------
        # Dashboard Date Period Filter
        # ----------------------------------

        period = self.request.GET.get('period', 'this_year')

        valid_periods = ['this_month', 'this_year', 'all_time']

        if period not in valid_periods:
            period = 'this_year'

        if period == 'this_month':
            start_date = today.replace(day=1)
            period_label = 'This Month'

        elif period == 'this_year':
            start_date = today.replace(month=1, day=1)
            period_label = 'This Year'

        else:
            start_date = None
            period_label = 'All Time'

        context['selected_period'] = period
        context['period_label'] = period_label

        # Reusable date-filtered querysets
        harvest_queryset = Harvest.objects.all()
        expense_queryset = Expense.objects.all()
        inventory_queryset = InventoryTransaction.objects.all()

        if start_date:
            harvest_queryset = harvest_queryset.filter(
                harvest_date__gte=start_date
            )

            expense_queryset = expense_queryset.filter(
                expense_date__gte=start_date
            )

            inventory_queryset = inventory_queryset.filter(
                transaction_date__gte=start_date
            )


        # context['today'] = today

        # ----------------------------------
        # Farm Overview
        # ----------------------------------

        context['total_fields'] = Field.objects.count()

        context['total_crops'] = Crop.objects.count()

        context['growing_crops'] = Crop.objects.filter(
            status='GROWING'
        ).count()

        context['planned_crops'] = Crop.objects.filter(
            status='PLANNED'
        ).count()

        context['harvested_crops'] = Crop.objects.filter(
            status='HARVESTED'
        ).count()

        # ----------------------------------
        # Inventory Overview
        # ----------------------------------

        context['total_inventory_items'] = Inventory.objects.count()

        context['low_stock_items'] = Inventory.objects.filter(
            quantity__lte=F('minimum_quantity')
        ).order_by('quantity')[:5]

        context['low_stock_count'] = Inventory.objects.filter(
            quantity__lte=F('minimum_quantity')
        ).count()

        context['stock_in_count'] = InventoryTransaction.objects.filter(
            transaction_type='STOCK_IN'
        ).count()

        context['stock_out_count'] = InventoryTransaction.objects.filter(
            transaction_type='STOCK_OUT'
        ).count()

        context['recent_inventory_transactions'] = (
            InventoryTransaction.objects
            .select_related('inventory')
            .order_by('-transaction_date', '-created_at')[:5]
        )

        # ----------------------------------
        # Farm Activities
        # ----------------------------------

        context['total_activities'] = FarmActivity.objects.count()

        context['recent_activities'] = (
            FarmActivity.objects
            .select_related('crop', 'crop__field')
            .order_by('-activity_date', '-created_at')[:5]
        )

   
        # ----------------------------------
        # Harvest Revenue
        # ----------------------------------

        # harvest_summary = Harvest.objects.aggregate(
        #     total_quantity=Sum('quantity'),
        # )

        # total_harvest_quantity = (
        #     harvest_summary['total_quantity'] or 0
        # )

        # total_harvest_revenue = sum(
        #     (
        #         harvest.quantity * harvest.selling_price
        #         for harvest in Harvest.objects.all()
        #     ),
        #     start=0
        # )

        # context['total_harvest_quantity'] = total_harvest_quantity
        # context['total_harvest_revenue'] = total_harvest_revenue

        # ----------------------------------
        # Total Farm Expenses
        # ----------------------------------

        # expense_summary = Expense.objects.aggregate(
        #     total_expenses=Sum('amount')
        # )

        # total_expenses = expense_summary['total_expenses'] or 0
  
        # context['total_expenses'] = total_expenses

        # ----------------------------------
        # Net Farm Profit
        # ----------------------------------

        # net_profit = total_harvest_revenue - total_expenses

        # context['net_profit'] = net_profit

######################################################################################
        
        # ----------------------------------
        # Period-Based Harvest Revenue
        # ----------------------------------

        harvest_summary = harvest_queryset.aggregate(
            total_quantity=Sum('quantity')
        )

        total_harvest_quantity = (
            harvest_summary['total_quantity'] or Decimal('0')
        )

        total_harvest_revenue = sum(
            (
                harvest.quantity * harvest.selling_price
                for harvest in harvest_queryset
            ),
            start=Decimal('0')
        )

        context['total_harvest_quantity'] = total_harvest_quantity
        context['total_harvest_revenue'] = total_harvest_revenue

        # ----------------------------------
        # Period-Based Farm Expenses
        # ----------------------------------

        expense_summary = expense_queryset.aggregate(
            total_expenses=Sum('amount')
        )

        total_expenses = (
            expense_summary['total_expenses'] or Decimal('0')
        )

        context['total_expenses'] = total_expenses

        # ----------------------------------
        # Period-Based Net Farm Profit
        # ----------------------------------

        net_profit = total_harvest_revenue - total_expenses

        context['net_profit'] = net_profit






        # ----------------------------------
        # Expense Overview
        # ----------------------------------

        expense_summary = Expense.objects.aggregate(
            total_expenses=Sum('amount')
        )

        context['total_expenses'] = (
            expense_summary['total_expenses'] or 0
        )

        context['recent_expenses'] = (
            Expense.objects
            .select_related('crop')
            .order_by('-expense_date', '-created_at')[:5]
        )

        # ----------------------------------
        # Today's Overview
        # ----------------------------------

        context['today_activities'] = FarmActivity.objects.filter(
            activity_date=today
        ).count()

        context['today_harvests'] = Harvest.objects.filter(
            harvest_date=today
        ).count()

        context['today'] = today


        # ----------------------------------
        # Crop Distribution Chart
        # ----------------------------------

        crop_distribution = Crop.objects.values(
            'status'
        ).annotate(
            total=Count('id')
        ).order_by('status')

        context['crop_chart_labels'] = [
            dict(Crop.STATUS_CHOICES).get(item['status'], item['status'])
            for item in crop_distribution
        ]

        context['crop_chart_data'] = [
            item['total']
            for item in crop_distribution
        ]

        

        # ----------------------------------
        # Monthly Harvest Chart
        # ----------------------------------

        harvest_records = list(
            harvest_queryset
            .annotate(month=TruncMonth('harvest_date'))
            .values('month', 'unit')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('month', 'unit')
        )

        harvest_months = sorted({
            record['month'] for record in harvest_records
        })

        context['harvest_chart_labels'] = [
            month.strftime('%b %Y') for month in harvest_months
        ]

        harvest_units = sorted({
            record['unit'] for record in harvest_records
        })

        harvest_lookup = {
            (record['month'], record['unit']): float(
                record['total_quantity'] or 0
            )
            for record in harvest_records
        }

        context['harvest_chart_datasets'] = [
            {
                'label': unit,
                'data': [
                    harvest_lookup.get((month, unit), 0)
                    for month in harvest_months
                ]
            }
            for unit in harvest_units
        ]



        
        # ----------------------------------
        # Monthly Expenses Chart
        # ----------------------------------

        expense_records = list(
            expense_queryset
            .annotate(month=TruncMonth('expense_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        expense_months = [
            record['month'] for record in expense_records
        ]

        context['expense_chart_labels'] = [
            month.strftime('%b %Y') for month in expense_months
        ]

        context['expense_chart_data'] = [
            float(record['total_amount'] or 0)
            for record in expense_records
        ]

        
        
        # ----------------------------------
        # Monthly Inventory Movement Chart
        # ----------------------------------

        inventory_records = list(
            inventory_queryset
            .annotate(month=TruncMonth('transaction_date'))
            .values('month', 'inventory__unit', 'transaction_type')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('month', 'inventory__unit', 'transaction_type')
        )

        inventory_months = sorted({
            record['month'] for record in inventory_records
        })

        context['inventory_chart_labels'] = [
            month.strftime('%b %Y') for month in inventory_months
        ]

        inventory_units = sorted({
            record['inventory__unit']
            for record in inventory_records
        })

        inventory_lookup = {
            (
                record['month'],
                record['inventory__unit'],
                record['transaction_type']
            ): float(record['total_quantity'] or 0)
            for record in inventory_records
        }

        inventory_chart_datasets = []

        for unit in inventory_units:
            for transaction_type in ['STOCK_IN', 'STOCK_OUT']:

                inventory_chart_datasets.append({
                    'label': (
                        f"{'Stock In' if transaction_type == 'STOCK_IN' else 'Stock Out'} ({unit})"
                    ),
                    'data': [
                        inventory_lookup.get(
                            (month, unit, transaction_type), 0
                        )
                        for month in inventory_months
                    ],
                    'transaction_type': transaction_type,
                    'unit': unit,
                })

        context['inventory_chart_datasets'] = inventory_chart_datasets


 

        return context

# Create your views here.
