from django.dispatch import receiver
from fast_drf import signals


@receiver(signals.before_post_api)
def receiver_before_post_api(sender, requested_data, **kwargs):
    print(sender, requested_data)


@receiver(signals.after_post_api)
def receiver_after_post_api(sender, instance, requested_data, **kwargs):
    print(sender, instance, requested_data)
