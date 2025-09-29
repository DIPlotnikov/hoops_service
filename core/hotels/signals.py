from django.dispatch import Signal, receiver

save_task_in_admin_panel = Signal()


@receiver(save_task_in_admin_panel)
def my_callback(sender, instance, **kwargs):
    count = instance.executers.all().count()
    if count > int(instance.count_executers):
        instance.count_executers = count
        instance.save()
