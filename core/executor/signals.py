from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from hotels.models import ExecuterState

from .models import Metrics


@receiver(post_save, sender=ExecuterState)
def create_notification_for_partner(sender, instance, created, **kwargs):
    if created:
        metric = Metrics.objects.filter(executor=instance.executer).last()
        if not metric:
            Metrics.objects.create(executor=instance.executer, last_request_task=timezone.now())
        else:
            metric.last_request_task = timezone.now()
            metric.save()
