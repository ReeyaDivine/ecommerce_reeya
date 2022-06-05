from unicodedata import category, name
from django.db import models
from django.utils.html import mark_safe


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name
 
class Category(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()


    class Meta:
        verbose_name_plural = "Categories"

    
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    image_url = models.CharField(max_length=500)
    color_code = models.CharField(max_length=20)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    registered_on = models.DateTimeField()
    is_active = models.BooleanField()

    def image_tag(self):
        return mark_safe(f'< img src="{self.image}" width= "50" height= "50"/>')

    image_tag.short_description = "Product"
        
def __str__(self):
            return self.name