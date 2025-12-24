from django import forms
from django_select2.forms import ModelSelect2Widget

from crm.models import Client, Vehicle
from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    """
    Order form class with Select2 widget to search by client name,
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2Widget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={
                "class": "form-control",
                "data-placeholder": "Search by client's name",
            }
        ),
        required=True,
        label="Client"
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(client=client),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
        label="Vehicle"
    )

    class Meta:
        model = Order
        fields = "__all__"


class InvoiceForm(forms.ModelForm):
    """
    Invoice creating form class to choose orders only without invoices
    """
    class Meta:
        model = Invoice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].label = "Select current order"
        self.fields["order"].queryset = Order.objects.filter(
            invoice__isnull=True
        )


class InvoiceUpdateForm(forms.ModelForm):
    """
    Invoice update form class to update only price of the parts
    """
    class Meta:
        model = Invoice
        fields = ("parts_total",)


class OrderUpdateForm(forms.ModelForm):
    """
    Order update form class to update only requirements and status
    """
    class Meta:
        model = Order
        fields = ("requirements", "status")


class OrderClientLastNameSearchForm(forms.Form):
    """
    Searching orders by client last name
    """
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control float-right",
            "placeholder": "Search by client last name",
        })
    )
