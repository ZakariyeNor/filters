from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Brand

from django_filters.views import FilterView
from .filters import ProductFilter

from django.shortcuts import render

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
