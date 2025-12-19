from django import forms
from django_select2.forms import ModelSelect2Widget

from crm.models import Client, Vehicle
from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2Widget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=ModelSelect2Widget(
            model=Vehicle,
            search_fields=[
                "number_registration__icontains",
            ],
            attrs={"class": "form-control"}
        ),
        required=True,
    )

    class Meta:
        model = Order
        fields = "__all__"


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].label = "Select order without invoice"
        self.fields["order"].queryset = Order.objects.filter(invoice__isnull=True)

class InvoiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("parts_total",)


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("requirements", "status")
