from django.db.models.signals import post_save
from django.dispatch import receiver
from nurse.models import RequestedItems


@receiver(post_save, sender=RequestedItems)
def update_request_totals(sender, instance, **kwargs):
    instance.request.update_totals()
