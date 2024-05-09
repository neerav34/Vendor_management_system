# vendor_management/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F, Avg, ExpressionWrapper
from django.db.models.fields import DurationField
from .models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == "completed":
        vendor = instance.vendor
        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status="completed"
        ).count()
        on_time_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status="completed",
            delivery_date__lte=F("expected_delivery_date"),
        ).count()
        on_time_delivery_rate = (
            (on_time_orders / total_completed_orders) * 100
            if total_completed_orders > 0
            else 0
        )
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_average(sender, instance, created, **kwargs):
    if instance.status == "completed" and instance.quality_rating is not None:
        vendor = instance.vendor
        quality_rating_avg = (
            PurchaseOrder.objects.filter(vendor=vendor, status="completed").aggregate(
                avg_quality_rating=Avg("quality_rating")
            )["avg_quality_rating"]
            or 0
        )
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        total_orders = PurchaseOrder.objects.filter(
            vendor=vendor
        ).count()  # Calculate total orders
        response_times = (
            PurchaseOrder.objects.filter(
                vendor=vendor, acknowledgment_date__isnull=False
            )
            .annotate(
                response_time=ExpressionWrapper(
                    F("acknowledgment_date") - F("issue_date"),
                    output_field=DurationField(),
                )
            )
            .aggregate(avg_response_time=Avg("response_time"))["avg_response_time"]
        )
        average_response_time = (
            response_times.total_seconds() / total_orders if response_times else 0
        )
        vendor.average_response_time = average_response_time
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed"
    ).count()
    fulfillment_rate = (
        (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
    )
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
