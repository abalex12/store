from django.db import transaction
from .models import Category, Brand, Product
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Brand, Product
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Brand, Product
from django.urls import reverse_lazy


def delete_product(pk):
    try:
        product = Product.objects.get(id=pk)
        product.soft_delete()
        return True, "Product soft-deleted successfully."
    except Product.DoesNotExist:
        return False, "Product not found."

def delete_brand(brand_id, category_id):
    try:
        with transaction.atomic():
            brand = Brand.objects.get(id=brand_id, category_id=category_id)
            brand.soft_delete()
        return True, "Brand relation with category soft-deleted successfully."
    except Brand.DoesNotExist:
        return False, "Brand not found for the given category."

# def delete_category(category_id):
    try:
        with transaction.atomic():
            category = Category.objects.get(id=category_id)
            
            # Get all brands associated with this category
            brands = Brand.objects.filter(category=category)
            
            # Get all products associated with these brands
            products = Product.objects.filter(brand__in=brands)
            
            # Soft-delete the products
            for product in products:
                product.soft_delete()
            
            # Soft-delete the brand relations
            for brand in brands:
                brand.soft_delete()
            
            # Soft-delete the category
            category.soft_delete()
            
        return True, "Category and associated brands and products soft-deleted successfully."
    except Category.DoesNotExist:
        return False, "Category not found."
    
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    brands=Brand.objects.filter( category=category)
    products = Product.objects.filter(brand__in=brands)
    context = {
        'brand':brands,
        'product':products,
        'object': category,
    }
    if request.method == 'POST':
        category.delete()
        return redirect(reverse_lazy('application:category'))
    return render(request, 'confirm_delete.html', context)
