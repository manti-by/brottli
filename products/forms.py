from django import forms

ORDER_CHOICES = (
    ("price", "Price Asc"),
    ("-price", "Price Desc"),
)


class ProductsFilterForm(forms.Form):
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)
    price_from = forms.IntegerField(required=False)
    price_to = forms.IntegerField(required=False)
