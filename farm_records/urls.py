from django.urls import path

from . import views

app_name = "farm_records"

urlpatterns = [
    # Harvest Management
    path(
        "harvests/",
        views.HarvestListView.as_view(),
        name="harvest_list",
    ),
    path(
        "harvests/add/",
        views.HarvestCreateView.as_view(),
        name="harvest_add",
    ),
    path(
        "harvests/<int:pk>/",
        views.HarvestDetailView.as_view(),
        name="harvest_detail",
    ),
    path(
        "harvests/<int:pk>/edit/",
        views.HarvestUpdateView.as_view(),
        name="harvest_edit",
    ),
    path(
        "harvests/<int:pk>/delete/",
        views.HarvestDeleteView.as_view(),
        name="harvest_delete",
    ),
    
    # Expense Management
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense_add'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),



]
