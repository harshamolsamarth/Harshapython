from django.contrib import admin
from .models.category import Category
from .models.customer import Customer
from .models.product import Product
from .models.orders import Order
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_price', 'discription', 'image', 'category']

admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']

admin.site.register(Category, CategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_no', 'email', 'password']

admin.site.register(Customer, CustomerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price', 'address', 'phone', 'date', 'status']

admin.site.register(Order, OrderAdmin)