from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


# vendor_management/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor


# vendor_management/views.py


# vendor_management/views.py

from django.utils import timezone  # Import timezone
from .signals import (
    update_average_response_time,
)  # Import the update_average_response_time function


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import PurchaseOrder, Vendor
from .signals import update_average_response_time


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            performance_metrics = {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }
            return Response(performance_metrics, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            # Trigger recalculation of average response time
            update_average_response_time(
                sender=PurchaseOrder, instance=purchase_order, created=False
            )
            return Response(
                {"message": "Purchase order acknowledged successfully"},
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND
            )
