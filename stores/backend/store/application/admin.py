from django.contrib import admin
from .models import Profile, Category, Brand, Product, Purchase, Sale,Brands_list

from django.contrib.admin import AdminSite
from django.contrib.auth.views import LogoutView
from django.urls import path

from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def logout(self, request, extra_context=None):
        from django.contrib.auth.views import logout_then_login
        return logout_then_login(request, login_url='application:login') 

custom_admin_site = CustomAdminSite(name='custom_admin')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'category' )

@admin.register(Brands_list)
class Brand_listsAdmin(admin.ModelAdmin):
    list_display =('brand_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand', 'purchase_price', 'sale_price', 'quantity_in_stock','photo')
    list_filter = ('brand' , 'product_name')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_purchased', 'purchase_date', 'admin')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'sale_date', 'employee')
