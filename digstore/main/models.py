from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
   name = models.CharField(max_length=100, unique=True)

   def __str__(self):
       return self.name

   class Meta:
       verbose_name = "Категория"
       verbose_name_plural = "Категории"


class Product(models.Model):
   name = models.CharField(max_length=50)
   description = models.TextField()
   price = models.DecimalField(max_digits=10, decimal_places=2)
   image = models.ImageField(upload_to='')
   rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
   sales_count = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   combinations = models.TextField(blank=True, help_text="Список комбинаций, разделенных запятыми")
   ratings = models.JSONField(default=list, blank=True)
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
   seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name="Продавец")

   def __str__(self):
       return self.name

   def update_rating(self, new_rating):
       self.ratings.append(new_rating)
       if self.ratings:
           self.rating = sum(self.ratings) / len(self.ratings)
       else:
           self.rating = 0
       self.save()

   def get_seller_stats(self):
       seller_products = Product.objects.filter(seller=self.seller)
       total_sales = sum(product.sales_count for product in seller_products)
       ratings = [r for p in seller_products for r in p.ratings]
       average_rating = sum(ratings) / len(ratings) if ratings else 0
       return {'total_sales': total_sales, 'average_rating': average_rating}

   class Meta:
       verbose_name = "Товар"
       verbose_name_plural = "Товары"