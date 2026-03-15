from django.db.models.signals import pre_save
from django.dispatch import receiver
from orders.models import Order


@receiver(pre_save, sender=Order)
def deduct_inventory_on_order_done(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            # Check if status is transitioning to DONE
            if (
                old_order.status != Order.Status.DONE
                and instance.status == Order.Status.DONE
            ):
                for item in instance.items.all():
                    part = item.part
                    part.stock_level -= item.quantity
                    part.save(update_fields=["stock_level"])
        except Order.DoesNotExist:
            pass
