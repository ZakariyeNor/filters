# products/optimizations.py
import hashlib
from urllib.parse import urlencode
from django.core.cache import cache
from django.template.loader import render_to_string

def cache_key_for_request(prefix: str, get_items):
    """
    Create a stable cache key for a filter request.
    Includes page number & GET params.
    """
    _s = urlencode(sorted(get_items))
    return f"{prefix}:{hashlib.md5(_s.encode()).hexdigest()}"

def cache_products_response(request, products_page, active_filters):
    """
    Cache the rendered products HTML & active filters for a filter request.
    """
    key = cache_key_for_request("products:list", request.GET.items())
    cached = cache.get(key)
    if cached:
        return cached  # Cache hit

    # Cache miss — render and store
    products_html = render_to_string("products/partials/multi_tags_list.html", {"products": products_page})
    tags_html = render_to_string("products/partials/active_filters.html", {"active_filters": active_filters})
    payload = {"html": products_html, "tags_html": tags_html}

    # Save in Redis for 60 seconds
    cache.set(key, payload, timeout=60 * 5)  # 5 min TTL
    return payload
