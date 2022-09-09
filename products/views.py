from django.shortcuts import render
from django.core.paginator import Paginator

from products.forms import ProductsFilterForm
from products.models import Product


def products(request):
    queryset = Product.objects.all()
    filter_form = ProductsFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data["price_from"]:
            queryset = queryset.filter(price__gte=filter_form.cleaned_data["price_from"])
        if filter_form.cleaned_data["price_to"]:
            queryset = queryset.filter(price__lte=filter_form.cleaned_data["price_to"])
        if filter_form.cleaned_data["order"]:
            queryset = queryset.order_by(filter_form.cleaned_data["order"])

    page_number = request.GET.get("page")
    paginator = Paginator(queryset, 15)
    page = paginator.get_page(page_number)

    return render(request, "index.html", {"page": page, "filter_form": filter_form})
