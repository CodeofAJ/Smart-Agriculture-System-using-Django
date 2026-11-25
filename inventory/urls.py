from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.InventoryListView.as_view(), name="list"),
    path("add/", views.InventoryCreateView.as_view(), name="add"),
    path("<int:pk>/", views.InventoryDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.InventoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.InventoryDeleteView.as_view(), name="delete"),
    path("<int:pk>/stock-in/", views.StockInView.as_view(), name="stock_in"),
    path("<int:pk>/stock-out/", views.StockOutView.as_view(), name="stock_out"),
    path(
        "transactions/",
        views.InventoryTransactionListView.as_view(),
        name="transactions",
    ),
    path(
        "<int:pk>/transactions/",
        views.InventoryTransactionListView.as_view(),
        name="item_transactions",
    ),
]
