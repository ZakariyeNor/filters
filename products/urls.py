from django.urls import path
from .views import ProductFilterView, ProductFilterChApplyView
from . import views

urlpatterns = [
    # For manual filtering with GET parameters
    path("", views.home, name="filter_home"),
    path('manual/', views.product_list, name='manual_list'),
    path("dj_filters/", ProductFilterView.as_view(), name="dj_filters_list"),
    path("facet_ch_apply", ProductFilterChApplyView.as_view(), name="checkbox_apply_list"),
    path("instant_filter/", views.product_list_ajax, name="product_list_ajax"),
    path("multi_tags/", views.product_list_multi, name="multi_tags_list"),
]