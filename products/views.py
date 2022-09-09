from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from products.forms import ProductsFilterForm
from products.models import Product, Favorite


def products(request):
    queryset = Product.objects.all()
    filter_form = ProductsFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data["price_from"]:
            queryset = queryset.filter(
                price__gte=filter_form.cleaned_data["price_from"]
            )
        if filter_form.cleaned_data["price_to"]:
            queryset = queryset.filter(price__lte=filter_form.cleaned_data["price_to"])
        if filter_form.cleaned_data["order"]:
            queryset = queryset.order_by(filter_form.cleaned_data["order"])

    page_number = request.GET.get("page")
    paginator = Paginator(queryset, 15)
    page = paginator.get_page(page_number)

    return render(request, "index.html", {"page": page, "filter_form": filter_form})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        if request.POST.get("action") == "add_to_favorites":
            queryset = Favorite.objects.filter(user=request.user, product=product)
            if queryset.exists():
                queryset.delete()
            else:
                Favorite.objects.create(user=request.user, product=product)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, product=product
        ).exists()
    return render(
        request, "details.html", {"product": product, "is_favorite": is_favorite}
    )
