from django.shortcuts import render

from products.models import Product


def products(request):
    product_list = Product.objects.all()
    return render(request, "index.html", {"product_list": product_list})