from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Profile model to extend the User model with an optional photo field
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices= [
    ('Employee', 'Employee'),
    ('Admin', 'Admin')
], null= True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.category_name


    
class Brands_list(BaseModel):
    brand_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def __str__(self):
        return f'{self.brand_name}'


class Brand(BaseModel):
    brand_name = models.ForeignKey(Brands_list, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
 
    def __str__(self):
        return f'{self.brand_name}'
    
class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField()
    photo = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.product_name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})

    def __str__(self):
        return f"Purchase of {self.product} on {self.purchase_date}"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})

    def __str__(self):
        return f"Sale of {self.product} on {self.sale_date}"
