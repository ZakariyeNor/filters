from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver([post_save, post_delete], sender=Product)
def clear_products_cache(sender, instance, **kwargs):
    """
    Invalidate all product list caches when a product is added/updated/deleted.
    """
    try:
        # Delete all keys starting with "products:list:"
        cache.delete_pattern("products:list*")
    except AttributeError:
        # fallback if backend doesn't support delete_pattern
        cache.clear()