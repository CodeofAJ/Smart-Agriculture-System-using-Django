
from django.urls import path

from . import views

app_name = 'farm_records'

urlpatterns = [
    # Harvest Management
    path(
        'harvests/',
        views.HarvestListView.as_view(),
        name='harvest_list',
    ),

    path(
        'harvests/add/',
        views.HarvestCreateView.as_view(),
        name='harvest_add',
    ),

    path(
        'harvests/<int:pk>/',
        views.HarvestDetailView.as_view(),
        name='harvest_detail',
    ),

    path(
        'harvests/<int:pk>/edit/',
        views.HarvestUpdateView.as_view(),
        name='harvest_edit',
    ),

    path(
        'harvests/<int:pk>/delete/',
        views.HarvestDeleteView.as_view(),
        name='harvest_delete',
    ),
]
