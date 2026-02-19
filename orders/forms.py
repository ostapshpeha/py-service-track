from django import forms
# Removed django_select2 imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div

from crm.models import Client, Vehicle
from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    """
    Order form class
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        # Use standard Select widget with tom-select class
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Search by client's name",
            }
        ),
        required=True,
        label="Client"
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Search by owner's name or license place",
            }
        ),
        required=True,
        label="Vehicle"
    )

    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('client', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('vehicle', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('status', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            'requirements',
            Submit('submit', 'Save Order', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get("client")
        vehicle = cleaned_data.get("vehicle")

        if client and vehicle:
            if vehicle.client != client:
                self.add_error(
                    "vehicle",
                    f"This vehicle belongs to {vehicle.client}, not {client}."
                )
        return cleaned_data


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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'order',
            'parts_total',
            Submit('submit', 'Create Invoice', css_class='w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


class InvoiceUpdateForm(forms.ModelForm):
    """
    Invoice update form class to update only price of the parts
    """
    class Meta:
        model = Invoice
        fields = ("parts_total",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'parts_total',
            Submit('submit', 'Update Invoice', css_class='w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


class OrderUpdateForm(forms.ModelForm):
    """
    Order update form class to update only requirements and status
    """
    class Meta:
        model = Order
        fields = ("requirements", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'status',
            'requirements',
            Submit('submit', 'Update Order', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


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
