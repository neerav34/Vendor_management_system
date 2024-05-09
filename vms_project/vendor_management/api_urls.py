# vendor_management/api_urls.py

from django.urls import path, include
from rest_framework import routers
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet

router = routers.DefaultRouter()
router.register(r"vendors", VendorViewSet)
router.register(r"purchase-orders", PurchaseOrderViewSet)
router.register(r"historical-performances", HistoricalPerformanceViewSet)


# vendor_management/api_urls.py

from django.urls import path
from .views import VendorPerformanceView

urlpatterns = [
    path("", include(router.urls)),
    path(
        "vendors/<int:vendor_id>/performance/",
        VendorPerformanceView.as_view(),
        name="vendor_performance",
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        AcknowledgePurchaseOrderView.as_view(),
        name="acknowledge_purchase_order",
    ),
    path(
        "vendors/<int:vendor_id>/performance/",
        VendorPerformanceView.as_view(),
        name="vendor_performance",
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        AcknowledgePurchaseOrderView.as_view(),
        name="acknowledge_purchase_order",
    ),
]

# vendor_management/api_urls.py

from .views import AcknowledgePurchaseOrderView
