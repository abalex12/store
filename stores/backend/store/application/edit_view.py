from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Brands_list, Brand, Product
from .forms import CategoryForm, BrandsListForm, BrandForm, ProductForm
from django.contrib import messages
from fuzzywuzzy import fuzz

# Your existing add_category, add_brand, and add_product views remain unchanged

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            # Normalize the category name input
            category_name = form.cleaned_data['category_name'].strip().lower()
            
            # Get all existing category names, excluding the current category
            existing_categories = Category.objects.exclude(pk=pk).values_list('category_name', flat=True)
            
            # Check for fuzzy matches (similar to add_category logic)
            highest_ratio = 0
            most_similar_category = None
            for existing_name in existing_categories:
                ratio = fuzz.ratio(category_name, existing_name.lower())
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    most_similar_category = existing_name
            
            if highest_ratio > 80:  # Adjust the threshold as needed
                messages.error(request, f'Category name is too similar to existing category "{most_similar_category}".')
                return render(request, 'edit_category.html', {'form': form, 'category': category})
            
            form.instance.category_name = category_name.capitalize()
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('application:category')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'add_item/add_category.html', {'is_edit':True,'form': form, 'category': category})

@login_required
def edit_brand(request, pk):
    brand=get_object_or_404(Brand,pk=pk)
    brands_list = get_object_or_404(Brands_list,brand_name=brand.brand_name)
    if request.method == 'POST':
        form = BrandsListForm(request.POST, request.FILES, instance=brands_list)
        if form.is_valid():
            # Normalize the brand name
            brand_name = form.cleaned_data['brand_name'].strip().lower()
            
            # Check if the brand name already exists (excluding this brand)
            existing_brands = Brands_list.objects.exclude(pk=brands_list.pk).filter(brand_name__iexact=brand_name)
            
            if existing_brands.exists():
                messages.error(request, f"Brand name '{brand_name}' already exists.")
                return render(request, 'add_item/add_brand.html', {'is_edit':True,'brands_list_form': form, 'brand': brands_list})
            
            form.instance.brand_name = brand_name.capitalize()
            form.save()
            messages.success(request, 'Brand updated successfully.')
            
            # Redirect to the brands list of the first category this brand is associated with
            related_brand = Brand.objects.filter(brand_name=brands_list).first()
            if related_brand and related_brand.category:
                return redirect('application:brands', category_id=related_brand.category.id)
            return redirect('application:category')
    else:
        form = BrandsListForm(instance=brands_list)
    
    return render(request, 'add_item/add_brand.html', {'is_edit':True,'brands_list_form': form, 'brand': brands_list})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, is_edit=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('application:product', brand_id=product.brand.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product, is_edit = True)
    
    return render(request, 'add_item/add_product.html', {'is_edit':True,'form': form, 'product': product})