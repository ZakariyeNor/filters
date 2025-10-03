from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Brand

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
        "products/list.html",
        {
            "products": products,
            "categories": categories,
            "brands": brands,
            "params": request.GET
        }
    )
