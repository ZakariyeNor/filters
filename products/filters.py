import django_filters
from django import forms
from .models import Product, Category, Brand

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category",
        widget=forms.Select(attrs={
            "class": "p-2 border border-gray-300 rounded-md"
        }),
    )

    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.all(),
        field_name="brand",
        widget=forms.Select(attrs={
            "class": "p-2 border border-gray-300 rounded-md"
        }),
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        widget=forms.NumberInput(attrs={
            "class": "p-2 border border-gray-300 rounded-md",
            "placeholder": "Min Price"
        })
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        widget=forms.NumberInput(attrs={
            "class": "p-2 border border-gray-300 rounded-md",
            "placeholder": "Max Price"
        })
    )

    status = django_filters.ChoiceFilter(
        choices=Product.STATUS_CHOICES,
        field_name="status",
        widget=forms.Select(attrs={
            "class": "p-2 border border-gray-300 rounded-md"
        }),
    )

    class Meta:
        model = Product
        fields = ["category", "brand", "status", "min_price", "max_price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.filters['category'].field.empty_label = "-- All Categories --"
        self.filters['brand'].field.empty_label = "-- All Brands --"
        self.filters['status'].field.empty_label = "-- Any Status --"
