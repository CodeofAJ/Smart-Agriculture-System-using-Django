
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='list'),
    path('add/', views.InventoryCreateView.as_view(), name='add'),
    path('<int:pk>/', views.InventoryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.InventoryUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='delete'),
]
