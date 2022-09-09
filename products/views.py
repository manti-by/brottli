from django.shortcuts import render
from django.core.paginator import Paginator

from products.models import Product


def products(request):
    paginator = Paginator(Product.objects.all(), 15)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})
