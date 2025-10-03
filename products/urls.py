from django.urls import path
from .views import ProductFilterView
from . import views

urlpatterns = [
    path("", ProductFilterView.as_view(), name="product_list"),
]


# For manual filtering with GET parameters
# path('', views.product_list, name='product_list')