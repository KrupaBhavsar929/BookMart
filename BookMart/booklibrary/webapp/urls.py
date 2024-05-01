
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('myapp.urls')),
    path("mydminapp", include('mydminapp.urls')),
    path("supplier", include('supplier.urls')),
]
