from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from.models import Ride
from.cache_service import invalidate_ride_cache

@receiver(post_save, sender=Ride)
@receiver(post_delete, sender=Ride)
def clear_cache_on_ride_change(sender, **kwargs):
    invalidate_ride_cache()