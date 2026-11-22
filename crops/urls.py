from django.urls import path

from .views import (
    CropListView,
    CropCreateView,
    CropDetailView,
    CropUpdateView,
    CropDeleteView,
)


app_name = 'crops'


urlpatterns = [

    path('', CropListView.as_view(), name='list'),

    path('add/', CropCreateView.as_view(), name='add'),

    path('<int:pk>/', CropDetailView.as_view(), name='detail'),

    path('<int:pk>/edit/', CropUpdateView.as_view(), name='edit'),

    path('<int:pk>/delete/', CropDeleteView.as_view(), name='delete'),

]