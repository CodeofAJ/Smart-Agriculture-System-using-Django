
from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Activity list
    path(
        '',
        views.FarmActivityListView.as_view(),
        name='list'
    ),

    # Create activity
    path(
        'add/',
        views.FarmActivityCreateView.as_view(),
        name='add'
    ),

    # Activity details
    path(
        '<int:pk>/',
        views.FarmActivityDetailView.as_view(),
        name='detail'
    ),

    # Update activity
    path(
        '<int:pk>/edit/',
        views.FarmActivityUpdateView.as_view(),
        name='edit'
    ),

    # Delete activity
    path(
        '<int:pk>/delete/',
        views.FarmActivityDeleteView.as_view(),
        name='delete'
    ),
]
