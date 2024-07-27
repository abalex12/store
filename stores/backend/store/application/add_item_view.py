from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Brands_list, Brand, Product
from .forms import CategoryForm, BrandsListForm, BrandForm, ProductForm
from django.contrib import messages
from fuzzywuzzy import fuzz


# Make sure to import your Category model

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            # Normalize the category name input
            category_name = form.cleaned_data['category_name'].strip().lower()
            
            # Get all existing category names
            existing_categories = Category.objects.values_list('category_name', flat=True)
            
            # Initialize variables to find the most similar category
            highest_ratio = 0
            most_similar_category = None

            # Check for fuzzy matches
            for existing_name in existing_categories:
                ratio = fuzz.ratio(category_name, existing_name.lower())
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    most_similar_category = existing_name
            
            # Determine if the similarity is high enough to consider it a duplicate
            if highest_ratio > 80:  # Adjust the threshold as needed
                # Add an error message with the most similar category
                messages.error(request, f'Category already exists or is similar to the existing category "{most_similar_category}".')
                return render(request, 'add_item/add_category.html', {'form': form})
            
            # Save the form if no similar category name exists
            form.instance.category_name = category_name.capitalize()  # Capitalize the name before saving
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('application:category')
    else:
        form = CategoryForm()
    
    return render(request, 'add_item/add_category.html', {'form': form})


@login_required
def add_brand(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        brands_list_form = BrandsListForm(request.POST, request.FILES)
        
        if brands_list_form.is_valid():
            # Normalize the brand name
            brand_name = brands_list_form.cleaned_data['brand_name'].strip().lower()
            brand_photo = brands_list_form.cleaned_data['photo']
            
            # Check if the brand already exists in Brands_list
            existing_brands = Brands_list.objects.filter(brand_name__iexact=brand_name)
            
            if existing_brands.exists():
                # Use the first existing brand
                brands_list = existing_brands.first()
                
                # Update photo if a new one was provided
                if brand_photo:
                    brands_list.photo = brand_photo
                    brands_list.save()
                
                created = False
            else:
                # Create a new brand if it doesn't exist
                brands_list = Brands_list.objects.create(brand_name=brand_name, photo=brand_photo)
                created = True

            # Check if this brand already exists for this category
            brand, brand_created = Brand.objects.get_or_create(
                brand_name=brands_list,
                category=category
            )

            if created:
                messages.success(request, f"Brand '{brands_list.brand_name.capitalize()}' added successfully.")
            else:
                messages.info(request, f"Existing brand '{brands_list.brand_name.capitalize()}' used.")

            if brand_created:
                messages.success(request, f"Brand '{brands_list.brand_name.capitalize()}' added to category '{category.category_name}'.")
            else:
                messages.info(request, f"Brand '{brands_list.brand_name.capitalize()}' already exists in category '{category.category_name}'.")

            return redirect('application:brands', category_id=category_id)
    else:
        brands_list_form = BrandsListForm()

    return render(request, 'add_item/add_brand.html', {
        'brands_list_form': brands_list_form,
        'category': category
    })





@login_required
def add_product(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.brand = brand
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('application:product', brand_id=brand_id)
        else:
            # If form is not valid, return to the form with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    return render(request, 'add_item/add_product.html', {'form': form, 'brand': brand})