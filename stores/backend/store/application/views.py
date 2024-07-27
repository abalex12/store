from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Brand, Product, Purchase, Sale
from django.db.models import F
from django.db import transaction
from django.contrib.auth import login, authenticate,logout
from django.urls import reverse
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(reverse('admin:index'))
            else:
                return redirect('application:category')  
        else:
            messages.error(request, 'Invalid username or password.Try again')
            return redirect('application:login')
    
    else:
    
       return render(request, 'login.html')

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('application:login')

@login_required
def opencatagories(request):
    categories=Category.objects.all()
    context ={
        "categories":categories
    }
    return render(request,"category.html",context)
@login_required
def openbrand(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    brands = Brand.objects.filter(category=category)

    context = {
        "brands":brands,
        "category":category,
    }
    return render (request,"brand.html",context)


@login_required
def product_list(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    products = Product.objects.filter(brand=brand)

    context = {
        "products":products,
        'brand':brand
    }
    return render(request,"product.html",context)


@login_required
@transaction.atomic
def make_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        confirm = request.POST.get('confirm')
        
        product = get_object_or_404(Product, pk=product_id)
        
        if not confirm:
            # This is the initial form submission, show confirmation
            context = {
                'product': product,
                'quantity': quantity,
                'confirm': True
            }
            return render(request, 'confirm_sale.html', context)
        
        # This is the confirmed submission
        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('application:product', brand_id=product.brand.id)
        
        if quantity > product.quantity_in_stock :
            messages.error(request,"Not enough quantity in Stock")
            return redirect('application:product', brand_id=product.brand.id)
        
        product.quantity_in_stock = F('quantity_in_stock') - quantity
        product.save()

        Sale.objects.create(
            product=product,
            quantity_sold=quantity,
            employee=request.user
        )
        
        messages.success(request, f"Successfully sold {quantity} units of {product.product_name}")
        return redirect('application:category')
    
    return redirect('application:category')

@login_required
def sale_history(request):
    # Get all sales for the logged-in employee
    all_sales = Sale.objects.filter(employee=request.user).order_by('-sale_date')

    # Calculate all-time total money made
    all_time_total = all_sales.aggregate(
        total=Sum(F('quantity_sold') * F('product__sale_price'))
    )['total'] or 0

    # Get filter dates from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply date filters if provided
    if start_date:
        all_sales = all_sales.filter(sale_date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        all_sales = all_sales.filter(sale_date__lte=datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))

    # Calculate filtered total money made
    filtered_total = all_sales.aggregate(
        total=Sum(F('quantity_sold') * F('product__sale_price'))
    )['total'] or 0

    context = {
        'sales': all_sales,
        'all_time_total': all_time_total,
        'filtered_total': filtered_total,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'sale_history.html', context)




@login_required
def inventory_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.GET.get('action')
        if action == 'get_brands':
            category_id = request.GET.get('category_id')
            brands = Brand.objects.filter(category_id=category_id).annotate(
                product_count=Count('product'),
                total_stock=Sum('product__quantity_in_stock')
            ).values(
                'id', 
                'brand_name__brand_name', 
                'brand_name__photo', 
                'product_count', 
                'total_stock'
            )
            # Add full URL to brand photos
            for brand in brands:
                if brand['brand_name__photo']:
                    brand['brand_name__photo'] = request.build_absolute_uri(settings.MEDIA_URL + brand['brand_name__photo'])
            return JsonResponse(list(brands), safe=False)
        elif action == 'get_products':
            brand_id = request.GET.get('brand_id')
            products = Product.objects.filter(brand_id=brand_id).values(
                'id', 'product_name', 'quantity_in_stock', 'purchase_price', 'sale_price', 'photo'
            )
            # Add full URL to product photos
            for product in products:
                if product['photo']:
                    product['photo'] = request.build_absolute_uri(settings.MEDIA_URL + product['photo'])
            return JsonResponse(list(products), safe=False)
    else:
        categories = Category.objects.annotate(
            brand_count=Count('brand'),
            product_count=Count('brand__product'),
            total_stock=Sum('brand__product__quantity_in_stock')
        )
        return render(request, 'inventory.html', {'categories': categories})
    



