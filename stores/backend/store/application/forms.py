# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  AuthenticationForm
from .models import Profile
from django import forms
from .models import Category, Brands_list, Brand, Product

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'photo']

class BrandsListForm(forms.ModelForm):
    class Meta:
        model = Brands_list
        fields = ['brand_name', 'photo']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'purchase_price', 'sale_price', 'quantity_in_stock', 'photo']

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise forms.ValidationError('Product name is required.')
        
        # Normalize the product name (lowercase for uniqueness check)
        normalized_name = product_name.strip().lower()

        # Only check for existing products if this is not an edit operation
        if not self.is_edit:
            if Product.objects.filter(product_name__iexact=normalized_name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('A product with this name already exists.')
        
        # Capitalize the product name before saving
        return product_name.strip().capitalize()

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if purchase_price is None:
            raise forms.ValidationError('Purchase price is required.')
        if purchase_price <= 0:
            raise forms.ValidationError('Purchase price must be greater than zero.')
        return purchase_price

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price is None:
            raise forms.ValidationError('Sale price is required.')
        if sale_price <= 0:
            raise forms.ValidationError('Sale price must be greater than zero.')
        if sale_price < self.cleaned_data.get('purchase_price', 0):
            raise forms.ValidationError('Sale price must be greater than purchase price.')
        return sale_price

    def clean_quantity_in_stock(self):
        quantity = self.cleaned_data.get('quantity_in_stock')
        if quantity is None:
            raise forms.ValidationError('Quantity in stock is required.')
        if quantity < 0:
            raise forms.ValidationError('Quantity in stock cannot be negative.')
        return quantity

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Validate photo size
            max_size_mb = 5  # Maximum file size in MB
            max_size_bytes = max_size_mb * 1024 * 1024
            if photo.size > max_size_bytes:
                raise forms.ValidationError(f'Photo size should not exceed {max_size_mb} MB.')
        return photo