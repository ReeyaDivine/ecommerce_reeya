from django.db import models

# Create your models here.
class Brand(models.model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()
