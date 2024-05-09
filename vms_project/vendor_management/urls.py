from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet

# Create a router and register viewsets with it
router = routers.DefaultRouter()
router.register(r"vendors", VendorViewSet)
router.register(r"purchase-orders", PurchaseOrderViewSet)
router.register(r"historical-performances", HistoricalPerformanceViewSet)

# The API URLs are now determined automatically by the router
# Additionally, we include the router URLs under the app's namespace
urlpatterns = [
    path("", include(router.urls)),
    path("api/", include("vendor_management.api_urls")),
    path("admin/", admin.site.urls),
    path("", include("vendor_management.api_urls")),
    path("admin/", admin.site.urls),
    path("api/", include("vendor_management.api_urls")),
]
# project/urls.py

