from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path('dashboard/', include('dashboard.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("crops/", include("crops.urls")),
    # Field Management
    path("fields/", include("fields.urls")),
    path("activities/", include("activities.urls")),
    path('inventory/', include('inventory.urls')),

    # HArvest 
    path('farm-records/', include('farm_records.urls')),
]
