from django.contrib import admin

# Register your models here.
from .models import Brand,Category,Product



admin.site.register(Brand)
admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","brand","category",]
    search_fields = ["name","price","brand__name","category__name",]
    list_filter = ["brand", "category",]
    readonly_fields = ["quantity"]


class Meta:
    model = Product 

    admin.site.register(Product,ProductAdmin)

