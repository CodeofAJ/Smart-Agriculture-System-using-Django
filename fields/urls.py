from django.urls import path

from .views import (
    FieldListView,
    FieldCreateView,
    FieldDetailView,
    FieldUpdateView,
    FieldDeleteView,
)

app_name = 'fields'

urlpatterns = [
    path('', FieldListView.as_view(), name='list'),
    path('add/', FieldCreateView.as_view(), name='add'),
    path('<int:pk>/', FieldDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', FieldUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', FieldDeleteView.as_view(), name='delete'),
]