from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from .models import Product, Brand, Category
...
def index(request):
        if request.method == "GET":
            category_id = request.GET.get("category") 
            brand_id = request.GET.get("brand")
            if category_id: 
                filter_query = Q(category__id=category_id) 
                products = Product.objects.filter(filter_query) 
            elif brand_id:
                filter_query = Q(brand__id=brand_id)
                products = Product.objects.filter(filter_query)
            else:
                products = Product.objects.all()
                categories = Category.objects.all()
                brands = Brand.objects.all()
                context = {
                'products': products,
                'categories': categories,
                'brands': brands,
                'search_query': '',
                }
            return render(request, 'index.html', context)

        elif request.method == "POST":
            q = request.POST.get("query")
            if "-" in q:
                price_values = q.split("-")
                filter_query = Q(price__gte=price_values[0]) & Q(price__lte=price_values[1])
            else:
             filter_query = Q(name__icontains=q) | Q(price__icontains=q) | Q(brand__name__icontains=q)
            products = Product.objects.filter(filter_query)
            categories = Category.objects.all()
            brands = Brand.objects.all()
            context = {
            'products': products,
            'categories': categories,
            'brands': brands,
            'search_query': q,
            }
            return render(request, 'index.html', context)