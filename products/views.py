from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Brand

from django_filters.views import FilterView
from .filters import ProductFilter

from django.shortcuts import render

from django.http import JsonResponse
from django.template.loader import render_to_string

# Instant filtering via AJAX
def product_list_ajax(request):
    query = Product.objects.all()
    
    # Filters
    category_ids = request.GET.getlist("category")
    if category_ids:
        query = query.filter(category_id__in=category_ids)
    
    brand = request.GET.get("brand")
    if brand:
        try:
            query = query.filter(brand_id=int(brand))
        except ValueError:
            pass
        query = query.filter(brand_id=int(brand))
    
    status = request.GET.getlist("status")
    if status:
        query = query.filter(status__in=status)
    
    price_bucket = request.GET.get("price_bucket")
    if price_bucket and "_" in price_bucket:
        try:
            min_price, max_price = price_bucket.split("_")
            query = query.filter(price__gte=int(min_price), price__lte=int(max_price))
        except ValueError:
            pass
            
    # Pagination
    page = int(request.GET.get("page", 1))
    paginator = Paginator(query, 32)
    products = paginator.get_page(page)
    
    # Context
    context = {
            "products": products,
            "page_obj": products,
            "categories": Category.objects.all(),
            "statuses": Product.STATUS_CHOICES,
            "brands": Brand.objects.all(),
        }
    
    # If AJAX, return redered HTML of the product list only
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            "products/partials/filter_instant_list.html",
            context,
        )
        return JsonResponse({"html": html})
    # Otherwise render full template
    return render(
        request,
        "products/product_list_ajax.html",
        context,
    )

# Map price_bucket values to min/max
PRICE_BUCKETS = {
    "0_50": (0, 50),
    "50_100": (50, 100),
    "100_200": (100, 200),
    "200_500": (200, 500),
    "500_800": (500, 800),
    "800_1000": (800, 1000),
}

# Multi-select tags
def product_list_multi(request):
    queries = Product.objects.all()
    
    # Multi-select filters
    selected_categories = [int(c) for c in request.GET.getlist("category") if c.isdigit()]
    selected_statuses = request.GET.getlist("status")
    selected_brands = [int(b) for b in request.GET.getlist("brand") if b.isdigit()]
    
    # Brand and price bucket
    selected_brand = request.GET.get("brand")
    price_bucket = request.GET.get("price_bucket")
    
    # Apply filters
    if selected_categories:
        queries = queries.filter(category__id__in=selected_categories)
    if selected_statuses:
        queries = queries.filter(status__in=selected_statuses)
    if selected_brands:
        queries = queries.filter(brand__id__in=selected_brands)
    if selected_brand and selected_brand.isdigit():
        queries = queries.filter(brand__id=int(selected_brand))
    
    if price_bucket in PRICE_BUCKETS:
        min_price, max_price = PRICE_BUCKETS[price_bucket]
        queries = queries.filter(price__gte=min_price, price__lte=max_price)
    
    # Active filters for display
    active_filters = {
        "category": Category.objects.filter(id__in=selected_categories),
        "status": [sts for sts in Product.STATUS_CHOICES if sts[0] in selected_statuses],
        "brand": Brand.objects.filter(id__in=selected_brands + ([int(selected_brand)] if selected_brand else [])),
        "price_bucket": price_bucket,
    }
    
    # Pagination
    page = int(request.GET.get("page", 1))
    paginator = Paginator(queries, 32)
    products = paginator.get_page(page)
    
    # AJAX response
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        html = render_to_string("products/partials/multi_tags_list.html", {"products": products})
        tags_html = render_to_string("products/partials/active_filters.html", {"active_filters": active_filters})
        return JsonResponse({"html": html, "tags_html": tags_html})
    
    # Render full page
    return render(
        request,
        "products/product_list_tags.html",
        {
            "products": products,
            "page_obj": products,
            "categories": Category.objects.all(),
            "statuses": Product.STATUS_CHOICES,
            "brands": Brand.objects.all(),
            "active_filters": active_filters,
            "selected_categories": selected_categories,
            "selected_statuses": selected_statuses,
            "selected_brands": selected_brands,
            "price_bucket": price_bucket,
            "selected_brand": selected_brand,
        }
    )
    
# Home page view
def home(request):
    """
    Home page for the Filter Engine.
    Displays information about manual GET filtering and automatic faceted filtering.
    """
    return render(request, "products/home.html")

# Facet sidebar phase 1 Checkbox + apply
class ProductFilterChApplyView(FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 24
    template_name = "products/ch_apply.html"
    context_object_name = "products"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        bucket = self.request.GET.get("price_bucket")
        if bucket and "_" in bucket:
            try:
                min_val, max_val = map(int, bucket.split("_"))
                queryset = queryset.filter(price__gte=min_val, price__lt=max_val)
            except ValueError:
                # Ignore invalid values
                pass

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # Category Facets
        context['category_facets'] = (
            Product.objects.values(
                "category__id", "category__name"
            ).annotate(count=Count('id')).order_by("-count")
        )
        
        # Status facets
        context['status_facets'] = (
            Product.objects.values('status')
            .annotate(count=Count('id'))
        )
        
        
        # Price Buckets
        context['price_buckets'] = queryset.aggregate(
            p_0_50=Count(Case(When(price__lt=50, then=1), output_field=IntegerField())),
            p_50_100=Count(Case(When(price__gte=50, price__lt=100, then=1), output_field=IntegerField())),
            p_100_200=Count(Case(When(price__gte=100, price__lt=200, then=1), output_field=IntegerField())),
            p_200_500=Count(Case(When(price__gte=200, price__lt=500, then=1), output_field=IntegerField())),
            p_500_800=Count(Case(When(price__gte=500, price__lt=800, then=1), output_field=IntegerField())),
            p_800_1000=Count(Case(When(price__gte=800, price__lte=1000, then=1), output_field=IntegerField())),
        )
        
        # Selected filters (pass to template)
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_statuses'] = self.request.GET.getlist('status')
        context['selected_price_bucket'] = self.request.GET.get('price_bucket', '')
        context['selected_price_bucket_display'] = (self.request.GET.get('price_bucket', '').replace("_", "–"))
        

        return context

# Django Filters
class ProductFilterView(FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 24
    template_name = "products/dj_filters.html"
    context_object_name = "products"
    
# Manual filtering with GET params
def product_list(request):
    qs = Product.objects.select_related("category","brand").all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # GET parameters
    category = request.GET.get("category")
    brand_id = request.GET.get("brand")
    status = request.GET.get("status")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Filters
    if category:
        qs = qs.filter(category__name=category.strip())
    if brand_id:
        qs = qs.filter(brand_id=brand_id)
    if status:
        qs = qs.filter(status=status.strip())

    try:
        if min_price:
            qs = qs.filter(price__gte=float(min_price))
        if max_price:
            qs = qs.filter(price__lte=float(max_price))
    except ValueError:
        pass

    # Pagination
    paginator = Paginator(qs, 24)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(
        request,
        "products/manual_filtering.html",
        {
            "products": products,
            "categories": categories,
            "brands": brands,
            "params": request.GET
        }
    )
