from django import forms
from django_select2.forms import ModelSelect2Widget

from crm.models import Client
from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            "client": ModelSelect2Widget(
                model=Client,
                search_fields=[
                    "last_name__icontains",
                    "first_name__icontains",
                    "mobile_number__icontains",
                ],
            )
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].label = "Cars"
        self.fields["order"].queryset = Order.objects.filter(invoice__isnull=True)