from django.db import models
from store.models.category import Category
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    discription = models.CharField(max_length=100,default="", null=True, blank=True)
    image = models.ImageField(upload_to="uploads/product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_categoryid(category_id):
        if category_id :
            return Product.objects.filter(category=category_id) #category is the field in product table
        else:
            return Product.get_all_products()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)