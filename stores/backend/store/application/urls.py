from django.urls import path
from .views import *
from .excel_generator_views import *
from .add_item_view import *
from . import edit_view
from . import delete_view

app_name='application'

urlpatterns = [
    path('',opencatagories, name="category"),
    path('login/',login_view,name="login"),
    path('logout/',custom_logout,name="logout"),
    path('brands/<int:category_id>',openbrand, name="brands"),
    path('inventory/', inventory_view, name='inventory_list'),
    path('product/<int:brand_id>/', product_list, name='product'),
    path('make_purchase/',make_sale, name='make_sale'),
    path('sale-history/', sale_history, name='sale_history'),
    path('export-products/', export_products_excel, name='export_products_excel'),
    path('export-sales/', export_sales_excel, name='export_sales_excel'),

    path('categories/add/', add_category, name='add_category'),
    path('categories/<int:category_id>/brands/add/', add_brand, name='add_brand'),
    path('brands/<int:brand_id>/products/add/', add_product, name='add_product'),

    path('category/<int:pk>/edit/', edit_view.edit_category, name='edit_category'),
    path('brand/<int:pk>/edit/', edit_view.edit_brand, name='edit_brand'),
    path('product/<int:pk>/edit/', edit_view.edit_product, name='edit_product'),
    
    path('category/delete/<int:pk>/',delete_view.delete_category, name='category-delete'),
    path('brand/<int:brand_id>/<int:category_id>/delete/', delete_view.delete_brand, name='delete_brand'),
    path('product-delete/<int:pk>/', delete_view.delete_product, name='delete_product'),
    
]
    