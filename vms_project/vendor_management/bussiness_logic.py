from .models import Vendor, PurchaseOrder, HistoricalPerformance

from django.db.models import Avg, ExpressionWrapper, F
from django.db.models.functions import Now
from django.db.models.fields import DurationField
from .models import Vendor, PurchaseOrder, HistoricalPerformance

def calculate_vendor_performance_metrics(vendor):
    # Calculate on-time delivery rate
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    on_time_orders = PurchaseOrder.objects.filter(
        vendor=vendor, delivery_date__lte=F("expected_delivery_date")
    ).count()
    on_time_delivery_rate = (
        (on_time_orders / total_orders) * 100 if total_orders > 0 else 0
    )

    # Calculate quality rating average
    quality_rating_avg = (
        PurchaseOrder.objects.filter(vendor=vendor).aggregate(Avg("quality_rating"))[
            "quality_rating__avg"
        ]
        or 0
    )

    # Calculate average response time
    response_times = (
        PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        .annotate(
            response_time=ExpressionWrapper(
                F("acknowledgment_date") - F("issue_date"), output_field=DurationField()
            )
        )
        .aggregate(avg_response_time=Avg("response_time"))["avg_response_time"]
    )
    average_response_time = (
        response_times.total_seconds() / total_orders if response_times else 0
    )

    # Calculate fulfillment rate
    fulfilled_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed"
    ).count()
    fulfillment_rate = (
        (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
    )

    # Update or create HistoricalPerformance record
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate,
    )
