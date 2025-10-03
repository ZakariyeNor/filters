from django.contrib import admin
from .models import Category, Brand, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'status', 'price', 'stock', 'created_at')
    list_filter = ('status', 'category', 'brand')
    search_fields = ('name',)
